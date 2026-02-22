"""
chat_roles.py — Routing de chats por rol en BeeXy.

Define qué grupos reciben qué tipo de contenido:
  • community_chats()  → noticias, saludos, cripto, trivias
  • memes_chat()       → memes (automáticos y comando /meme)

Configurar en .env:
    COMMUNITY_CHAT_IDS=-100111111,-100222222
    MEMES_CHAT_ID=-100333333
"""

from config import (
    TARGET_CHAT_IDS,
    COMMUNITY_CHAT_IDS,
    MEMES_CHAT_ID,
    logger,
)


def community_chats() -> list[int]:
    """
    Devuelve la lista de chat IDs que reciben contenido general
    (noticias, saludos diarios, resumen cripto, trivias, etc.).

    Si COMMUNITY_CHAT_IDS no está definido, cae al viejo TARGET_CHAT_IDS
    como fallback de compatibilidad.
    """
    if COMMUNITY_CHAT_IDS:
        return COMMUNITY_CHAT_IDS
    logger.warning(
        "⚠️  COMMUNITY_CHAT_IDS no configurado — usando TARGET_CHAT_IDS como fallback"
    )
    return TARGET_CHAT_IDS


def memes_chat() -> list[int]:
    """
    Devuelve la lista con el chat ID del grupo de memes.

    Si MEMES_CHAT_ID no está definido, cae a community_chats()
    para no silenciar los memes en producción.
    """
    if MEMES_CHAT_ID is not None:
        return [MEMES_CHAT_ID]
    logger.warning(
        "⚠️  MEMES_CHAT_ID no configurado — enviando memes a community_chats()"
    )
    return community_chats()
