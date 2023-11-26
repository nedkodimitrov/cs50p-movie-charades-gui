from openai.error import AuthenticationError
import pytest
from requests import RequestException
from unittest.mock import patch, MagicMock

from helpers import get_random_movie_title, download_ai_img, mask_string, guess_string


@patch("helpers.requests.get")
def test_get_random_movie_title(mock_requests_get):
    """Mock requests.get() to return "Back to the Future" and assert the same title is returned by get_random_movie_title()."""
    mock_response = MagicMock()
    # mock_response.status_code = 200
    mock_response.json.return_value = {"results": [{"title": "Back to the Future"}]}
    mock_requests_get.return_value = mock_response

    assert get_random_movie_title() == "Back to the Future"


@patch("helpers.requests.get")
def test_fail_get_random_movie_title(mock_requests_get):
    """
    Mock response.raise_for_status() to raise a RequestException and set response.status code to 401 and then 403.
    Assert that the program exits via sys.exit() and displays that the api key is not set.
    """
    mock_response = MagicMock()
    mock_response.raise_for_status.side_effect = RequestException()
    
    for status_code in [401, 403]:
        mock_response.status_code = status_code
        mock_requests_get.return_value = mock_response

        with pytest.raises(SystemExit) as e:
            get_random_movie_title()
        assert e.value.args[0] == "MoviesMiniDatabase request error. X_RAPIDAPI_API_KEY not set or incorrect."


@patch("helpers.openai.Image.create")
def test_download_ai_img(mock_openai_image_create):
    """Mock helpers.openai.Image.create() to return base64 data and assert that download_ai_img() returns True."""
    from base64 import b64encode

    # Set the return value for the mock_openai_image_create function
    mock_openai_image_create.return_value = {
        "data": [{"b64_json": b64encode("somerandomdata".encode())}]
    }
    assert download_ai_img("") == True

@patch("helpers.openai.Image.create")
def test_fail_download_ai_img(mock_openai_image_create):
    """
    Mock helpers.openai.Image.create() to raise an AuthenticationError.
    Assert that the program exits via sys.exit() and displays that the api key is not set
    """
    mock_openai_image_create.side_effect = AuthenticationError()

    with pytest.raises(SystemExit) as e:
        download_ai_img("")

    assert e.value.args[0] == "OPENAI DALL-E 2 request error. OPENAI_API_KEY not set or incorrect."


def test_mask_string():
    assert mask_string("") == ""
    assert mask_string("H") == "H"
    assert mask_string("hello world") == "h____ _____"
    assert mask_string("Hello, world!") == "H____, _____!"


def test_fail_mask_string():
    with pytest.raises(TypeError):
        mask_string()
        mask_string(1)


@patch("helpers.input")
def test_guess_string(mock_input):
    """Mock input() to simulate a correct movie title guess and assert True return value from guess_string()."""
    mock_input.return_value = "Back to the Future"
    assert guess_string("Back to the Future") == True


@patch("helpers.input")
def test_fail_guess_string(mock_input):
    """Mock input() to simulate a wrong movie title guess and assert False return value from guess_string()."""
    mock_input.return_value = "I don't know"
    assert guess_string("Back to the Future") == False

    with pytest.raises(TypeError):
        guess_string()
        guess_string(1)


if __name__ == "__main__":
    main()