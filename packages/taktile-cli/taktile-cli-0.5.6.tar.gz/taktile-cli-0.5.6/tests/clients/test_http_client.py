import os

import pytest
import requests
from pydantic import BaseModel

from tktl.core.clients.http_client import API, interpret_response
from tktl.core.config import settings
from tktl.core.exceptions.exceptions import APIClientException
from tktl.core.managers.auth import AuthConfigManager


def test_instantiate_api_client():
    key = os.environ["TEST_USER_API_KEY"]
    AuthConfigManager.set_api_key(key)
    client = API(api_url=settings.DEPLOYMENT_API_URL)
    assert "X-Api-Key" in client.default_headers
    assert client.default_headers["X-Api-Key"] == key
    assert (
        client.get_path(f"{settings.API_V1_STR}/deployments")
        == f"{settings.DEPLOYMENT_API_URL}{settings.API_V1_STR}/deployments"
    )

    assert client.get_path() == f"{settings.DEPLOYMENT_API_URL}"


def test_request_failures():
    client = API(api_url=settings.DEPLOYMENT_API_URL)
    response = client.post("non/existent/path")
    with pytest.raises(requests.exceptions.RequestException):
        response.raise_for_status()

    response = client.get("non/existent/path")
    with pytest.raises(requests.exceptions.RequestException):
        response.raise_for_status()

    response = client.patch("non/existent/path")
    with pytest.raises(requests.exceptions.RequestException):
        response.raise_for_status()

    response = client.put("non/existent/path")
    with pytest.raises(requests.exceptions.RequestException):
        response.raise_for_status()

    response = client.delete("non/existent/path")
    with pytest.raises(requests.exceptions.RequestException):
        response.raise_for_status()


def test_interpret_response():
    client = API(api_url=settings.DEPLOYMENT_API_URL)
    response = client.post("non/existent/path")
    with pytest.raises(APIClientException):
        interpret_response(response, model=BaseModel)

    client = API(api_url="https://jsonplaceholder.typicode.com/todos/1")
    response = client.get()

    class TestModel(BaseModel):
        userId: int
        id: int
        title: str
        completed: bool

    interpreted = interpret_response(response, TestModel)
    assert interpreted.dict()["id"] == 1
