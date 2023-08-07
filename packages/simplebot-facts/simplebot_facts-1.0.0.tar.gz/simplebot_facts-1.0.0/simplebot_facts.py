import bs4
import requests
import simplebot
from simplebot.bot import Replies

__version__ = "1.0.0"
HEADERS = {
    "user-agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:60.0)"
    " Gecko/20100101 Firefox/60.0"
}


@simplebot.command
def fact(payload: str, replies: Replies) -> None:
    """Get a random fact from https://dailyfacts.org"""
    replies.add(text=_get_fact())


@simplebot.command
def factOfTheDay(payload: str, replies: Replies) -> None:
    """Get the fact of the day from https://dailyfacts.org"""
    replies.add(text=_get_fact(""))


@simplebot.command
def factGeneral(payload: str, replies: Replies) -> None:
    """Get a random fact from the "general" category."""
    replies.add(text=_get_fact("general"))


@simplebot.command
def factScience(payload: str, replies: Replies) -> None:
    """Get a random fact from the "science" category."""
    replies.add(text=_get_fact("science"))


@simplebot.command
def factLifeHacks(payload: str, replies: Replies) -> None:
    """Get a random fact from the "life-hacks" category."""
    replies.add(text=_get_fact("life-hacks"))


@simplebot.command
def factSports(payload: str, replies: Replies) -> None:
    """Get a random fact from the "sports" category."""
    replies.add(text=_get_fact("sports"))


@simplebot.command
def factPsychology(payload: str, replies: Replies) -> None:
    """Get a random fact from the "psychology" category."""
    replies.add(text=_get_fact("psychology"))


@simplebot.command
def factBody(payload: str, replies: Replies) -> None:
    """Get a random fact from the "human-body" category."""
    replies.add(text=_get_fact("human-body"))


@simplebot.command
def factHistory(payload: str, replies: Replies) -> None:
    """Get a random fact from the "history" category."""
    replies.add(text=_get_fact("history"))


@simplebot.command
def factTrivia(payload: str, replies: Replies) -> None:
    """Get a random fact from the "trivia" category."""
    replies.add(text=_get_fact("trivia"))


@simplebot.command
def factSpooky(payload: str, replies: Replies) -> None:
    """Get a random fact from the "spooky" category."""
    replies.add(text=_get_fact("spooky"))


@simplebot.command
def factFood(payload: str, replies: Replies) -> None:
    """Get a random fact from the "food" category."""
    replies.add(text=_get_fact("food"))


@simplebot.command
def factTech(payload: str, replies: Replies) -> None:
    """Get a random fact from the "technology" category."""
    replies.add(text=_get_fact("technology"))


@simplebot.command
def factNature(payload: str, replies: Replies) -> None:
    """Get a random fact from the "nature" category."""
    replies.add(text=_get_fact("nature"))


@simplebot.command
def factAnimals(payload: str, replies: Replies) -> None:
    """Get a random fact from the "animals" category."""
    replies.add(text=_get_fact("animals"))


@simplebot.command
def factCelebrities(payload: str, replies: Replies) -> None:
    """Get a random fact from the "celebrities" category."""
    replies.add(text=_get_fact("celebrities"))


@simplebot.command
def factMovies(payload: str, replies: Replies) -> None:
    """Get a random fact from the "movies" category."""
    replies.add(text=_get_fact("movies"))


@simplebot.command
def factUniverse(payload: str, replies: Replies) -> None:
    """Get a random fact from the "universe" category."""
    replies.add(text=_get_fact("universe"))


@simplebot.command
def factWorld(payload: str, replies: Replies) -> None:
    """Get a random fact from the "world" category."""
    replies.add(text=_get_fact("world"))


@simplebot.command
def factKids(payload: str, replies: Replies) -> None:
    """Get a random fact from the "kids" category."""
    replies.add(text=_get_fact("kids"))


@simplebot.command
def factBusiness(payload: str, replies: Replies) -> None:
    """Get a random fact from the "business" category."""
    replies.add(text=_get_fact("business"))


@simplebot.command
def factUS(payload: str, replies: Replies) -> None:
    """Get a random fact from the "united-states" category."""
    replies.add(text=_get_fact("united-states"))


@simplebot.command
def factLanguage(payload: str, replies: Replies) -> None:
    """Get a random fact from the "language" category."""
    replies.add(text=_get_fact("language"))


@simplebot.command
def factInternet(payload: str, replies: Replies) -> None:
    """Get a random fact from the "internet" category."""
    replies.add(text=_get_fact("internet"))


def _get_fact(category: str = None) -> str:
    if category is None:
        with requests.get("https://dailyfacts.org/", headers=HEADERS) as resp:
            resp.raise_for_status()
            soup = bs4.BeautifulSoup(resp.text, "html.parser")
        url = soup.find("a", class_="nav-link", text="Random Fact")["href"]
    else:
        url = "https://dailyfacts.org/" + category

    with requests.get(url, headers=HEADERS) as resp:
        resp.raise_for_status()
        soup = bs4.BeautifulSoup(resp.text, "html.parser")
    fact = soup.find(class_="fact-content").text.strip()
    if not category:
        category = soup.find(class_="fact-categories").a.text.strip().lower()
    return "{}\n\n#{} #Fact".format(
        fact, "".join(map(str.capitalize, category.split("-")))
    )


class TestPlugin:
    def test_fact(self, mocker, lp):
        msg = mocker.get_one_reply("/fact")
        assert "#Fact" in msg.text

    def test_factOfTheDay(self, mocker, lp):
        msg = mocker.get_one_reply("/factOfTheDay")
        assert "#Fact" in msg.text

    def test_category(self, mocker, lp):
        msg = mocker.get_one_reply("/factGeneral")
        assert "#General" in msg.text
