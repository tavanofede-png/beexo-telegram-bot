"""
Contenido estático de BeeXy: mensajes, keywords, reacciones y polls.
"""

# ═══════════════════════════════════════════════════════════════
# MENSAJES DIARIOS
# ═══════════════════════════════════════════════════════════════

GOOD_MORNING = [
    "☀️ *Buen día Beexers!* Hoy aprendé 1 concepto nuevo de cripto y compartilo 👇",
    "🚀 *Buen día!* Paciencia + criterio > hype.",
    "📈 *Buen día comunidad!* Hoy gana el que gestiona riesgo.",
    "🔥 *Buen día!* Mini desafío: explicá blockchain en 1 frase.",
    "🧠 *Buen día!* Recordá: DYOR antes de invertir.",
]

GOOD_NIGHT = [
    "🌙 *Buenas noches Beexo.* Sobrevivir en cripto ya es ganar.",
    "✨ *Buenas noches.* Gestión de riesgo > euforia.",
    "🛌 *Buenas noches!* Nunca compartas tu seed phrase.",
    "🌑 *Buenas noches comunidad.* ¿Qué aprendiste hoy?",
    "🌙 *Buenas noches.* Si hoy fue rojo, fue información.",
]

# ═══════════════════════════════════════════════════════════════
# ANTI-SCAM
# ═══════════════════════════════════════════════════════════════

SCAM_ALERT = (
    "⚠️ *ALERTA ANTI-SCAM*\n\n"
    "• Nadie te pedirá tus *12 palabras / seed phrase*\n"
    "• Ningún admin te escribe por privado primero\n"
    "• Pedí ayuda solo en el grupo\n"
)

KEYWORDS_WALLET = [
    # Seed / claves
    "seed", "seed phrase", "12 palabras", "24 palabras", "frase semilla",
    "frase de recuperación", "recovery phrase", "private key", "clave privada",
    "mnemonic", "passphrase",
    # Wallet / billetera
    "wallet", "billetera", "recovery", "restaurar wallet",
    # Contacto sospechoso
    "me escribieron", "me contactaron", "me mandó mensaje",
    "dm", "privado", "por privado", "mensaje privado", "inbox",
    # Soporte falso
    "soporte", "soporte técnico", "support", "ayuda", "help",
    "admin", "administrador", "moderador",
    # Scams clásicos
    "validar wallet", "verificar wallet", "sincronizar", "sync",
    "conectar wallet", "connect wallet", "migrar", "migrate",
    "actualizar wallet", "upgrade",
    # Regalos / airdrops falsos
    "airdrop", "claim", "regalo", "giveaway", "sorteo",
    "token gratis", "gratis", "free", "whitelist",
    # Inversión fraudulenta
    "inversión garantizada", "rendimiento garantizado", "duplicar",
    "enviar para recibir", "ganancia segura", "100% profit",
    # Usuario vulnerable
    "me hackearon", "hackeado", "me robaron", "robaron mis fondos",
    "perdí mis fondos", "no puedo acceder", "fondos bloqueados",
    "desbloquear", "congelaron", "frozen",
    # Phishing
    "formulario", "form", "kyc", "verificar identidad",
    "ingresá tu", "ingresa tu", "completar datos",
]

# ═══════════════════════════════════════════════════════════════
# BIENVENIDA
# ═══════════════════════════════════════════════════════════════

WELCOME_MESSAGES = [
    "🐝 *¡Bienvenid@ {name}!*\n\nSoy *BeeXy*, el bot de la comunidad Beexo.\n\n"
    "📌 Regla #1: nunca compartas tu seed phrase\n"
    "🤖 Consultame lo que necesites: `BeeXy ¿qué es DeFi?`\n"
    "🎨 También genero imágenes: `BeeXy dibujame un gato astronauta`",
    "👋 *¡Hola {name}!* Bienvenid@ a la comunidad Beexo 🐝\n\n"
    "Acá aprendemos sobre cripto y nos cuidamos entre todos.\n"
    "Escribí `/help` para ver todo lo que puedo hacer.",
    "🎉 *¡{name} se sumó a Beexo!*\n\n"
    "Bienvenid@ a la mejor comunidad cripto de habla hispana.\n"
    "Nunca respondas DMs de \"soporte\". Toda ayuda acá en el grupo. 🛡",
]

# ═══════════════════════════════════════════════════════════════
# REACCIONES EMOCIONALES
# ═══════════════════════════════════════════════════════════════

EMOTION_REACTIONS: dict[str, dict] = {
    "pump": {
        "keywords": ["pump", "pumpeando", "bullish", "bull run",
                     "todo verde", "subiendo fuerte", "para arriba"],
        "responses": [
            "🚀🟢 ¡PUMP MODE ACTIVADO! A la luna vamos 🌕",
            "📈💚 ¡Verde que te quiero verde! Los toros mandan 🐂",
            "🔥 ¡Despegamos! Abróchense los cinturones 🚀",
        ],
        "gif_query": "crypto pump rocket celebration",
    },
    "dump": {
        "keywords": ["dump", "crash", "se desplomó", "todo rojo", "cayó fuerte",
                     "bearish", "liquidado", "liquidaron", "dumpeando"],
        "responses": [
            "📉🔴 F en el chat... Resistamos 💀",
            "🩸 Día rojo. Recordá: el que no vende no pierde",
            "🐻 Los osos atacaron hoy. Paciencia 💪",
        ],
        "gif_query": "crypto crash panic oh no",
    },
    "hodl": {
        "keywords": ["hodl", "diamond hands", "manos de diamante", "no vendo",
                     "aguantamos", "hold fuerte"],
        "responses": [
            "💎🙌 ¡HODL GANG! Las manos de diamante nunca fallan",
            "🗿 Aguantamos como campeones. HODL forever.",
            "💪 El que aguanta, gana. No suelten.",
        ],
        "gif_query": "diamond hands hodl strong",
    },
    "fomo": {
        "keywords": ["fomo", "all in", "compro ya", "yolo", "me lo pierdo"],
        "responses": [
            "⚠️ ¡Cuidado con el FOMO! DYOR siempre 🧠",
            "🎰 FOMO detectado... Respirá hondo primero",
            "💡 No comprés por FOMO, comprá por convicción",
        ],
        "gif_query": "fomo panic buying hurry",
    },
    "moon": {
        "keywords": ["to the moon", "ath", "máximo histórico", "all time high",
                     "nuevo máximo", "mooning"],
        "responses": [
            "🌕 ¡TO THE MOOOON! 🚀🚀🚀",
            "🏔️ ¡Nuevo ATH! Esto es histórico 🎉",
            "🌙 ¡La luna queda chica! Sin frenos 🔥",
        ],
        "gif_query": "to the moon crypto celebration",
    },
}

# ═══════════════════════════════════════════════════════════════
# POLLS
# ═══════════════════════════════════════════════════════════════

POLLS = [
    ("📊 ¿Cómo ves el mercado hoy?", ["Bullish", "Neutral", "Bearish", "Solo observo"]),
    ("📊 ¿Qué querés más en la comunidad?", ["Trivias", "Noticias", "Tutoriales", "AMAs"]),
]

# ═══════════════════════════════════════════════════════════════
# UTILIDADES
# ═══════════════════════════════════════════════════════════════

def contains_wallet_keywords(text: str) -> bool:
    """Devuelve True si el texto contiene keywords relacionadas con wallets/scams."""
    t = (text or "").lower()
    return any(k in t for k in KEYWORDS_WALLET)
