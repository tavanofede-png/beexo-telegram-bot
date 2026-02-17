"""
Tests para ai_chat.py — detección de monedas, preguntas de precio, y web search.
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "beexo-telegram-bot"))

os.environ.setdefault("TELEGRAM_BOT_TOKEN", "test:token")
os.environ.setdefault("TARGET_CHAT_IDS", "123")
os.environ.setdefault("GROQ_API_KEY", "test_key")

from ai_chat import _detect_coins, _is_price_question, _needs_web_search


class TestDetectCoins:
    """Tests para detección de criptomonedas en texto."""

    def test_detects_btc(self):
        coins = _detect_coins("cuánto vale btc?")
        assert "bitcoin" in coins

    def test_detects_ethereum(self):
        coins = _detect_coins("qué pasa con ethereum hoy?")
        assert "ethereum" in coins

    def test_detects_multiple(self):
        coins = _detect_coins("precio de btc eth y sol")
        assert "bitcoin" in coins
        assert "ethereum" in coins
        assert "solana" in coins

    def test_no_coins(self):
        coins = _detect_coins("hola cómo estás?")
        assert len(coins) == 0

    def test_alias_doge(self):
        coins = _detect_coins("doge subió?")
        assert "dogecoin" in coins

    def test_no_duplicates(self):
        coins = _detect_coins("bitcoin btc bitcoin")
        assert coins.count("bitcoin") == 1


class TestIsPriceQuestion:
    """Tests para detección de preguntas de precio."""

    def test_precio(self):
        assert _is_price_question("cuál es el precio de btc?") is True

    def test_cuanto_vale(self):
        assert _is_price_question("cuánto vale ethereum?") is True

    def test_subio(self):
        assert _is_price_question("subió bitcoin?") is True

    def test_not_price(self):
        assert _is_price_question("qué es DeFi?") is False

    def test_market_cap(self):
        assert _is_price_question("market cap de solana") is True


class TestNeedsWebSearch:
    """Tests para detección de necesidad de búsqueda web."""

    def test_question_mark(self):
        assert _needs_web_search("quién es Satoshi Nakamoto?") is True

    def test_que_es(self):
        assert _needs_web_search("que es una DAO") is True

    def test_noticias(self):
        assert _needs_web_search("noticias de bitcoin hoy") is True

    def test_greeting_no_search(self):
        assert _needs_web_search("hola a todos") is False

    def test_short_text_no_search(self):
        assert _needs_web_search("hola") is False

    def test_gracias_no_search(self):
        assert _needs_web_search("gracias por la info") is False

    def test_diferencia_entre(self):
        assert _needs_web_search("diferencia entre PoW y PoS") is True

    def test_como_funciona(self):
        assert _needs_web_search("cómo funciona staking") is True
