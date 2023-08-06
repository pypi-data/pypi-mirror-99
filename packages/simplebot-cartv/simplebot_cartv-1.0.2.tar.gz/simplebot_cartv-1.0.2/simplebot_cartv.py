import requests
import simplebot
from simplebot.bot import Replies

__version__ = "1.0.2"
tv_emoji, cal_emoji, aster_emoji = "📺", "📆", "✳"
channels = {
    name: "http://eprog2.tvcdigital.cu/programacion/" + code
    for name, code in zip(
        (
            "Cubavisión",
            "Tele Rebelde",
            "Educativo",
            "Educativo 2",
            "Multivisión",
            "Clave",
            "Caribe",
            "Habana",
        ),
        (
            "5c096ea5bad1b202541503cf",
            "596c6d34769cf31454a473aa",
            "596c6d4f769cf31454a473ab",
            "596c8107670d001588a8bfc1",
            "597eed8948124617b0d8b23a",
            "5a6a056c6c40dd21604965fd",
            "5c5357124929db17b7429949",
            "5c42407f4fa5d131ce00f864",
        ),
    )
}


@simplebot.command
def cartv(replies: Replies) -> None:
    """Muestra la cartelera de todos los canales de la TV cubana."""
    replies.add(text="\n\n".join(_get_channel(chan) for chan in channels.keys()))


@simplebot.command
def cartvcv(replies: Replies) -> None:
    """Muestra la cartelera del canal Cubavisión."""
    replies.add(text=_get_channel("Cubavisión"))


@simplebot.command
def cartvtr(replies: Replies) -> None:
    """Muestra la cartelera del canal Tele Rebelde."""
    replies.add(text=_get_channel("Tele Rebelde"))


@simplebot.command
def cartved(replies: Replies) -> None:
    """Muestra la cartelera del canal Educativo."""
    replies.add(text=_get_channel("Educativo"))


@simplebot.command
def cartved2(replies: Replies) -> None:
    """Muestra la cartelera del canal Educativo 2."""
    replies.add(text=_get_channel("Educativo 2"))


@simplebot.command
def cartvmv(replies: Replies) -> None:
    """Muestra la cartelera del canal Multivisión."""
    replies.add(text=_get_channel("Multivisión"))


@simplebot.command
def cartvcl(replies: Replies) -> None:
    """Muestra la cartelera del canal Clave."""
    replies.add(text=_get_channel("Clave"))


@simplebot.command
def cartvca(replies: Replies) -> None:
    """Muestra la cartelera del canal Caribe."""
    replies.add(text=_get_channel("Caribe"))


@simplebot.command
def cartvha(replies: Replies) -> None:
    """Muestra la cartelera del canal Habana."""
    replies.add(text=_get_channel("Habana"))


def _get_channel(chan) -> str:
    with requests.get(channels[chan]) as req:
        req.raise_for_status()
        programs = req.json()

    text = "{} {}\n".format(tv_emoji, chan)
    date = None
    for prog in programs:
        if date != prog["fecha_inicial"]:
            date = prog["fecha_inicial"]
            text += "{} {}\n".format(cal_emoji, date)
        time = prog["hora_inicio"][:-3]
        title = " ".join(prog["titulo"].split())
        desc = " ".join(prog["descripcion"].split())
        trans = prog["transmision"].strip()
        text += "{} {} {}\n".format(
            aster_emoji, time, "/".join(e for e in (title, desc, trans) if e)
        )

    if not programs:
        text += "Cartelera no disponible."

    return text


class TestSendFile:
    def test_cartv(self, mocker, requests_mock) -> None:
        self._requests_mock(requests_mock)
        msg = mocker.get_one_reply("/cartv")
        assert msg.text

    def test_cartvcv(self, mocker, requests_mock) -> None:
        self._requests_mock(requests_mock)
        msg = mocker.get_one_reply("/cartvcv")
        assert msg.text

    def test_cartvtr(self, mocker, requests_mock) -> None:
        self._requests_mock(requests_mock)
        msg = mocker.get_one_reply("/cartvtr")
        assert msg.text

    def test_cartved(self, mocker, requests_mock) -> None:
        self._requests_mock(requests_mock)
        msg = mocker.get_one_reply("/cartved")
        assert msg.text

    def test_cartved2(self, mocker, requests_mock) -> None:
        self._requests_mock(requests_mock)
        msg = mocker.get_one_reply("/cartved2")
        assert msg.text

    def test_cartvmv(self, mocker, requests_mock) -> None:
        self._requests_mock(requests_mock)
        msg = mocker.get_one_reply("/cartvmv")
        assert msg.text

    def test_cartvcl(self, mocker, requests_mock) -> None:
        self._requests_mock(requests_mock)
        msg = mocker.get_one_reply("/cartvcl")
        assert msg.text

    def test_cartvca(self, mocker, requests_mock) -> None:
        self._requests_mock(requests_mock)
        msg = mocker.get_one_reply("/cartvca")
        assert msg.text

    def test_cartvha(self, mocker, requests_mock) -> None:
        self._requests_mock(requests_mock)
        msg = mocker.get_one_reply("/cartvha")
        assert msg.text

    def _requests_mock(self, requests_mock):
        data = {
            "Cubavisión": [
                {
                    "fecha_inicial": "2021-03-24",
                    "hora_inicio": "00:15:00",
                    "titulo": "Example program",
                    "descripcion": "Example description",
                    "transmision": "Estreno",
                }
            ],
        }
        data["Tele Rebelde"] = data["Cubavisión"]
        data["Educativo"] = data["Cubavisión"]
        data["Educativo 2"] = data["Cubavisión"]
        data["Multivisión"] = data["Cubavisión"]
        data["Clave"] = data["Cubavisión"]
        data["Caribe"] = data["Cubavisión"]
        data["Habana"] = data["Cubavisión"]
        for name, url in channels.items():
            requests_mock.get(url, json=data[name])
