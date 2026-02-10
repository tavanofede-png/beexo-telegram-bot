"""
Base de datos de 50+ trivias cripto para Beexo Wallet Bot.
Organizadas por categoría temática.
"""

TRIVIAS_DATA = [
    # ===========================================
    # BITCOIN HISTORY
    # ===========================================
    {
        "q": "¿En qué año se minó el primer bloque de Bitcoin?",
        "options": ["2007", "2008", "2009", "2010"],
        "correct": 2,
        "explain": "El bloque génesis fue minado el 3 de enero de 2009 por Satoshi Nakamoto."
    },
    {
        "q": "¿Cuántos BTC se pagaron por 2 pizzas en 2010?",
        "options": ["100 BTC", "1.000 BTC", "10.000 BTC", "50.000 BTC"],
        "correct": 2,
        "explain": "Laszlo Hanyecz pagó 10.000 BTC por dos pizzas el 22 de mayo de 2010."
    },
    {
        "q": "¿Cuál es el suministro máximo de Bitcoin?",
        "options": ["18 millones", "21 millones", "100 millones", "Ilimitado"],
        "correct": 1,
        "explain": "Solo existirán 21 millones de BTC. El último se minará alrededor de 2140."
    },
    {
        "q": "¿Con qué pseudónimo se conoce al creador de Bitcoin?",
        "options": ["Vitalik Buterin", "Satoshi Nakamoto", "Adam Back", "Nick Szabo"],
        "correct": 1,
        "explain": "Satoshi Nakamoto es el pseudónimo del creador (o creadores) de Bitcoin."
    },
    {
        "q": "¿Cada cuántos bloques ocurre el halving de Bitcoin?",
        "options": ["100.000", "210.000", "500.000", "1.000.000"],
        "correct": 1,
        "explain": "El halving reduce la recompensa a la mitad cada 210.000 bloques (~4 años)."
    },
    {
        "q": "¿Cuándo fue el último halving de Bitcoin?",
        "options": ["2020", "2022", "2024", "2023"],
        "correct": 2,
        "explain": "El halving más reciente fue en abril de 2024, reduciendo la recompensa a 3.125 BTC."
    },
    {
        "q": "¿Qué mensaje dejó Satoshi en el bloque génesis?",
        "options": [
            "Hello World",
            "The Times 03/Jan/2009 Chancellor on brink...",
            "Bitcoin is freedom",
            "In crypto we trust"
        ],
        "correct": 1,
        "explain": "Referencia a un titular del diario The Times sobre el rescate bancario de 2009."
    },
    {
        "q": "¿Qué país adoptó Bitcoin como moneda legal primero?",
        "options": ["Panamá", "Paraguay", "El Salvador", "Argentina"],
        "correct": 2,
        "explain": "El Salvador adoptó Bitcoin como moneda de curso legal en septiembre de 2021."
    },
    # ===========================================
    # BLOCKCHAIN TECHNOLOGY
    # ===========================================
    {
        "q": "¿Qué tipo de estructura de datos es una blockchain?",
        "options": [
            "Árbol binario",
            "Lista enlazada de bloques con hashes",
            "Base de datos SQL",
            "Archivo CSV"
        ],
        "correct": 1,
        "explain": "Cada bloque contiene el hash del anterior, formando una cadena inmutable."
    },
    {
        "q": "¿Qué significa Proof of Work (PoW)?",
        "options": [
            "Demostrar que trabajás 8 horas",
            "Resolver problemas criptográficos para validar bloques",
            "Verificar identidad con documento",
            "Hacer staking de monedas"
        ],
        "correct": 1,
        "explain": "Los mineros compiten resolviendo problemas matemáticos para agregar bloques."
    },
    {
        "q": "¿Qué es un nodo en una blockchain?",
        "options": [
            "Un tipo de criptomoneda",
            "Una PC que mantiene copia de la blockchain",
            "Un exchange descentralizado",
            "Un contrato inteligente"
        ],
        "correct": 1,
        "explain": "Los nodos validan transacciones y mantienen la red descentralizada."
    },
    {
        "q": "¿Cuántas confirmaciones se recomiendan para BTC?",
        "options": ["1", "3", "6", "12"],
        "correct": 2,
        "explain": "6 confirmaciones (~1 hora) se consideran suficientes para transacciones seguras."
    },
    {
        "q": "¿Qué es un smart contract?",
        "options": [
            "Un contrato legal firmado digitalmente",
            "Código autoejectable en blockchain",
            "Un acuerdo entre dos exchanges",
            "Un tipo de NFT"
        ],
        "correct": 1,
        "explain": "Los contratos inteligentes se ejecutan automáticamente según condiciones programadas."
    },
    {
        "q": "¿Qué blockchain introdujo los smart contracts?",
        "options": ["Bitcoin", "Cardano", "Ethereum", "Solana"],
        "correct": 2,
        "explain": "Ethereum, creada por Vitalik Buterin, fue la primera plataforma de smart contracts (2015)."
    },
    {
        "q": "¿Qué algoritmo de hash usa Bitcoin?",
        "options": ["MD5", "SHA-256", "SHA-512", "Keccak-256"],
        "correct": 1,
        "explain": "Bitcoin usa SHA-256 (Secure Hash Algorithm 256-bit) para su prueba de trabajo."
    },
    {
        "q": "¿Qué es una sidechain?",
        "options": [
            "Blockchain independiente conectada a la principal",
            "Una copia de seguridad de la blockchain",
            "Una cadena de bloques rota",
            "Un fork de Bitcoin"
        ],
        "correct": 0,
        "explain": "Las sidechains permiten transferir activos entre blockchains con interoperabilidad."
    },
    # ===========================================
    # ALTCOINS & TOKENS
    # ===========================================
    {
        "q": "¿Qué cripto pasó de PoW a PoS en 'The Merge'?",
        "options": ["Bitcoin", "Cardano", "Ethereum", "Polkadot"],
        "correct": 2,
        "explain": "Ethereum completó 'The Merge' en sept 2022, reduciendo consumo energético ~99%."
    },
    {
        "q": "¿Qué es un token ERC-20?",
        "options": [
            "Un token nativo de Bitcoin",
            "Un estándar de token en Ethereum",
            "Una stablecoin regulada",
            "Un NFT musical"
        ],
        "correct": 1,
        "explain": "ERC-20 es el estándar técnico para crear tokens fungibles en la red Ethereum."
    },
    {
        "q": "¿Cuál de estas NO es una stablecoin?",
        "options": ["USDT", "USDC", "DAI", "DOGE"],
        "correct": 3,
        "explain": "DOGE es una memecoin. USDT, USDC y DAI mantienen paridad con el dólar."
    },
    {
        "q": "¿Qué stablecoin algorítmica colapsó en mayo 2022?",
        "options": ["USDT", "DAI", "UST (Terra/Luna)", "USDC"],
        "correct": 2,
        "explain": "UST perdió paridad con el dólar, causando pérdidas de ~$40 mil millones."
    },
    {
        "q": "¿Cuál es el gas token de la red Ethereum?",
        "options": ["USDT", "ETH", "GAS", "GWEI"],
        "correct": 1,
        "explain": "ETH (Ether) se usa para pagar las fees de transacción (gas) en Ethereum."
    },
    {
        "q": "¿Qué red se destaca por PoH y transacciones baratas?",
        "options": ["Ethereum", "Bitcoin", "Solana", "Litecoin"],
        "correct": 2,
        "explain": "Solana usa Proof of History (PoH) + PoS para alta velocidad y bajo costo."
    },
    {
        "q": "¿Qué es un wrapped token como WBTC?",
        "options": [
            "Bitcoin envuelto en papel",
            "Representación de BTC en otra blockchain",
            "Un Bitcoin más seguro",
            "Un token de regalo"
        ],
        "correct": 1,
        "explain": "WBTC es BTC tokenizado en Ethereum, respaldado 1:1."
    },
    {
        "q": "¿Cuál fue la primera memecoin popular?",
        "options": ["SHIB", "PEPE", "DOGE", "FLOKI"],
        "correct": 2,
        "explain": "Dogecoin (DOGE) fue creada en 2013 como broma basada en el meme del perro Shiba Inu."
    },
    # ===========================================
    # DeFi
    # ===========================================
    {
        "q": "¿Qué significa DeFi?",
        "options": [
            "Digital Finance",
            "Decentralized Finance",
            "Defined Fiscal",
            "Deficit Financing"
        ],
        "correct": 1,
        "explain": "DeFi = Finanzas Descentralizadas: servicios financieros sin intermediarios."
    },
    {
        "q": "¿Qué es un liquidity pool?",
        "options": [
            "Una piscina de criptomonedas",
            "Fondos en un smart contract para facilitar trading",
            "Una cuenta de ahorro cripto",
            "Un tipo de wallet"
        ],
        "correct": 1,
        "explain": "Los liquidity pools permiten intercambios descentralizados sin order book."
    },
    {
        "q": "¿Qué es yield farming?",
        "options": [
            "Cultivar criptomonedas",
            "Obtener rendimiento proveyendo liquidez en DeFi",
            "Minar Bitcoin con paneles solares",
            "Comprar tierras virtuales"
        ],
        "correct": 1,
        "explain": "Yield farming busca maximizar rendimientos moviendo fondos entre protocolos DeFi."
    },
    {
        "q": "¿Qué es un DEX?",
        "options": [
            "Un exchange centralizado",
            "Un exchange descentralizado",
            "Un tipo de token",
            "Una blockchain privada"
        ],
        "correct": 1,
        "explain": "DEX (Decentralized Exchange) permite intercambiar tokens sin intermediarios. Ej: Uniswap."
    },
    {
        "q": "¿Qué riesgo tiene proveer liquidez en un AMM?",
        "options": [
            "Impermanent Loss",
            "Permanent Gain",
            "Doble ganancia",
            "Ningún riesgo"
        ],
        "correct": 0,
        "explain": "Impermanent Loss ocurre cuando el precio relativo de los tokens cambia."
    },
    {
        "q": "¿Qué es un flash loan?",
        "options": [
            "Un préstamo con garantía",
            "Préstamo instantáneo sin colateral devuelto en la misma tx",
            "Un préstamo a largo plazo",
            "Un préstamo entre amigos"
        ],
        "correct": 1,
        "explain": "Los flash loans se usan para arbitraje y liquidaciones en una sola transacción."
    },
    # ===========================================
    # SECURITY
    # ===========================================
    {
        "q": "¿Qué es una cold wallet?",
        "options": [
            "Una wallet en el Ártico",
            "Una wallet sin conexión a internet",
            "Una wallet gratuita",
            "Una wallet con poco saldo"
        ],
        "correct": 1,
        "explain": "Las cold wallets almacenan claves offline para máxima seguridad."
    },
    {
        "q": "¿Qué es un ataque del 51%?",
        "options": [
            "Cuando el 51% de wallets son hackeadas",
            "Cuando un grupo controla la mayoría del hashrate",
            "Cuando el precio cae 51%",
            "Cuando el 51% de nodos se desconectan"
        ],
        "correct": 1,
        "explain": "Con >50% del hashrate, un atacante podría revertir transacciones y hacer doble gasto."
    },
    {
        "q": "¿Qué es un rug pull?",
        "options": [
            "Un tirón de alfombra literal",
            "Desarrolladores roban fondos y abandonan el proyecto",
            "Un error técnico en la blockchain",
            "Una caída natural del mercado"
        ],
        "correct": 1,
        "explain": "En un rug pull, los creadores drenan la liquidez dejando tokens sin valor."
    },
    {
        "q": "¿Qué es phishing en el contexto cripto?",
        "options": [
            "Pescar con blockchain",
            "Sitios/mensajes falsos que roban credenciales",
            "Un método de minería",
            "Un tipo de staking"
        ],
        "correct": 1,
        "explain": "Los ataques de phishing imitan sitios legítimos para robar seeds y claves."
    },
    {
        "q": "¿Qué es una hardware wallet?",
        "options": [
            "Una app de celular",
            "Dispositivo físico que almacena claves offline",
            "Una computadora para minar",
            "Un pendrive cualquiera"
        ],
        "correct": 1,
        "explain": "Hardware wallets como Ledger o Trezor son la forma más segura de guardar cripto."
    },
    {
        "q": "¿Qué es SIM swapping?",
        "options": [
            "Cambiar de operador celular",
            "Clonar tu número para interceptar SMS de verificación",
            "Usar dos tarjetas SIM",
            "Un método de encriptación"
        ],
        "correct": 1,
        "explain": "Atacantes convencen al operador de transferir tu número para robar 2FA por SMS."
    },
    {
        "q": "¿Cuál es la forma más segura de 2FA?",
        "options": [
            "SMS",
            "Email",
            "App autenticadora (Google Authenticator)",
            "No usar 2FA"
        ],
        "correct": 2,
        "explain": "Las apps generan códigos localmente, más seguras que SMS (vulnerable a SIM swap)."
    },
    {
        "q": "¿Qué es una seed phrase?",
        "options": [
            "Contraseña del exchange",
            "Frase de 12/24 palabras que controla tus fondos",
            "PIN del teléfono",
            "Tu clave pública"
        ],
        "correct": 1,
        "explain": "Si alguien tiene tu seed phrase, controla completamente tu wallet."
    },
    # ===========================================
    # TRADING
    # ===========================================
    {
        "q": "¿Qué significa FOMO?",
        "options": [
            "Fast Online Money Opportunity",
            "Fear Of Missing Out",
            "First Option Most Obvious",
            "For Only My Opinion"
        ],
        "correct": 1,
        "explain": "FOMO = miedo a perderse algo. Lleva a comprar impulsivamente cuando ya subió."
    },
    {
        "q": "¿Qué es un stop-loss?",
        "options": [
            "Ganar siempre",
            "Orden que vende automáticamente para limitar pérdidas",
            "Dejar de tradear",
            "Un tipo de criptomoneda"
        ],
        "correct": 1,
        "explain": "El stop-loss es fundamental para gestión de riesgo en trading."
    },
    {
        "q": "¿Qué indica una vela verde en un gráfico?",
        "options": [
            "Precio bajó en ese periodo",
            "Precio subió en ese periodo",
            "No hubo movimiento",
            "El mercado está cerrado"
        ],
        "correct": 1,
        "explain": "Vela verde = precio de cierre mayor al de apertura. Roja = lo contrario."
    },
    {
        "q": "¿Qué es DCA (Dollar Cost Averaging)?",
        "options": [
            "Comprar todo de una vez",
            "Invertir cantidades fijas a intervalos regulares",
            "Vender en cada subida",
            "Pedir préstamos para invertir"
        ],
        "correct": 1,
        "explain": "DCA reduce el impacto de la volatilidad comprando regularmente sin importar el precio."
    },
    {
        "q": "¿Qué es un bull market?",
        "options": [
            "Mercado bajista",
            "Mercado lateral",
            "Mercado alcista con precios al alza",
            "Mercado cerrado"
        ],
        "correct": 2,
        "explain": "Bull market = tendencia alcista. El toro ataca hacia arriba con sus cuernos."
    },
    {
        "q": "¿Qué es el market cap de una cripto?",
        "options": [
            "El precio actual",
            "Precio x cantidad total de monedas en circulación",
            "La ganancia del proyecto",
            "El volumen diario de trading"
        ],
        "correct": 1,
        "explain": "Market Cap = Precio × Supply. Indica el valor total del mercado de esa cripto."
    },
    {
        "q": "¿Qué significa DYOR?",
        "options": [
            "Do Your Own Research",
            "Deposit Your Own Reward",
            "Direct Yield On Risk",
            "Digital Yearly Option"
        ],
        "correct": 0,
        "explain": "Investigá por tu cuenta antes de invertir en cualquier proyecto."
    },
    # ===========================================
    # FAMOUS EVENTS & CULTURE
    # ===========================================
    {
        "q": "¿Qué se celebra el 22 de mayo en cripto?",
        "options": ["Bitcoin Day", "Pizza Day", "Halving Day", "Satoshi Day"],
        "correct": 1,
        "explain": "Bitcoin Pizza Day: el 22/05/2010 se usaron 10.000 BTC para comprar 2 pizzas."
    },
    {
        "q": "¿Qué exchange colapsó en noviembre de 2022?",
        "options": ["Binance", "Coinbase", "FTX", "Kraken"],
        "correct": 2,
        "explain": "FTX colapsó por fraude y uso indebido de fondos de clientes."
    },
    {
        "q": "¿Qué significa WAGMI?",
        "options": [
            "We All Got More Income",
            "We Are Gonna Make It",
            "When All Goes Missing",
            "Wallet And Gain My Interest"
        ],
        "correct": 1,
        "explain": "WAGMI = 'Todos lo vamos a lograr'. Grito de guerra optimista de la comunidad cripto."
    },
    {
        "q": "¿Qué significa 'to the moon' en cripto?",
        "options": [
            "Invertir en la NASA",
            "Que el precio subirá enormemente",
            "Un proyecto blockchain espacial",
            "Comprar terrenos lunares con cripto"
        ],
        "correct": 1,
        "explain": "'To the moon' expresa la expectativa de ganancias extremas en un activo."
    },
    {
        "q": "¿Qué es un whitepaper en cripto?",
        "options": [
            "Papel blanco para escribir seeds",
            "Documento técnico que describe un proyecto cripto",
            "Un contrato legal",
            "Una licencia de minería"
        ],
        "correct": 1,
        "explain": "El whitepaper de Bitcoin fue publicado por Satoshi en 2008."
    },
    {
        "q": "¿Qué es un airdrop en cripto?",
        "options": [
            "Lanzar celulares desde un avión",
            "Distribución gratuita de tokens a wallets",
            "Una caída del precio",
            "Un tipo de hack"
        ],
        "correct": 1,
        "explain": "Los airdrops distribuyen tokens gratis como marketing o recompensa a la comunidad."
    },
    {
        "q": "¿Qué significa NGMI?",
        "options": [
            "Nice Going My Investment",
            "Not Gonna Make It",
            "New Global Market Index",
            "Never Give Money In"
        ],
        "correct": 1,
        "explain": "NGMI = 'No lo va a lograr'. Se usa para decisiones malas en cripto."
    },
    {
        "q": "¿Qué es un NFT?",
        "options": [
            "New Financial Token",
            "Token No Fungible: activo digital único",
            "Network Fee Transaction",
            "Non-Fixed Token"
        ],
        "correct": 1,
        "explain": "Los NFTs representan propiedad única de un activo digital."
    },
    {
        "q": "¿Cuántos satoshis tiene 1 Bitcoin?",
        "options": ["1.000", "1.000.000", "100.000.000", "1.000.000.000"],
        "correct": 2,
        "explain": "1 BTC = 100.000.000 satoshis. Es la unidad más pequeña de Bitcoin."
    },
    {
        "q": "¿Qué es el TVL en DeFi?",
        "options": [
            "Total Value Locked",
            "Token Verified Ledger",
            "Trading Volume Level",
            "Transaction Validation Layer"
        ],
        "correct": 0,
        "explain": "TVL = Valor Total Bloqueado. Mide cuántos fondos hay depositados en protocolos DeFi."
    },
    {
        "q": "¿Qué red se conoce como la internet de blockchains?",
        "options": ["Ethereum", "Cosmos", "Bitcoin", "Avalanche"],
        "correct": 1,
        "explain": "Cosmos (ATOM) permite interoperabilidad entre blockchains via protocolo IBC."
    },
    {
        "q": "¿Qué es un oracle en blockchain?",
        "options": [
            "Un adivino cripto",
            "Servicio que conecta datos reales con smart contracts",
            "Un exchange premium",
            "Un tipo de token"
        ],
        "correct": 1,
        "explain": "Oracles como Chainlink proveen datos externos a contratos inteligentes."
    },
    {
        "q": "¿Qué es un bear market?",
        "options": [
            "Mercado de osos",
            "Período prolongado de precios bajando",
            "Período de precios subiendo",
            "Mercado cerrado por festividad"
        ],
        "correct": 1,
        "explain": "Bear market = mercado bajista. El oso ataca hacia abajo con sus garras."
    },
    {
        "q": "¿Qué % del suministro total de BTC ya fue minado?",
        "options": ["75%", "85%", "93%", "99%"],
        "correct": 2,
        "explain": "~19.5M de los 21M de BTC ya fueron minados (~93%). Faltan ~1.5M."
    },
    {
        "q": "¿Qué es Layer 2 en blockchain?",
        "options": [
            "La segunda cripto más grande",
            "Soluciones sobre la blockchain principal para escalar",
            "El segundo nivel de seguridad",
            "Un exchange de nivel 2"
        ],
        "correct": 1,
        "explain": "Layer 2 (Lightning, Optimism, Arbitrum) procesan tx fuera de la cadena principal."
    },
    {
        "q": "¿Qué es el gas en Ethereum?",
        "options": [
            "Combustible para minar",
            "Fee para ejecutar transacciones o smart contracts",
            "Una criptomoneda alternativa",
            "Energía eléctrica del minero"
        ],
        "correct": 1,
        "explain": "Gas mide esfuerzo computacional. Se paga en ETH y varía según congestión."
    },
]
