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

SIGNALS_ALERT = (
    "🚫 *ALERTA ANTI-SPAM*\n\n"
    "• Están prohibidas las invitaciones a canales VIP o de señales.\n"
    "• No confíes en 'bots de trading' ni rendimientos mágicos.\n"
    "• Te recordamos que compartir enlaces no solicitados puede ser motivo de baneo.\n"
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
    "admin", "administrador", "moderador", "soporte oficial",
    "atención al cliente", "customer service",
    # Scams clásicos
    "validar wallet", "verificar wallet", "sincronizar", "sync",
    "conectar wallet", "connect wallet", "migrar", "migrate",
    "actualizar wallet", "upgrade", "wallet connect", "dapp",
    "nodo", "node", "web3", "vincular bimetálica", "vincular wallet",
    # Regalos / airdrops falsos
    "airdrop", "claim", "regalo", "giveaway", "sorteo",
    "token gratis", "gratis", "free", "whitelist", "bonus", "reward",
    # Inversión fraudulenta
    "inversión garantizada", "rendimiento garantizado", "duplicar",
    "enviar para recibir", "ganancia segura", "100% profit",
    "doblar tu inversión", "doblamos tus cryptos",
    # Usuario vulnerable
    "me hackearon", "hackeado", "me robaron", "robaron mis fondos",
    "perdí mis fondos", "no puedo acceder", "fondos bloqueados",
    "desbloquear", "congelaron", "frozen", "revertir transacción",
    "recuperar fondos", "cuenta suspendida", "actualización de seguridad",
    "bug", "problema", "error", "falla", "ayuda con",
    # Phishing
    "ingresá tu", "ingresa tu", "completar datos", "iniciar sesión",
    "ingresa tu frase", "login",
]

