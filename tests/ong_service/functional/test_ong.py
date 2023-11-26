""" Create ong service tests """
import datetime
import http
import pytest
from pytest_bdd import given, when, then, scenario
from app.services.ong_service import OngService
from app.domain.models.ong import OngModel
from app.domain.models.dto.response import ResponseDTO
import os
from faker import Faker 

@scenario("./ong.feature", "Creating a ONG")
def test_create_ong():
    pass

@pytest.fixture()
def setup():
    if not os.getenv("ENVIRONMENT"):
        raise Exception("ENVIRONMENT variable is not set")

    if os.getenv("ENVIRONMENT") != "test":
        if not os.getenv("DATABASE_URL_TEST"):
            raise Exception("DATABASE_URL_TEST variable is not set")
        if not os.getenv("DATABASE_NAME_TEST"):
            raise Exception("DATABASE_NAME_TEST variable is not set")
        print(os.getenv("DATABASE_URL_TEST"))
        raise Exception("ENVIRONMENT must be test")

fake = Faker("pt_BR")
ong_service = OngService()

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
        created_at=datetime.datetime.now().isoformat(),
        updated_at=datetime.datetime.now().isoformat()
    )
    return ongModel

ongModel = generate_ongModel()

@given("I have all the required data", target_fixture="ong_required_data")
def ong_required_data():
    return ongModel

@given("ONG is not registered")
def ong_not_registered(ong_required_data):
    ong = ong_service.get_ong_by_cnpj(ong_required_data.dict()['cnpj'])
    assert ong is None

@when("I register the ONG", target_fixture="register_ong")
def register_ong(ong_required_data) -> ResponseDTO:
    response = ong_service.create_ong(ong_required_data)
    return response

@then("I should be able to login with the ONG")
def login_with_ong(register_ong):
    assert isinstance(register_ong, ResponseDTO)
    assert register_ong.status == http.HTTPStatus.CREATED
    assert register_ong.message == "Ong created successfully"

@scenario("./ong.feature", "Finding a ONG")
def test_find_ong():
    pass

@given("ONG is registered", target_fixture="registered_ong")
def registered_ong():
    ong = ong_service.get_ong_by_cnpj(ongModel.dict()['cnpj'])
    assert ong is not None
    return ong

@when("I search for the ONG", target_fixture="search_ong")
def search_ong(registered_ong):
    return ong_service.get_ong_by_cnpj(registered_ong['cnpj'])

@then("I should be able to find the ONG")
def find_ong(search_ong):
    # Add code here to verify that the ONG was found
    pass

@scenario("./ong.feature", "Updating a ONG")
def test_update_ong():
    pass

@given("I have all the required data to update", target_fixture="ong_update_data")
def ong_update_data():
    newOngModel = ongModel
    # change some fields
    newOngModel.name = fake.name()
    newOngModel.email = fake.email()
    newOngModel.phone = fake.phone_number()
    newOngModel.city = fake.city()
    return newOngModel

@given("ONG is registered", target_fixture="registered_ong")
def registered_ong():
    newModel = generate_ongModel()
    response = ong_service.create_ong(newModel)
    global ongId 
    ongId = response.data['id']
    assert ongId is not None

@when("I update the ONG", target_fixture="update_ong")
def update_ong(ong_update_data):
    return ong_service.update_ong(ong_update_data, ongId)

@then("All the data should be updated")
def verify_updated_data(update_ong):
    assert isinstance(update_ong, ResponseDTO)
    assert update_ong.status == http.HTTPStatus.OK
    assert update_ong.message == "Ong updated successfully"
