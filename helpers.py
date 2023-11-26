from base64 import b64decode
import openai
from os import getenv
from PIL import Image
from pyfiglet import Figlet
from random import randint
from re import sub
import requests
from sys import exit
from time import sleep


def print_welcome():
    """Using pyfiglet prints a welcome message with ASCII art title and information about the AI and database used."""
    figlet = Figlet()
    figlet.setFont(font="small")
    print(figlet.renderText("CS50P Movie Charades"))

    figlet.setFont(font="straight")
    print(figlet.renderText("Powered by OpenAI DALL-E 2 API and MoviesMiniDatabase RapidAPI"))


def get_random_movie_title() -> str:
    """
    Get a random movie title from the top 1000 rated movies on MoviesMiniDatabase using RapidAPI using request.get().

    :return: A string containing a movie title.
    :rtype: str

    :raises SystemExit: If the request is unsuccessful.
    """
    url = "https://moviesminidatabase.p.rapidapi.com/movie/order/byRating/"
    headers = {
        "X-RapidAPI-Key": getenv("X_RAPIDAPI_API_KEY"),
        "X-RapidAPI-Host": "moviesminidatabase.p.rapidapi.com",
    }
    querystring = {
        "page_size": "1",
        "page": randint(1, 1000)
    }

    # loop in case there is a connection issue. Try to reconnect unless user terminates the program
    while True:
        try:
            response = requests.get(url, headers=headers, params=querystring)
            # raise HTTPError (subclass of RequestError) if the request was unsuccessful
            response.raise_for_status()
        except requests.ConnectionError:
            print("MoviesMiniDatabase request error. There was a connection issue. Trying to reconnect in 60 seconds. Press Ctrl + C to exit instead.")
            try:
                sleep(60)
            except KeyboardInterrupt:
                exit("\nTerminated by user.")
        except requests.RequestException as e:
            if response.status_code in [401, 403]:
                exit("MoviesMiniDatabase request error. X_RAPIDAPI_API_KEY not set or incorrect.")
            exit(e)
        else:
            return response.json()["results"][0]["title"]


def download_ai_img(img_prompt: str, image_file_name: str = "image.png") -> bool:
    """
    Download an AI-generated image from the DALL·E 2 API, utilizing a provided prompt using openai.Image.create().

    :param img_prompt: The prompt that will be used by DALL-E 2 to generate the image.
    :type img_prompt: str

    :param image_file_name: The name of the image file that will be saved (Default: "image.png").
    :type image_file_name: str

    :return: True ifsuccessfully downloaded AI-generated image
    :rtype: bool

    :raises SystemExit: If the request is unsuccessful.
    """
    openai.api_key = getenv("OPENAI_API_KEY")

    # loop in case there is a connection issue. Try to reconnect unless user terminates the program
    while True:
        try:
            response = openai.Image.create(prompt=img_prompt, n=1, size="512x512", response_format="b64_json")
        except openai.error.APIConnectionError:
            print("OPENAI DALL-E 2 request error. There was a connection issue. Trying to reconnect in 60 seconds. Press Ctrl + C to exit instead.")
            try:
                sleep(60)
            except KeyboardInterrupt:
                exit("\nTerminated by user.")
        except openai.error.AuthenticationError:
            exit("OPENAI DALL-E 2 request error. OPENAI_API_KEY not set or incorrect.")
        except openai.error.OpenAIError as e:
            exit(e)
        else:
            img_file = open(image_file_name, "wb")
            img_file.write(b64decode(response["data"][0]["b64_json"]))
            img_file.close()
            return True


def open_img(image_file_name: str = "image.png"):
    """Open and show an image using Pillow."""
    img = Image.open(image_file_name)
    img.show()


def mask_string(string: str) -> str:
    """
    Mask a string by replacing every alphanumeric character except the first one with an underscore.

    :param string: The input string.
    :type string: str

    :return: The masked string.
    :rtype: str

    :raises TypeError: If the input is not a string.
    """
    return string[0] + sub(r"\w", "_", string[1:]) if len(string) > 1 else string


def guess_string(answer: str, attempts: int = 3) -> bool:
    """
    Prompt the user to guess a string in a case-insensitive manner.

    :param answer: The correct answer that the user has to guess.
    :type answer: str

    :param attempts: Number of attempts the user is given to guess the string. (Default: 3)
    :type attempts: int

    :return: True if the user successfully guessed, False otherwise.
    :rtype: bool

    :raises TypeError: If the function is called with no arguments.
    :raises AttributeError: If the "answer" argument is not a string.
    """
    answer = answer.lower()

    for _ in range(attempts):
        guess = input("Guess: ").strip().lower()

        if guess == answer:
            return True
        else:
            print("Wrong answer!")

    return False
