""" Create ong service tests """
import http
import pytest
from pytest_bdd import given, when, then, scenario
from app.services.ong_service import OngService
from app.domain.models.ong import OngModel
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


@scenario("./test_create_ong.feature", "Creating a ONG")
def test_create_ong():
    pass

@given("I have all the required data", target_fixture="ong_required_data")
def ong_required_data():
    return generate_ongModel()

@given("ONG is not registered")
def ong_not_registered(ong_required_data):
    ong = ong_service.get_ong_by_cnpj(ong_required_data.model_dump()['cnpj'])
    assert ong is None

@when("I register the ONG", target_fixture="register_ong")
def register_ong(ong_required_data) -> ResponseDTO:
    response = ong_service.create_ong(ong_required_data)
    return response

@then("The ONG should be registered")
def verify_ong_registered(register_ong):
    assert isinstance(register_ong, ResponseDTO)
    assert register_ong.status == http.HTTPStatus.CREATED
    assert register_ong.message == "Ong created successfully"




scenario("./test_create_ong.feature", "Creating a ONG with not all required data")
def test_create_ong_with_not_all_required_data():
    pass

@given("I do not have all the required data", target_fixture="ong_invalid_data")
def ong_invalid_data() -> OngModel:
    return OngModel()

@when("I register the ONG with invalid data", target_fixture="register_ong_invalid_data")
def register_ong_invalid_data(ong_invalid_data) -> ResponseDTO:
    response = ong_service.create_ong(ong_invalid_data)
    return response

@then("I should see the error message")
def verify_ong_registered(register_ong_invalid_data):
    assert isinstance(register_ong_invalid_data, ResponseDTO)
    # FIXME: Isso por algum motivo ta passando, o certo é ser BAD_REQUEST
    assert register_ong_invalid_data.status == http.HTTPStatus.IM_A_TEAPOT
    assert register_ong_invalid_data.message == "Missing required fields: {'cnpj', 'email', 'state', 'foundation', 'description', 'phone', 'logo', 'password', 'mission', 'name', 'city'}"
    