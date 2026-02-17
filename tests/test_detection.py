"""
Tests para image_tools.py — detección de pedidos de imagen.
Versión pytest de test_detection.py original.
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "beexo-telegram-bot"))

os.environ.setdefault("TELEGRAM_BOT_TOKEN", "test:token")
os.environ.setdefault("TARGET_CHAT_IDS", "123")
os.environ.setdefault("GROQ_API_KEY", "test_key")

from image_tools import detect_image_request


class TestDetectImageRequestNone:
    """Textos que NO deben detectarse como pedido de imagen."""

    def test_busca_en_x(self):
        assert detect_image_request("busca en x cuando sera la proxima beexo radio") is None

    def test_busca_en_google(self):
        assert detect_image_request("busca en google que es bitcoin") is None

    def test_busca_informacion(self):
        assert detect_image_request("busca informacion sobre ethereum") is None

    def test_mostra_precio(self):
        assert detect_image_request("mostra el precio de btc") is None

    def test_pasa_link(self):
        assert detect_image_request("pasa el link del sitio") is None

    def test_manda_saludo(self):
        assert detect_image_request("manda un saludo al grupo") is None

    def test_haceme_favor(self):
        assert detect_image_request("haceme un favor") is None

    def test_poneme_al_dia(self):
        assert detect_image_request("poneme al dia con las noticias") is None

    def test_quiero_ver_precio(self):
        assert detect_image_request("quiero ver el precio de btc") is None


class TestDetectImageRequestSearch:
    """Textos que deben detectarse como búsqueda de imagen."""

    def test_buscame_foto(self):
        result = detect_image_request("buscame una foto de cr7")
        assert result is not None
        assert result[0] == "search"

    def test_buscame_imagen(self):
        result = detect_image_request("buscame una imagen de bitcoin")
        assert result is not None
        assert result[0] == "search"

    def test_mostrame_foto(self):
        result = detect_image_request("mostrame una foto de un gato")
        assert result is not None
        assert result[0] == "search"

    def test_mandame_imagen(self):
        result = detect_image_request("mandame una imagen de ethereum")
        assert result is not None
        assert result[0] == "search"

    def test_quiero_imagen(self):
        result = detect_image_request("quiero una imagen de la luna")
        assert result is not None
        assert result[0] == "search"

    def test_foto_solo(self):
        result = detect_image_request("foto de un atardecer")
        assert result is not None
        assert result[0] == "search"


class TestDetectImageRequestGenerate:
    """Textos que deben detectarse como generación de imagen."""

    def test_generame(self):
        result = detect_image_request("generame un dinosaurio minando btc")
        assert result is not None
        assert result[0] == "generate"

    def test_dibuja(self):
        result = detect_image_request("dibuja un perro astronauta")
        assert result is not None
        assert result[0] == "generate"

    def test_genera(self):
        result = detect_image_request("genera una vaca en la luna")
        assert result is not None
        assert result[0] == "generate"

    def test_ilustrame(self):
        result = detect_image_request("ilustrame un dragon")
        assert result is not None
        assert result[0] == "generate"

    def test_disenñame(self):
        result = detect_image_request("diseñame un logo cripto")
        assert result is not None
        assert result[0] == "generate"