KEYWORDS_SIGNALS = [
    # Palabras clave de grupos de señales
    "canal de señales", "grupo de señales", "señales vip", "grupo vip",
    "bot de trading", "trading bot", "rentabilidad diaria", "rendimiento diario",
    "multiplica tu dinero", "ganancias aseguradas", "ganancias diarias",
    "pump signal", "unite a mi canal", "únete a mi canal", "unite al canal",
    "rentabilidad asegurada", "roi garantizado", "inversión segura",
    "link en mi bio", "sumate a mi equipo", "gana dinero desde tu celular",
    "libertad financiera", "deja que el bot trabaje por ti"
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
    ("📊 ¿Cómo ves el mercado hoy?", ["Bullish 🚀", "Neutral 😐", "Bearish 🐻", "Solo observo 👀"]),
    ("📊 ¿Qué querés más en la comunidad?", ["Trivias", "Noticias", "Tutoriales", "AMAs"]),
    ("📊 ¿Cuál es tu estrategia principal en crypto?", ["HODL a largo plazo 💎🙌", "Trading diario 📉📈", "Swing trading 🏄‍♂️", "Defi farming 🚜"]),
    ("📊 ¿Qué criptomoneda tiene más futuro para vos (además de BTC/ETH)?", ["Solana (SOL)", "Cardano (ADA)", "Polkadot (DOT)", "Otra (decilo en el chat)"]),
    ("📊 ¿Cuántas veces al día revisás tu portfolio?", ["1 vez", "2 a 5 veces", "Más de 5 veces 🥵", "Trato de no mirar 🙈"]),
    ("📊 ¿Mantenés tus cryptos en exchanges o en billeteras propias?", ["Todo en exchange 🏦", "Todo en hardware wallet 🔐", "Mitad y mitad ⚖️", "Hot wallets (MetaMask, etc) 🦊"]),
    ("📊 ¿Cuál fue tu primer criptomoneda?", ["Bitcoin (BTC) ₿", "Ethereum (ETH) ⟠", "Dogecoin u otra meme 🐕", "Otra"]),
    ("📊 ¿Qué opinas de las memecoins?", ["Son divertidas y dejan plata 🤑", "Son una estafa 🚩", "Indiferente 🤷‍♂️", "Solo meto lo que puedo perder 🎲"]),
    ("📊 ¿Cómo te informas sobre crypto?", ["Twitter/X 🐦", "Youtube 📺", "Telegram/Discord 💬", "Leyendo whitepapers 🤓"]),
    ("📊 ¿Qué narrativa crypto te interesa más hoy?", ["Inteligencia Artificial (AI) 🤖", "Real World Assets (RWA) 🏢", "Gaming / Web3 🎮", "DePIN 📡"]),
    ("📊 ¿Usaste alguna vez un DEX (Exchange Descentralizado)?", ["Sí, todo el tiempo 🔄", "Sí, un par de veces 🤔", "No, prefiero los CEX 🏦", "No sé qué es eso 🤨"]),
    ("📊 ¿Creés que Bitcoin superará los 150k este ciclo?", ["Seguro que sí 🚀", "Tal vez, pero con altibajos 🎢", "No creo 🐻", "Me da igual, yo tradeo 🤝"]),
    ("📊 ¿Te interesa participar en airdrops?", ["Sí, cazo todos los airdrops 🪂", "Solo los más seguros 🛡️", "No, mucho trabajo y riesgo 😴", "Airdrop? Qué es eso? 🧐"]),
    ("📊 ¿Has sido víctima de alguna estafa en crypto?", ["Nunca (toco madera) 🪵", "Sí, phishing/scam 🎣", "Sí, rug pull de un proyecto 📉", "Casi, pero me di cuenta a tiempo 🕵️‍♂️"]),
    ("📊 ¿Qué red blockchain usás más (fuera de Ethereum y Bitcoin)?", ["Solana", "Polygon / Arbitrum", "Binance Smart Chain", "Otras (Avalanche, Cosmos, etc)"]),
    ("📊 Si tuvieras que explicarle crypto a un familiar, ¿Qué le dirías?", ["Que es el futuro del dinero 🔮", "Que es como invertir en acciones riesgosas 📉", "Le diría que no se meta todavía 🛑", "Trato de no hablarles del tema 🤐"]),
    ("📊 ¿Qué opinas de los NFTs?", ["Tienen mucho potencial futuro 🖼️", "Son pura especulación 🫧", "Ya pasaron de moda 📉", "Tengo un par guardados por las dudas 📦"]),
    ("📊 ¿Usas hardware wallets (Ledger, Trezor)?", ["Sí, es fundamental 🔒", "No, uso hot wallets (Metamask) 🦊", "Dejo todo en exchanges 🏦", "Planeo comprar una pronto 🛒"]),
    ("📊 ¿Qué te parece la regulación crypto?", ["Es necesaria para masificar ⚖️", "Va en contra de la esencia de blockchain 🚫", "Me da igual 🤷‍♂️", "Depende qué regulen 🧐"]),
    ("📊 El mercado cae un 20% en un día. ¿Qué hacés?", ["Compro el dip 🛒", "Vendo por pánico (Panic sell) 😱", "HODL, ni toco 🗿", "Me voy a llorar al rincón 😭"]),
    ("📊 ¿Invertís en algo más aparte de criptomonedas?", ["Sí, acciones/cedears 📈", "Sí, dólares/plazo fijo 💵", "Sí, en mi propio negocio 💼", "No, 100% cripto 🚀"]),
    ("📊 ¿Preferís Proof of Work (PoW) o Proof of Stake (PoS)?", ["Proof of Work (Seguridad) ⛏️", "Proof of Stake (Velocidad/Eco) 🌱", "No me importa mientras suba 📈", "Una mezcla de ambos ⚖️"]),
    ("📊 ¿Cuál crees que es la mayor barrera para la adopción masiva?", ["Falta de educación 📚", "Riesgo de estafas/hacks ⚠️", "Complejidad técnica ⚙️", "Falta de regulación clara ⚖️"]),
    ("📊 ¿A qué edad compraste tu primer crypto?", ["Menos de 18 🧒", "Entre 18 y 25 👱‍♂️", "Entre 26 y 35 🧔", "Más de 35 🧙‍♂️"]),
    ("📊 ¿Qué porcentaje de tus ahorros está en cripto?", ["Menos del 10% 🐣", "Entre 10% y 40% 🐥", "Entre 40% y 80% 🦅", "Casi todo, all-in 🔥"]),
    ("📊 ¿Usas la red Lightning Network de Bitcoin?", ["Sí, para micropagos ⚡", "Sé qué es pero no la usé 🧠", "Prefiero otras redes más rápidas 🏎️", "No sé qué es 🤔"]),
    ("📊 ¿Cuál sería tu objetivo financiero con cripto?", ["Comprar una casa 🏠", "Llegar a fin de mes / Ahorro base 💼", "Independencia financiera (Jubilarme joven) 🏝️", "Solo es un hobby/juego 🎮"]),
    ("📊 ¿Has farmeado liquidez en DeFi (Yield Farming)?", ["Sí, sigo farmeando 🚜", "Lo hice en el pasado, ya no 🔙", "No, muy riesgoso/complejo 😰", "¿DeFi qué? 🤷‍♂️"]),
    ("📊 ¿Confías en las stablecoins algorítmicas (tipo DAI)?", ["Totalmente 🤝", "Tengo mis dudas (ej. UST) 🤨", "Prefiero USDT/USDC (respaldadas fíat) 💵", "No uso stablecoins 🚫"]),
    ("📊 ¿Crees que las CBDCs (monedas digitales de bancos centrales) son buenas?", ["Sí, ayudarán a la digitalización 🏦", "No, son la peor herramienta de control 👁️", "Inevitable, pero preocupante ⏳", "No sigo ese tema 📰"]),
    ("📊 Cuando el mercado está aburrido (lateraliza), ¿Qué hacés?", ["Estudio nuevos proyectos 📚", "Desconecto y hago otras cosas 🧘‍♂️", "Hago trading de rango corto ⚖️", "Sigo abriendo los charts por inercia 🧟‍♂️"]),
    ("📊 ¿Recomendarías Beexo a tus amigos/familia?", ["¡Por supuesto, siempre lo hago! 🗣️", "Sí, a los que les interesa cripto 🤝", "Todavía no, pero tal vez pronto 🤔", "No, prefiero mantenerlo para mí 🤫"]),
    ("📊 ¿Alguna vez perdiste la clave/seedphrase de tu wallet?", ["Sí, y perdí todo 😭", "Sí, pero pude recuperarla de suerte 😅", "Nunca, soy muy cuidadoso 🛡️", "No, pero tengo miedo de que me pase 😰"]),
    ("📊 ¿Has comprado bienes o servicios pagando directo con cripto?", ["Sí, varias veces 🛒", "Alguna que otra p2p 🤝", "Nunca, solo las holdeó 💎", "Me gustaría poder hacerlo más seguido 🛍️"]),
    ("📊 ¿Te interesa el desarrollo de smart contracts y programación web3?", ["Sí, estoy aprendiendo/soy dev 👨‍💻", "Me gustaría, pero parece difícil 🤯", "No, prefiero solo invertir/tradear 📈", "No es lo mío 🙅‍♂️"]),
    ("📊 En un Bear Market profundo (todo rojo por meses), tu reacción es:", ["Depresión y borré las apps 📉", "Acumulación silenciosa 🛒", "Aburrimiento total 🥱", "Tratar de hacer short-selling 🐻"]),
    ("📊 ¿Qué pensás de los influenciadores / 'crypto-bros' de Youtube?", ["Aportan valor y educación 🎓", "La mayoría solo vende humo o cursos 💨", "Los miro por entretenimiento 🍿", "Los ignoro por completo 🚫"]),
    ("📊 ¿Tenés alarmas de precios configuradas en el celular?", ["Sí, para todas mis monedas 🚨", "Solo para Bitcoin/Ethereum 🔔", "No, me genera mucha ansiedad 😥", "Las tenía y las saqué 🔕"]),
    ("📊 ¿Dejarías tu trabajo si ganas x10/x100 en un token?", ["Inmediatamente 🚪🏃‍♂️", "No, pero trabajaría más relajado 🏖️", "Lo pensaría, depende del monto final 💰", "No, me gusta lo que hago 💼"]),
    ("📊 ¿Cuál consideras tu peor error en cripto hasta ahora?", ["Comprar en FOMO arriba de todo 📈", "Vender en pánico abajo 📉", "Entrar en una estafa / shitcoin 🚩", "No haber comprado antes ⏰"]),
    ("📊 Si hoy te regalamos $1000 USD, ¿Qué hacés?", ["Compro Bitcoin ₿", "Compro altcoins para más riesgo 🚀", "Los dejo en stablecoins para hacer tasa 💵", "Saco la plata para gastos de la vida real 🏠"]),
    ("📊 ¿Te interesan los airdrops en testnets (redes de prueba gratuitas)?", ["Sí, es plata gratis sin riesgo 🧪", "A veces, si el proyecto promete mucho 🔭", "No, pierdo mucho tiempo ⏳", "No entiendo cómo funcionan 🤯"]),
    ("📊 ¿Te parece que Ethereum está perdiendo terreno frente a Solana u otros?", ["Sí, las comisiones altas lo están hundiendo 🐢", "No, ETH sigue siendo el rey de los smart contracts 👑", "Están empate, cada uno tiene su público ⚖️", "Falta mucho para ver quién gana ⏱️"]),
    ("📊 ¿Preferís análisis técnico (gráficos) o análisis fundamental (proyecto/equipo)?", ["100% Análisis Técnico 📊", "100% Fundamental 📖", "Uso una combinación de los dos 🧩", "Solo sigo noticias e instinto 📡"]),
    ("📊 Tus contraseñas para los exchanges, ¿son seguras?", ["Tengo 2FA y pass manager 🛡️", "Uso una contraseña segura pero la misma en varios 🔒", "Tengo contraseñas medio débiles 😬", "Las tengo en un papelito bajo el teclado 📝"]),
    ("📊 ¿Crees que la inteligencia artificial va a impactar fuerte en el trading cripto?", ["Ya lo está haciendo (bots, análisis) 🤖", "Va a cambiar el juego por completo en un futuro 🌍", "Es solo humo por ahora 💨", "No creo que afecte demasiado 🤷‍♂️"]),
    ("📊 Cuando comprás una cripto, ¿te fijás primero en el Market Cap o en el precio por token?", ["Market Cap siemper 📊", "Precio por token (psicología) 🪙", "Miro las dos cosas 🧐", "No me fijo, solo compro 🛒"]),
    ("📊 Si descubren un fallo grave en Bitcoin y su precio cae a 0 por un día. ¿Qué hacés?", ["Entro en pánico y acepto la pérdida 💀", "Espero a ver qué dice la comunidad técnica 🧑‍💻", "Compro con todo lo que tengo asumiendo que lo arreglan 🛍️", "Me río por no llorar 😹"]),
    ("📊 ¿Creés que cripto será la moneda oficial del mundo algún día?", ["Sí, Bitcoin será el estándar global 🌍", "Será una alternativa muy importante pero no la única ⚖️", "No, los gobiernos nunca lo van a permitir 🏛️", "Solo se usará para casos muy específicos 🔬"]),
    ("📊 ¿Confiás más en la comunidad cripto hispana o en la de habla inglesa?", ["Inglesa, hay mejor info técnica 🇺🇸", "Hispana, nos ayudamos más 🇦🇷🇪🇸", "Uso ambas por igual 🌐", "No confío en nadie en cripto 🕵️‍♂️"]),
]

# ═══════════════════════════════════════════════════════════════
# UTILIDADES
# ═══════════════════════════════════════════════════════════════

def contains_wallet_keywords(text: str) -> bool:
    """Devuelve True si el texto contiene keywords relacionadas con wallets/scams."""
    t = (text or "").lower()
    return any(k in t for k in KEYWORDS_WALLET)

def contains_signals_keywords(text: str) -> bool:
    """Devuelve True si el texto contiene keywords relacionadas con canales de señales/spam."""
    t = (text or "").lower()
    return any(k in t for k in KEYWORDS_SIGNALS)
