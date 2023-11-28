from app.domain.models.ong import OngModel
from faker import Faker
from datetime import datetime

fake = Faker("pt_BR")

def generate_ongModel():
    ongModel = OngModel(
        name=fake.name(),
        cnpj=fake.cnpj(),
        email=fake.email(),
        phone=fake.phone_number(),
        city=fake.city(),
        state=fake.state_abbr(),
        description=fake.text(),
        foundation=fake.date(),
        logo=fake.image_url(),
        mission=fake.text(),
        password=fake.password(),
        created_at=datetime.now().isoformat(),
        updated_at=datetime.now().isoformat()
    )
    return ongModel