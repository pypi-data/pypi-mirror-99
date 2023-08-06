import requests

API_URL = "https://API.jagthefriend.repl.co"
GITHUB_REPO = "https://github.com/JagTheFriend/Complex-API"

__version__ = "0.0.7"
__all__ = [
    "compile", "reddit", "lyrics",
    "ascii", "temp", "length",
    "inspire", "calculator", "hex_to_denary"
]


def main() -> str:
    return requests.get(f"{API_URL}").text


def compile(*, lang: str, code: str) -> dict:
    """
    Gets the result of compiling code from the `Compiler API`
    :param lang: The language which the compiler would use to compile code
    :param code: The code to be compiled
    :return: Dictionary
    """
    return requests.get(f"{API_URL}/compile={lang}_{code}").json()


def reddit(*, limit: float, subreddit: str) -> dict:
    """
    Gets a limited amount of posts from a specific subreddit
    :param subreddit: Name of the subreddit
    :param limit: Number of posts to be returned
    :return: Dictionary
    """
    return requests.get(f"{API_URL}/reddit={subreddit}+{limit}").json()


def lyrics(*, song: str) -> dict:
    """
    Gets the lyrics of a song from the `Lyrics API`
    :param song: Name of the song
    :return: Dictionary
    """
    return requests.get(f"{API_URL}/lyrics+{song}").json()


def ascii(*, text: str) -> dict:
    """
    Gets Pixel art from the ASCII API
    :param text: The text which should be converted to Pixel art
    :return: Dictionary
    """
    return requests.get(f"{API_URL}/ascii_{text}").json()


def temp(*, place: str, unit: str = "metric") -> dict:
    """
    Gets the weather of a place
    :param place: The name of the place whose weather would be found
    :param unit: The unit used for measuring amounts,
                (it can be either 'metric' or 'imperial)
    :return: Dictionary
    """
    return requests.get(f"{API_URL}/temp={place}+{unit}").json()


def length(*, playlist: str) -> dict:
    """
    Gets the length of playlist
    :param playlist: This a unique id given to each playlist
    :return: Dictionary
    """
    return requests.get(f"{API_URL}/length+{playlist}").json()


def inspire() -> dict:
    """
    Gets a random inspirational text
    :return: Dictionary
    """
    return requests.get(f"{API_URL}/inspire").json()


def calculator(*, formula: str) -> dict:
    """
    Gets the result of a calculation
    :param formula: Stuff on which calculation will be carried
    :return: Dictionary
    """
    new_formula = formula.replace('/', '\\')
    return requests.get(f"{API_URL}/cal_{new_formula}").json()


def hex_to_denary(*, hex_code: str) -> dict:
    """
    Converts Hexadecimal code to decimal(or denary)
    :param formula: Stuff on which calculation will be carried on
    :return: Dictionary
    """
    return requests.get(f"{API_URL}/hex+{hex_code}").json()


def binary_to_denary(*, binary) -> dict:
    """
    Converts Denary code to binary
    :param binary: Stuff on which calculation will be carried on Example: 4569
    :return: Dictionary
    """
    return requests.get(f"{API_URL}/binary={binary}").json()
