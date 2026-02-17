"""
Tests para content.py — detección de keywords anti-scam.
"""

import sys
import os

# Agregar el directorio del proyecto al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "beexo-telegram-bot"))

# Setear variables de entorno mínimas antes de importar
os.environ.setdefault("TELEGRAM_BOT_TOKEN", "test:token")
os.environ.setdefault("TARGET_CHAT_IDS", "123")
os.environ.setdefault("GROQ_API_KEY", "test_key")
os.environ.setdefault("GEMINI_API_KEY", "test_key")

from content import contains_wallet_keywords


class TestContainsWalletKeywords:
    """Tests para la función contains_wallet_keywords."""

    def test_detects_seed_phrase(self):
        assert contains_wallet_keywords("me pidieron mi seed phrase") is True

    def test_detects_12_palabras(self):
        assert contains_wallet_keywords("ingresá tus 12 palabras") is True

    def test_detects_private_key(self):
        assert contains_wallet_keywords("dame tu private key") is True

    def test_detects_wallet(self):
        assert contains_wallet_keywords("conectar wallet") is True

    def test_detects_airdrop(self):
        assert contains_wallet_keywords("reclamá tu airdrop gratis") is True

    def test_detects_dm(self):
        assert contains_wallet_keywords("me escribieron por privado") is True

    def test_detects_soporte(self):
        assert contains_wallet_keywords("el soporte técnico me contactó") is True

    def test_detects_hackeado(self):
        assert contains_wallet_keywords("me hackearon la cuenta") is True

    def test_detects_formulario(self):
        assert contains_wallet_keywords("completá este formulario") is True

    def test_ignores_normal_text(self):
        assert contains_wallet_keywords("qué es DeFi?") is False

    def test_ignores_price_question(self):
        assert contains_wallet_keywords("cuánto vale bitcoin hoy?") is False

    def test_ignores_greeting(self):
        assert contains_wallet_keywords("hola a todos, buen día") is False

    def test_ignores_general_crypto(self):
        assert contains_wallet_keywords("ethereum subió un 5% hoy") is False

    def test_handles_none(self):
        assert contains_wallet_keywords(None) is False

    def test_handles_empty(self):
        assert contains_wallet_keywords("") is False

    def test_case_insensitive(self):
        assert contains_wallet_keywords("SEED PHRASE") is True
        assert contains_wallet_keywords("Conectar Wallet") is True
