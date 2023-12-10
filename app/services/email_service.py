import logging
import smtplib
import http

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from bson import ObjectId

from app.config.settings import settings
from app.domain.models.email import EmailModel
from app.domain.models.dto.response import ResponseDTO
from app.domain.models.email_template.html_email_template import get_html_text
from app.services.form_service import FormService


class EmailService:
    def __init__(self, form_service: FormService):
        self.logger = logging.getLogger(__name__)
        self.form_service = form_service
        self.sender_email = "adocaocaosciente@gmail.com"
        self.subject = "Adocãosciente: formulário de adoção"
        self.password = settings.EMAIL_PASSWORD

    def _server_email_connection(self):
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        return server

    def _send_single_email(self, server, email_config, email_to_send):
        try:
            email_config["From"] = self.sender_email
            email_config["To"] = email_to_send
            server.sendmail(self.sender_email, email_to_send, email_config.as_string())

            return None
        except Exception as exc:
            self.logger.error(f"Error sending e-mail to {email_to_send}: {exc}")
            return email_to_send

    def send_email(self, email: EmailModel, request_id: str = "") -> ResponseDTO:
        self.logger.info(f"id={request_id} Start service")
        try:
            form_link = f"https://adocao-caosciente-frontend-adocaosciente.vercel.app/login?adoption_form={email.form_id}"
            
            result = list(self.form_service.form_collection.aggregate([
                {"$match": {"_id": ObjectId(email.form_id)}},
                {"$addFields": { "animal_id_obj": { "$toObjectId": "$animal_id" }}},
                {"$lookup": {
                    "from": "animals",
                    "localField": "animal_id_obj",
                    "foreignField": "_id",
                    "as": "animal"
                }},
                {"$unwind": "$animal"},
                {"$project": {
                    "animalName": "$animal.name",
                }}
            ]))
            animal_name = result[0]["animalName"]
            
            message = get_html_text(animal_name, form_link)

            email_config = MIMEMultipart()
            email_config["Subject"] = self.subject
            email_config.attach(MIMEText(message, "html"))

            server = self._server_email_connection()
            server.login(self.sender_email, self.password)

            failed_recipients = []
            for email_to_send in email.recipient_emails:
                result = self._send_single_email(server, email_config, email_to_send)
                if result is not None:
                    failed_recipients.append(result)

            server.quit()
            if len(failed_recipients) == len(email.recipient_emails):
                self.logger.error(f"id={request_id} Error sending e-mail to all recipients")
                return ResponseDTO(None, "Error sending e-mail to all recipients", http.HTTPStatus.INTERNAL_SERVER_ERROR)

            if len(failed_recipients) > 0:
                self.logger.info(f"id={request_id} Email not sent to {failed_recipients}")
                return ResponseDTO({"failed_recipients": failed_recipients}, f"Error sending e-mail to {failed_recipients}", http.HTTPStatus.OK)

            self.logger.info(f"id={request_id} E-mail sent successfully to all recipients")
            return ResponseDTO(None, "E-mail sent successfully to all recipients", http.HTTPStatus.OK)

        except Exception as exc:
            self.logger.error(f"id={request_id} Error sending e-mail: {exc}")
            return ResponseDTO(None, "Error sending e-mail", http.HTTPStatus.BAD_REQUEST)
