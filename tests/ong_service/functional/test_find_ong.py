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

@scenario("./test_find_ong.feature", "Finding a ONG")
def test_find_ong():
    pass

@given("I have all the required data", target_fixture="ong_required_data")
def ong_required_data():
    return generate_ongModel()

@given("ONG is registered", target_fixture="registered_ong")
def registered_ong(ong_required_data):
    response = ong_service.create_ong(ong_required_data)
    assert isinstance(response, ResponseDTO)
    assert response.status == http.HTTPStatus.CREATED
    assert response.message == "Ong created successfully"
    return ong_required_data.model_dump()

@when("I search for the ONG", target_fixture="search_ong")
def search_ong(registered_ong):
    return ong_service.get_ong_by_cnpj(registered_ong['cnpj'])

@then("The ONG should be found")
def find_ong(search_ong, registered_ong):
    assert isinstance(search_ong, dict)
    for key, value in registered_ong.items():
        assert value == search_ong[key]