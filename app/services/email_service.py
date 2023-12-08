from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import logging
import smtplib
import http

from app.domain.models.email import EmailModel
from app.domain.models.dto.response import ResponseDTO
from app.domain.models.email_template.html_email_template import get_html_text


class EmailService:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def _server_email_connection(self):
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        return server

    def _config_email_data(self, email: EmailModel, message: str):
        email_config = MIMEMultipart()

        email_config["From"] = email.sender_email
        email_config["To"] = email.recipient_email
        email_config["Subject"] = email.subject
        email_config.attach(MIMEText(message, "html"))

        return email_config

    def send_email(
        self,
        email: EmailModel,
        request_id: str = ""
    ):
        self.logger.info(f"id={request_id} Start service")

        try:
            message = get_html_text(email.adopter_name, email.animal_name, email.form_link)

            email_config = self._config_email_data(email, message)

            server = self._server_email_connection()
            server.login(email_config["From"], email.password)

            server.sendmail(email_config["From"], email_config["To"], email_config.as_string())

            server.quit()


            self.logger.info(f"id={request_id} E-mail sent successfully")
            return ResponseDTO(None, "E-mail sent successfully", http.HTTPStatus.CREATED)

        except Exception as exc:
            self.logger.error(f"id={request_id} Error sending e-mail: {exc}")
            return ResponseDTO(None, "Error sending e-mail", http.HTTPStatus.INTERNAL_SERVER_ERROR)
