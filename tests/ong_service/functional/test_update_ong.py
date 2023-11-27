""" Create ong service tests """
import http
from faker import Faker
import pytest
from pytest_bdd import given, when, then, scenario
from app.domain.models.ong import OngModel
from app.services.ong_service import OngService
from app.domain.models.dto.response import ResponseDTO
import os

from tests.ong_service.utils import generate_ongModel

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

ong_service = OngService()

ongModel = generate_ongModel()


fake = Faker("pt_BR")

fieldsToUpdate = {
    "name": fake.name(),
    "email": fake.email(),
    "phone": fake.phone_number(),
    "city": fake.city(),
    "state": fake.state_abbr(),
}

notAllowedFieldsToUpdate = ["cnpj", "password", "created_at", "updated_at", "id"]

@scenario("./test_update_ong.feature", "Updating a ONG")
def test_update_ong():
    pass

@given("I have all the required data to update", target_fixture="ong_update_data")
def ong_update_data():
    newOngModel = OngModel(**{ key: value for key, value in ongModel.model_dump().items() if key not in notAllowedFieldsToUpdate })
    for key, value in fieldsToUpdate.items():
        setattr(newOngModel, key, value)

    return newOngModel

@given("ONG is registered", target_fixture="registered_ong")
def registered_ong() -> ResponseDTO:
    newModel = generate_ongModel()
    response = ong_service.create_ong(newModel)
    assert isinstance(response, ResponseDTO)
    assert response.status == http.HTTPStatus.CREATED
    assert response.message == "Ong created successfully"
    return response.data

@when("I update the ONG", target_fixture="update_ong")
def update_ong(ong_update_data, registered_ong) -> ResponseDTO:
    return ong_service.update_ong(ong_update_data, registered_ong['id'])

@then("All the data should be updated")
def verify_updated_data(update_ong):
    assert isinstance(update_ong, ResponseDTO)
    assert update_ong.status == http.HTTPStatus.OK
    assert update_ong.message == "Ong updated successfully"



@scenario("./test_update_ong.feature", "Updating a ONG that does not exist")
def test_update_ong_not_exist():
    pass

@given("ONG is not registered", target_fixture="not_registered_ong")
def not_registered_ong() -> OngModel:
    return generate_ongModel()

@when("I update the ONG that does not exist", target_fixture="update_ong_not_exist")
def update_ong_not_exist(not_registered_ong) -> ResponseDTO:
    # TODO: Generate random mongodb id to test this
    mongodb_id = "6564de210c2dcd7815894313"
    return ong_service.update_ong(not_registered_ong, mongodb_id)

@then("I should receive an error message")
def verify_error_message(update_ong_not_exist):
    assert isinstance(update_ong_not_exist, ResponseDTO)
    assert update_ong_not_exist.status == http.HTTPStatus.NOT_FOUND
    assert update_ong_not_exist.message == "Ong not found"