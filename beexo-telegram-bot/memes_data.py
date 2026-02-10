"""
Base de datos de 200 memes para Beexo Wallet Bot.
Organizados por categoría temática.
"""

MEMES_DATA = [
    # =============================================
    # CATEGORÍA: DIP CULTURE (1-15)
    # =============================================
    {"file": "meme_001.png", "top": "Compraste el dip con Beexo", "bottom": "Plot twist: era solo el aperitivo del dip", "grad_top": "#1a0a2e", "grad_bottom": "#3d0a4e", "accent": "#e94560", "sep": "arrow", "icon": "DIP"},
    {"file": "meme_002.png", "top": "El mercado cae un 30%", "bottom": "Beexer promedio: DESCUENTO!", "grad_top": "#0a2030", "grad_bottom": "#0a4060", "accent": "#00d2ff", "sep": "line", "icon": "-30%"},
    {"file": "meme_003.png", "top": "Compre el dip 7 veces esta semana", "bottom": "Ya no tengo plata ni para el colectivo", "grad_top": "#1a0a1a", "grad_bottom": "#3a1a3a", "accent": "#ff6b6b", "sep": "dots", "icon": "BROKE"},
    {"file": "meme_004.png", "top": "El dip que compraste ayer", "bottom": "Hoy ya es el piso de otro dip mas grande", "grad_top": "#0a1020", "grad_bottom": "#1a2a40", "accent": "#bb86fc", "sep": "arrow", "icon": "AGAIN"},
    {"file": "meme_005.png", "top": "Todos dicen compra el dip", "bottom": "Nadie dice con que plata", "grad_top": "#1a1a0a", "grad_bottom": "#3a3a1a", "accent": "#ffc947", "sep": "line", "icon": "$0.00"},
    {"file": "meme_006.png", "top": "BTC cae 2% y compro el dip", "bottom": "BTC cae 20% y me quedo mirando", "grad_top": "#0a0a1a", "grad_bottom": "#1a1a3a", "accent": "#4ecdc4", "sep": "dots", "icon": "WAIT"},
    {"file": "meme_007.png", "top": "Puse todo en el dip de lunes", "bottom": "El martes fue otro dip. Y el miercoles tambien.", "grad_top": "#1a0020", "grad_bottom": "#3a0040", "accent": "#e5b8f4", "sep": "arrow", "icon": "REKT"},
    {"file": "meme_008.png", "top": "Le digo a mi novia que compre el dip", "bottom": "Ella: el unico dip que compro es de supermercado", "grad_top": "#200a0a", "grad_bottom": "#401a1a", "accent": "#ff0266", "sep": "line", "icon": "LOVE"},
    {"file": "meme_009.png", "top": "Dip del 10% y nadie compra", "bottom": "Sube 5% y todos FOMO", "grad_top": "#0a200a", "grad_bottom": "#1a401a", "accent": "#03dac6", "sep": "dots", "icon": "WHY"},
    {"file": "meme_010.png", "top": "Compre el dip con mis ahorros", "bottom": "Ahora mis ahorros tambien dipearon", "grad_top": "#10100a", "grad_bottom": "#30301a", "accent": "#f7dc6f", "sep": "arrow", "icon": "SAD"},
    {"file": "meme_011.png", "top": "Cuando pensas que es el fondo", "bottom": "El fondo: dejame presentarte al sotano", "grad_top": "#0a0a20", "grad_bottom": "#1a1a40", "accent": "#79f7ff", "sep": "line", "icon": "FLOOR"},
    {"file": "meme_012.png", "top": "El experto dijo que era el fondo", "bottom": "Spoiler: no era el fondo", "grad_top": "#1a0a10", "grad_bottom": "#3a1a20", "accent": "#e94560", "sep": "dots", "icon": "NOPE"},
    {"file": "meme_013.png", "top": "Comprastelo dip a las 3am", "bottom": "Te levantas a las 7 y bajo otro 15%", "grad_top": "#050510", "grad_bottom": "#101020", "accent": "#bb86fc", "sep": "arrow", "icon": "3 AM"},
    {"file": "meme_014.png", "top": "Mi estrategia: comprar cada dip", "bottom": "Mi cuenta del banco: por favor para", "grad_top": "#0a1515", "grad_bottom": "#1a3030", "accent": "#4ecdc4", "sep": "line", "icon": "BANK"},
    {"file": "meme_015.png", "top": "El dip sigue dippeando", "bottom": "En este punto ya es arqueologia", "grad_top": "#150a0a", "grad_bottom": "#301a1a", "accent": "#ff6b6b", "sep": "dots", "icon": "DEEP"},

    # =============================================
    # CATEGORÍA: SEED PHRASE / SEGURIDAD (16-35)
    # =============================================
    {"file": "meme_016.png", "top": "Alguien te pide tu seed phrase", "bottom": "Dejame compartirte UN BLOQUEO", "grad_top": "#0a1628", "grad_bottom": "#1a3a5c", "accent": "#ff6b6b", "sep": "dots", "icon": "SCAM"},
    {"file": "meme_017.png", "top": "Anoto mi seed phrase en un papel", "bottom": "El papel desaparece misteriosamente", "grad_top": "#050818", "grad_bottom": "#0d1a40", "accent": "#79f7ff", "sep": "arrow", "icon": "RIP"},
    {"file": "meme_018.png", "top": "Password: Bitcoin123", "bottom": "Hacker: Gracias capo ni me esforce", "grad_top": "#1a0a20", "grad_bottom": "#3a1a40", "accent": "#e94560", "sep": "arrow", "icon": "HACK"},
    {"file": "meme_019.png", "top": "Guarde mi seed phrase en la nube", "bottom": "La nube: soy de todos ahora", "grad_top": "#0a1020", "grad_bottom": "#1a2040", "accent": "#00d2ff", "sep": "line", "icon": "CLOUD"},
    {"file": "meme_020.png", "top": "Mi seed phrase esta super segura", "bottom": "La seed: en un post-it pegado al monitor", "grad_top": "#1a1a00", "grad_bottom": "#3a3a10", "accent": "#ffc947", "sep": "dots", "icon": "NOTA"},
    {"file": "meme_021.png", "top": "Le mande mi seed a soporte tecnico", "bottom": "Era un estafador. Ya no tengo cripto.", "grad_top": "#200a10", "grad_bottom": "#401a20", "accent": "#ff0266", "sep": "arrow", "icon": "F"},
    {"file": "meme_022.png", "top": "Mi password tiene 4 caracteres", "bottom": "Un hacker la adivina antes que yo la escriba", "grad_top": "#0a0a1a", "grad_bottom": "#1a1a3a", "accent": "#bb86fc", "sep": "line", "icon": "1234"},
    {"file": "meme_023.png", "top": "Tatue mi seed phrase en el brazo", "bottom": "Plot twist: voy a la playa en verano", "grad_top": "#0a1a10", "grad_bottom": "#1a3a20", "accent": "#4ecdc4", "sep": "dots", "icon": "TATTO"},
    {"file": "meme_024.png", "top": "La seed phrase es como tu cepillo de dientes", "bottom": "No se comparte y si la perdiste ya fue", "grad_top": "#10100a", "grad_bottom": "#30301a", "accent": "#f7dc6f", "sep": "arrow", "icon": "TIP"},
    {"file": "meme_025.png", "top": "2FA activado en todo", "bottom": "Excepto en la cuenta con mis cripto obvio", "grad_top": "#0a0a20", "grad_bottom": "#1a1a40", "accent": "#79f7ff", "sep": "line", "icon": "2FA"},
    {"file": "meme_026.png", "top": "Verificacion por SMS como 2FA", "bottom": "SIM swappers: y gracias", "grad_top": "#1a0a0a", "grad_bottom": "#3a1a1a", "accent": "#e94560", "sep": "dots", "icon": "SIM"},
    {"file": "meme_027.png", "top": "Escondo mi seed en 3 lugares distintos", "bottom": "No me acuerdo donde puse ninguno", "grad_top": "#0a1828", "grad_bottom": "#1a3050", "accent": "#00d2ff", "sep": "arrow", "icon": "LOST"},
    {"file": "meme_028.png", "top": "Me dicen que haga backup de mi wallet", "bottom": "Yo: captura de pantalla de la seed", "grad_top": "#1a0a28", "grad_bottom": "#3a1a50", "accent": "#e5b8f4", "sep": "line", "icon": "NO"},
    {"file": "meme_029.png", "top": "Not your keys not your coins", "bottom": "Tu ex: not your cripto not your lambo", "grad_top": "#150a10", "grad_bottom": "#301a20", "accent": "#ff6b6b", "sep": "dots", "icon": "KEYS"},
    {"file": "meme_030.png", "top": "Uso la misma password en todo", "bottom": "Me hackean el mail y caen 47 cuentas", "grad_top": "#0a1510", "grad_bottom": "#1a3020", "accent": "#03dac6", "sep": "arrow", "icon": "OOPS"},
    {"file": "meme_031.png", "top": "Verifico 5 veces la direccion al enviar", "bottom": "Igual sudo frio hasta que confirma", "grad_top": "#100a15", "grad_bottom": "#201a30", "accent": "#bb86fc", "sep": "line", "icon": "CHECK"},
    {"file": "meme_032.png", "top": "Primera vez mandando cripto", "bottom": "Mando $1 de prueba. Pago $15 de fee.", "grad_top": "#0a100a", "grad_bottom": "#1a201a", "accent": "#4ecdc4", "sep": "dots", "icon": "TEST"},
    {"file": "meme_033.png", "top": "Alguien en el grupo dice SOPORTE", "bottom": "5 scammers: Hola como te puedo ayudar?", "grad_top": "#1a1008", "grad_bottom": "#3a2018", "accent": "#ffc947", "sep": "arrow", "icon": "DM"},
    {"file": "meme_034.png", "top": "Clave: nombre de mi perro + 123", "bottom": "Todo el barrio sabe como se llama mi perro", "grad_top": "#080818", "grad_bottom": "#101030", "accent": "#79f7ff", "sep": "line", "icon": "FIRULAIS"},
    {"file": "meme_035.png", "top": "Guarde mi seed en una caja fuerte", "bottom": "Perdi la llave de la caja fuerte", "grad_top": "#180a10", "grad_bottom": "#301a20", "accent": "#ff0266", "sep": "dots", "icon": "SAFE"},

    # =============================================
    # CATEGORÍA: HODL / DIAMOND HANDS (36-55)
    # =============================================
    {"file": "meme_036.png", "top": "Mis amigos: Vende ya!", "bottom": "Yo con Beexo: DIAMOND HANDS", "grad_top": "#0a1a20", "grad_bottom": "#0a3a40", "accent": "#03dac6", "sep": "arrow", "icon": "HODL"},
    {"file": "meme_037.png", "top": "Un Beexer nunca pierde", "bottom": "Solo HODLea hasta que el grafico se de vuelta", "grad_top": "#0a1a1a", "grad_bottom": "#1a3a3a", "accent": "#4ecdc4", "sep": "line", "icon": "HODL"},
    {"file": "meme_038.png", "top": "HODL desde 2021", "bottom": "A esta altura ya no es estrategia es terquedad", "grad_top": "#1a0a20", "grad_bottom": "#3a1a40", "accent": "#bb86fc", "sep": "dots", "icon": "2021"},
    {"file": "meme_039.png", "top": "Me dicen vendelo que ya perdiste", "bottom": "Yo: no perdi si no vendi", "grad_top": "#0a200a", "grad_bottom": "#1a401a", "accent": "#4ecdc4", "sep": "arrow", "icon": "IQ200"},
    {"file": "meme_040.png", "top": "Llevo 3 anios holdeando", "bottom": "A este punto la cripto ya es parte de la familia", "grad_top": "#10100a", "grad_bottom": "#20201a", "accent": "#f7dc6f", "sep": "line", "icon": "3Y"},
    {"file": "meme_041.png", "top": "Voy a holdear hasta el millon", "bottom": "Mi saldo: $47", "grad_top": "#0a0a18", "grad_bottom": "#1a1a30", "accent": "#79f7ff", "sep": "dots", "icon": "$47"},
    {"file": "meme_042.png", "top": "Paper hands venden en -5%", "bottom": "Diamond hands holdeamos hasta -95% con orgullo", "grad_top": "#1a0a10", "grad_bottom": "#3a1a20", "accent": "#e94560", "sep": "arrow", "icon": "STONE"},
    {"file": "meme_043.png", "top": "Mi cripto bajo 80%", "bottom": "Pero no vendi asi que tecnicamente no perdi", "grad_top": "#0a1520", "grad_bottom": "#1a3040", "accent": "#00d2ff", "sep": "line", "icon": "MATH"},
    {"file": "meme_044.png", "top": "Holdeando desde que BTC estaba en 60K", "bottom": "Si bajo a 20K pero ahora volvio. Ven? Paciencia.", "grad_top": "#1a1008", "grad_bottom": "#3a2818", "accent": "#ffc947", "sep": "dots", "icon": "ZEN"},
    {"file": "meme_045.png", "top": "Mi familia: cuando vendas?", "bottom": "Yo: Si.", "grad_top": "#100a18", "grad_bottom": "#201a30", "accent": "#bb86fc", "sep": "arrow", "icon": "NEVER"},
    {"file": "meme_046.png", "top": "Todos vendieron en panico", "bottom": "Yo: tengo Beexo y tengo paciencia", "grad_top": "#0a1810", "grad_bottom": "#1a3020", "accent": "#03dac6", "sep": "line", "icon": "CALM"},
    {"file": "meme_047.png", "top": "El grafico parece un electrocardiograma", "bottom": "Mi corazon tambien", "grad_top": "#1a0a0a", "grad_bottom": "#3a1a1a", "accent": "#ff6b6b", "sep": "dots", "icon": "BPM"},
    {"file": "meme_048.png", "top": "HODL es facil dicen", "bottom": "Facil hasta que tu portfolio baja 60%", "grad_top": "#0a0a10", "grad_bottom": "#1a1a20", "accent": "#e5b8f4", "sep": "arrow", "icon": "EASY?"},
    {"file": "meme_049.png", "top": "Vendi al fondo pensando que bajaba mas", "bottom": "Subio 40% al dia siguiente", "grad_top": "#180810", "grad_bottom": "#301820", "accent": "#ff0266", "sep": "line", "icon": "PAIN"},
    {"file": "meme_050.png", "top": "Mi plan: holdear 5 anios", "bottom": "Realidad: reviso Beexo cada 5 minutos", "grad_top": "#0a1018", "grad_bottom": "#1a2030", "accent": "#79f7ff", "sep": "dots", "icon": "5MIN"},
    {"file": "meme_051.png", "top": "Holdear es un arte", "bottom": "Y yo soy Picasso del sufrimiento", "grad_top": "#1a0818", "grad_bottom": "#3a1830", "accent": "#e94560", "sep": "arrow", "icon": "ART"},
    {"file": "meme_052.png", "top": "No soy inversor soy coleccionista", "bottom": "Colecciono perdidas no realizadas", "grad_top": "#081018", "grad_bottom": "#102030", "accent": "#00d2ff", "sep": "line", "icon": "NFT?"},
    {"file": "meme_053.png", "top": "Le digo a todos que soy holder", "bottom": "En realidad olvide la password de Beexo", "grad_top": "#10100a", "grad_bottom": "#28281a", "accent": "#ffc947", "sep": "dots", "icon": "SHHHH"},
    {"file": "meme_054.png", "top": "Compre en el ATH y holdee", "bottom": "Van 2 anios. Aun no recupere. Sigo firme.", "grad_top": "#0a0a18", "grad_bottom": "#1a1a38", "accent": "#bb86fc", "sep": "arrow", "icon": "ATH"},
    {"file": "meme_055.png", "top": "Mi abuela: vendelo nene", "bottom": "Yo: abuela vos no entendes blockchain", "grad_top": "#081520", "grad_bottom": "#183040", "accent": "#4ecdc4", "sep": "line", "icon": "ABU"},

    # =============================================
    # CATEGORÍA: SCAM AWARENESS (56-75)
    # =============================================
    {"file": "meme_056.png", "top": "'Hola soy del soporte de Beexo'", "bottom": "Ningun soporte te escribe por DM. ES ESTAFA.", "grad_top": "#1a1a0a", "grad_bottom": "#3a3a1a", "accent": "#ffc947", "sep": "arrow", "icon": "FAKE"},
    {"file": "meme_057.png", "top": "Inverti $100 y gane $10.000 en 1 dia", "bottom": "Si y yo soy Satoshi Nakamoto", "grad_top": "#300040", "grad_bottom": "#600080", "accent": "#ff0266", "sep": "dots", "icon": "JAJA"},
    {"file": "meme_058.png", "top": "Me mandaron un link por DM", "bottom": "Conecta tu wallet dice. Dale conectala en 3 2 1.", "grad_top": "#1a0a10", "grad_bottom": "#3a1a20", "accent": "#e94560", "sep": "arrow", "icon": "LINK"},
    {"file": "meme_059.png", "top": "Duplica tus BTC enviando 0.1 BTC", "bottom": "Si Elon Musk estuviera regalando plata no usaria YouTube", "grad_top": "#0a1020", "grad_bottom": "#1a2040", "accent": "#00d2ff", "sep": "line", "icon": "x2?"},
    {"file": "meme_060.png", "top": "Rentabilidad garantizada 50% mensual", "bottom": "La unica garantia es que te van a estafar", "grad_top": "#1a0a20", "grad_bottom": "#3a1a40", "accent": "#bb86fc", "sep": "dots", "icon": "PONZI"},
    {"file": "meme_061.png", "top": "Un admin me hablo por privado", "bottom": "Ningun admin real hace eso. Report + block.", "grad_top": "#0a1510", "grad_bottom": "#1a3020", "accent": "#4ecdc4", "sep": "arrow", "icon": "ADMIN"},
    {"file": "meme_062.png", "top": "Airdrops gratis si conectas tu wallet", "bottom": "Lo unico gratis va a ser tu wallet vacia", "grad_top": "#1a100a", "grad_bottom": "#3a201a", "accent": "#ffc947", "sep": "line", "icon": "FREE?"},
    {"file": "meme_063.png", "top": "Token nuevo con 10000% APY", "bottom": "Donde esta el equipo? Anonimo. Dale confia.", "grad_top": "#0a0a18", "grad_bottom": "#1a1a38", "accent": "#ff6b6b", "sep": "dots", "icon": "RUG"},
    {"file": "meme_064.png", "top": "El scammer: confien en mi", "bottom": "Su perfil: creado hace 2 horas sin foto", "grad_top": "#180810", "grad_bottom": "#381020", "accent": "#e5b8f4", "sep": "arrow", "icon": "NEW"},
    {"file": "meme_065.png", "top": "Si te apuran para invertir", "bottom": "La unica urgencia es la de ellos por tu plata", "grad_top": "#0a180a", "grad_bottom": "#1a301a", "accent": "#03dac6", "sep": "line", "icon": "STOP"},
    {"file": "meme_066.png", "top": "Proyecto sin whitepaper ni equipo visible", "bottom": "Pero tiene 3 influencers promocionandolo", "grad_top": "#10100a", "grad_bottom": "#28281a", "accent": "#f7dc6f", "sep": "dots", "icon": "RED"},
    {"file": "meme_067.png", "top": "El grupo de Telegram del token tiene 50K", "bottom": "48K son bots. Los otros 2K tambien.", "grad_top": "#0a0a1a", "grad_bottom": "#1a1a3a", "accent": "#79f7ff", "sep": "arrow", "icon": "BOTS"},
    {"file": "meme_068.png", "top": "Ganancia garantizada sin riesgo", "bottom": "Hay mas red flags que en una carrera de F1", "grad_top": "#1a0810", "grad_bottom": "#3a1020", "accent": "#e94560", "sep": "line", "icon": "F1"},
    {"file": "meme_069.png", "top": "El scammer me mando captura de ganancias", "bottom": "Yo puedo photoshopear eso en 5 minutos", "grad_top": "#0a1028", "grad_bottom": "#1a2050", "accent": "#00d2ff", "sep": "dots", "icon": "FAKE"},
    {"file": "meme_070.png", "top": "Inversion minima $500 ganancias maximas", "bottom": "La unica ganancia maxima es la del estafador", "grad_top": "#200a18", "grad_bottom": "#401a30", "accent": "#ff0266", "sep": "arrow", "icon": "NOPE"},
    {"file": "meme_071.png", "top": "Me pidieron verificar mi wallet", "bottom": "La unica verificacion es que son ladrones", "grad_top": "#0a1818", "grad_bottom": "#1a3030", "accent": "#4ecdc4", "sep": "line", "icon": "SCAM"},
    {"file": "meme_072.png", "top": "Si suena demasiado bueno para ser verdad", "bottom": "Adivina que? No es verdad.", "grad_top": "#181008", "grad_bottom": "#302818", "accent": "#ffc947", "sep": "dots", "icon": "REGLA"},
    {"file": "meme_073.png", "top": "Te contacta alguien que gana mucho en cripto", "bottom": "Si ganara tanto no necesitaria tu plata", "grad_top": "#0a0818", "grad_bottom": "#1a1030", "accent": "#bb86fc", "sep": "arrow", "icon": "THINK"},
    {"file": "meme_074.png", "top": "Firma esta transaccion para recibir tu premio", "bottom": "El premio: te vacia la wallet", "grad_top": "#180a0a", "grad_bottom": "#301a1a", "accent": "#ff6b6b", "sep": "line", "icon": "SIGN?"},
    {"file": "meme_075.png", "top": "Cripto-influencer: pongan todo ahi", "bottom": "El influencer ya vendio hace 2 semanas", "grad_top": "#08100a", "grad_bottom": "#18201a", "accent": "#03dac6", "sep": "dots", "icon": "SOLD"},

    # =============================================
    # CATEGORÍA: FOMO / FUD (76-95)
    # =============================================
    {"file": "meme_076.png", "top": "No compre cuando estaba barato", "bottom": "Ahora sigo sin comprar pero con bronca", "grad_top": "#0a2020", "grad_bottom": "#1a4a4a", "accent": "#4ecdc4", "sep": "dots", "icon": "FOMO"},
    {"file": "meme_077.png", "top": "Compro al ver que sube un 10%", "bottom": "Inmediatamente baja un 15%", "grad_top": "#1a0a18", "grad_bottom": "#3a1a30", "accent": "#e94560", "sep": "arrow", "icon": "LATE"},
    {"file": "meme_078.png", "top": "Todos estan comprando y yo no", "bottom": "Plot twist: soy el unico inteligente aca", "grad_top": "#0a1020", "grad_bottom": "#1a2040", "accent": "#00d2ff", "sep": "line", "icon": "WAIT"},
    {"file": "meme_079.png", "top": "FOMO a las 2 de la maniana", "bottom": "Compro en el pico. Duermo tranquilo. Miento.", "grad_top": "#050510", "grad_bottom": "#101020", "accent": "#bb86fc", "sep": "dots", "icon": "2 AM"},
    {"file": "meme_080.png", "top": "Alguien en Twitter dice que va a $0", "bottom": "Vendo todo. Sube 200% la semana siguiente.", "grad_top": "#1a1008", "grad_bottom": "#3a2818", "accent": "#ffc947", "sep": "arrow", "icon": "FUD"},
    {"file": "meme_081.png", "top": "Me salio una noticia de BTC en rojo", "bottom": "Entro en panico. Son solo las noticias de ayer.", "grad_top": "#180a10", "grad_bottom": "#301a20", "accent": "#ff6b6b", "sep": "line", "icon": "NEWS"},
    {"file": "meme_082.png", "top": "Todos mis amigos compraron X token", "bottom": "Lo compre por FOMO. Fui el ultimo antes del dump.", "grad_top": "#0a1510", "grad_bottom": "#1a3020", "accent": "#4ecdc4", "sep": "dots", "icon": "LAST"},
    {"file": "meme_083.png", "top": "Lei que cripto se muere en 2026", "bottom": "Lo mismo dijeron en 2017 2018 2019 2020 2021...", "grad_top": "#10100a", "grad_bottom": "#28281a", "accent": "#f7dc6f", "sep": "arrow", "icon": "DEAD?"},
    {"file": "meme_084.png", "top": "Musk tuiteo algo negativo de cripto", "bottom": "El mercado: Y AHORA SI PANICKEAMOS", "grad_top": "#0a0a18", "grad_bottom": "#1a1a38", "accent": "#79f7ff", "sep": "line", "icon": "ELON"},
    {"file": "meme_085.png", "top": "Deberia haber comprado hace 5 anios", "bottom": "En 5 anios voy a decir lo mismo de hoy", "grad_top": "#1a0a10", "grad_bottom": "#3a1a20", "accent": "#e5b8f4", "sep": "dots", "icon": "TIME"},
    {"file": "meme_086.png", "top": "Twitter dice BTC a 1 millon", "bottom": "Reddit dice BTC a 0. Yo ya no se nada.", "grad_top": "#0a1818", "grad_bottom": "#1a3030", "accent": "#03dac6", "sep": "arrow", "icon": "???"},
    {"file": "meme_087.png", "top": "Subio 3% y ya me siento millonario", "bottom": "Bajo 3% y ya estoy buscando laburo", "grad_top": "#1a0808", "grad_bottom": "#3a1818", "accent": "#ff0266", "sep": "line", "icon": "MOOD"},
    {"file": "meme_088.png", "top": "FOMO me hizo comprar 8 altcoins", "bottom": "7 ya no existen. La otra bajo 99%.", "grad_top": "#0a100a", "grad_bottom": "#1a201a", "accent": "#4ecdc4", "sep": "dots", "icon": "RIP x7"},
    {"file": "meme_089.png", "top": "Influencer: Esta cripto va a explotar!", "bottom": "Exploto. Pero en el mal sentido.", "grad_top": "#18100a", "grad_bottom": "#302818", "accent": "#ffc947", "sep": "arrow", "icon": "BOOM"},
    {"file": "meme_090.png", "top": "Me da FOMO cuando sube", "bottom": "Me da FUD cuando baja. No hay paz.", "grad_top": "#0a0818", "grad_bottom": "#1a1030", "accent": "#bb86fc", "sep": "line", "icon": "LOOP"},
    {"file": "meme_091.png", "top": "China banea cripto por 427ma vez", "bottom": "El mercado: ah si esto ya lo vimos", "grad_top": "#1a0a0a", "grad_bottom": "#3a1a1a", "accent": "#ff6b6b", "sep": "dots", "icon": "CHINA"},
    {"file": "meme_092.png", "top": "Vendi todo por miedo al crash", "bottom": "El mercado subio 100% sin mi", "grad_top": "#0a100a", "grad_bottom": "#1a301a", "accent": "#03dac6", "sep": "arrow", "icon": "BYE"},
    {"file": "meme_093.png", "top": "FUD de lunes: todo mal", "bottom": "FOMO de viernes: todo genial. Normal.", "grad_top": "#10080a", "grad_bottom": "#28181a", "accent": "#e94560", "sep": "line", "icon": "CYCLE"},
    {"file": "meme_094.png", "top": "Me convenci de no comprar", "bottom": "5 minutos despues estoy en Beexo comprando", "grad_top": "#08100a", "grad_bottom": "#18281a", "accent": "#f7dc6f", "sep": "dots", "icon": "WEAK"},
    {"file": "meme_095.png", "top": "FOMO + FUD + 0 gestion de riesgo", "bottom": "La santa trinidad de perder plata en cripto", "grad_top": "#0a0810", "grad_bottom": "#1a1020", "accent": "#79f7ff", "sep": "arrow", "icon": "HOLY"},

    # =============================================
    # CATEGORÍA: GAS FEES / TRANSACCIONES (96-110)
    # =============================================
    {"file": "meme_096.png", "top": "Queres hacer un swap", "bottom": "Las fees: Que lindo depto tenes ahi", "grad_top": "#200020", "grad_bottom": "#4a004a", "accent": "#e5b8f4", "sep": "line", "icon": "GAS"},
    {"file": "meme_097.png", "top": "Quiero mandar $10 de cripto", "bottom": "Fee de red: $47. Gracias Ethereum.", "grad_top": "#0a1020", "grad_bottom": "#1a2040", "accent": "#00d2ff", "sep": "dots", "icon": "$47"},
    {"file": "meme_098.png", "top": "Espere a que baje el gas", "bottom": "Sigo esperando. Van 3 semanas.", "grad_top": "#1a0a10", "grad_bottom": "#3a1a20", "accent": "#e94560", "sep": "arrow", "icon": "GWEI"},
    {"file": "meme_099.png", "top": "Fee de transaccion mas cara que mi almuerzo", "bottom": "Hoy no como pero al menos tengo descentralizacion", "grad_top": "#10100a", "grad_bottom": "#28281a", "accent": "#ffc947", "sep": "line", "icon": "LUNCH"},
    {"file": "meme_100.png", "top": "Hago una tx por $5", "bottom": "Pago $30 de fee. Gran negocio.", "grad_top": "#0a0a18", "grad_bottom": "#1a1a38", "accent": "#bb86fc", "sep": "dots", "icon": "-$25"},
    {"file": "meme_101.png", "top": "Gas bajo a $2 y corro a hacer el swap", "bottom": "Cuando cargo la tx ya esta en $18", "grad_top": "#0a1810", "grad_bottom": "#1a3020", "accent": "#4ecdc4", "sep": "arrow", "icon": "FAST"},
    {"file": "meme_102.png", "top": "Mando cripto a la direccion equivocada", "bottom": "No hay atencion al cliente en blockchain", "grad_top": "#1a0a18", "grad_bottom": "#3a1a30", "accent": "#ff0266", "sep": "line", "icon": "WRONG"},
    {"file": "meme_103.png", "top": "Espero 45 minutos por una confirmacion", "bottom": "Visa lo hace en 2 segundos pero no tiene gracia", "grad_top": "#081018", "grad_bottom": "#182030", "accent": "#79f7ff", "sep": "dots", "icon": "WAIT"},
    {"file": "meme_104.png", "top": "Mi transaccion esta pendiente hace 2 horas", "bottom": "Blockchain: estoy en eso maestro tranquilo", "grad_top": "#1a1008", "grad_bottom": "#3a2018", "accent": "#f7dc6f", "sep": "arrow", "icon": "PEND"},
    {"file": "meme_105.png", "top": "Puse gas muy bajo para ahorrar", "bottom": "Mi transaccion va a confirmar en el 2030", "grad_top": "#0a0a10", "grad_bottom": "#1a1a28", "accent": "#e5b8f4", "sep": "line", "icon": "2030"},
    {"file": "meme_106.png", "top": "Quiero comprar un NFT de $20", "bottom": "Fee de mint: $80. Es un hobby caro.", "grad_top": "#180810", "grad_bottom": "#381020", "accent": "#ff6b6b", "sep": "dots", "icon": "MINT"},
    {"file": "meme_107.png", "top": "Aprobar el contrato cuesta gas", "bottom": "Hacer el swap cuesta gas. Respirar cuesta gas.", "grad_top": "#0a1520", "grad_bottom": "#1a3040", "accent": "#00d2ff", "sep": "arrow", "icon": "ETH"},
    {"file": "meme_108.png", "top": "Layer 2 para fees baratas dicen", "bottom": "Bridge al L2: $40 de fee. Muy barato si.", "grad_top": "#1a0808", "grad_bottom": "#3a1818", "accent": "#e94560", "sep": "line", "icon": "L2"},
    {"file": "meme_109.png", "top": "Hago DCA semanal de $10", "bottom": "$10 de cripto + $15 de fees = gran estrategia", "grad_top": "#0a180a", "grad_bottom": "#1a301a", "accent": "#03dac6", "sep": "dots", "icon": "DCA"},
    {"file": "meme_110.png", "top": "Copy la direccion bien", "bottom": "Se me fue un caracter. Adiós para siempre cripto.", "grad_top": "#100a18", "grad_bottom": "#201a30", "accent": "#bb86fc", "sep": "arrow", "icon": "0x..."},

    # =============================================
    # CATEGORÍA: PORTFOLIO / OBSESIÓN (111-130)
    # =============================================
    {"file": "meme_111.png", "top": "Abro Beexo a ver mi portfolio", "bottom": "Lo cierro. Lo abro. Lo cierro. Lo abro.", "grad_top": "#141a0a", "grad_bottom": "#2a3a1a", "accent": "#f7dc6f", "sep": "line", "icon": "LOOP"},
    {"file": "meme_112.png", "top": "Miro el portfolio 47 veces al dia", "bottom": "No cambia nada pero por las dudas", "grad_top": "#0a1018", "grad_bottom": "#1a2030", "accent": "#79f7ff", "sep": "dots", "icon": "x47"},
    {"file": "meme_113.png", "top": "En verde: Soy un genio financiero", "bottom": "En rojo: El mercado esta manipulado", "grad_top": "#0a1020", "grad_bottom": "#1a2a40", "accent": "#ff6b6b", "sep": "arrow", "icon": "VS"},
    {"file": "meme_114.png", "top": "Mi portfolio sube $3", "bottom": "Yo: deberia dejar mi trabajo?", "grad_top": "#1a1008", "grad_bottom": "#3a2818", "accent": "#ffc947", "sep": "line", "icon": "$3"},
    {"file": "meme_115.png", "top": "Portfolio en rojo otra vez", "bottom": "Lo apago total ya estoy acostumbrado", "grad_top": "#1a0a10", "grad_bottom": "#3a1a20", "accent": "#e94560", "sep": "dots", "icon": "RED"},
    {"file": "meme_116.png", "top": "Lo primero que hago al despertar", "bottom": "Abrir Beexo. Despues respirar.", "grad_top": "#0a0a1a", "grad_bottom": "#1a1a3a", "accent": "#bb86fc", "sep": "arrow", "icon": "7 AM"},
    {"file": "meme_117.png", "top": "Mi novia: o el portfolio o yo", "bottom": "La extranio a veces", "grad_top": "#180a10", "grad_bottom": "#301a20", "accent": "#ff0266", "sep": "line", "icon": "BYE"},
    {"file": "meme_118.png", "top": "Reviso Beexo en el banio", "bottom": "Llevo 40 minutos y me estan buscando", "grad_top": "#0a1510", "grad_bottom": "#1a3020", "accent": "#4ecdc4", "sep": "dots", "icon": "WC"},
    {"file": "meme_119.png", "top": "Mi portfolio: -2% hoy", "bottom": "Yo buscando quien hackeo el mercado", "grad_top": "#10100a", "grad_bottom": "#28281a", "accent": "#f7dc6f", "sep": "arrow", "icon": "FBI"},
    {"file": "meme_120.png", "top": "Diversifique en 15 tokens", "bottom": "Todos bajaron. Gran diversificacion.", "grad_top": "#0a0a10", "grad_bottom": "#1a1a28", "accent": "#79f7ff", "sep": "line", "icon": "15x"},
    {"file": "meme_121.png", "top": "Portfolio 80% en un solo token", "bottom": "Diversificacion? Eso es para los miedosos.", "grad_top": "#1a0a18", "grad_bottom": "#3a1a30", "accent": "#e5b8f4", "sep": "dots", "icon": "ALL IN"},
    {"file": "meme_122.png", "top": "Le puse $100 y vale $47", "bottom": "Le pongo $100 mas para promediar la perdida", "grad_top": "#0a1818", "grad_bottom": "#1a3030", "accent": "#03dac6", "sep": "arrow", "icon": "DCA?"},
    {"file": "meme_123.png", "top": "Inversion a largo plazo dicen", "bottom": "Yo reviso el grafico de 1 minuto", "grad_top": "#1a0808", "grad_bottom": "#3a1818", "accent": "#ff6b6b", "sep": "line", "icon": "1M"},
    {"file": "meme_124.png", "top": "Puse mi portfolio en un Excel", "bottom": "La formula me da negativo en 14 colores", "grad_top": "#081008", "grad_bottom": "#182018", "accent": "#4ecdc4", "sep": "dots", "icon": "EXCEL"},
    {"file": "meme_125.png", "top": "Lunes: voy a dejar de mirar el portfolio", "bottom": "Martes a las 6am ya estoy en Beexo", "grad_top": "#10080a", "grad_bottom": "#28181a", "accent": "#e94560", "sep": "arrow", "icon": "ADDICT"},
    {"file": "meme_126.png", "top": "Saque screenshot cuando estaba en verde", "bottom": "Es el unico recuerdo feliz de mi portfolio", "grad_top": "#0a100a", "grad_bottom": "#1a281a", "accent": "#ffc947", "sep": "line", "icon": "FOTO"},
    {"file": "meme_127.png", "top": "Mi portfolio tiene tantos colores", "bottom": "Lástima que son todos rojos", "grad_top": "#0a0a18", "grad_bottom": "#1a1a30", "accent": "#bb86fc", "sep": "dots", "icon": "RGB"},
    {"file": "meme_128.png", "top": "Compre 20 criptos distintas", "bottom": "Mi portfolio parece un arcoiris depresivo", "grad_top": "#180a0a", "grad_bottom": "#301a1a", "accent": "#ff0266", "sep": "arrow", "icon": "RAIN"},
    {"file": "meme_129.png", "top": "Me dijeron pon solo lo que puedas perder", "bottom": "Bueno ya perdi lo que podia y lo que no tambien", "grad_top": "#0a1520", "grad_bottom": "#1a3040", "accent": "#00d2ff", "sep": "line", "icon": "RULE"},
    {"file": "meme_130.png", "top": "Portfolio tracker en el reloj", "bottom": "Me sube la presion cada vez que miro la hora", "grad_top": "#100a10", "grad_bottom": "#201a20", "accent": "#e5b8f4", "sep": "dots", "icon": "WATCH"},

    # =============================================
    # CATEGORÍA: TRADING / ANÁLISIS TÉCNICO (131-150)
    # =============================================
    {"file": "meme_131.png", "top": "Mi amigo dice que un token va x1000", "bottom": "DYOR o Do Your Own Regret", "grad_top": "#1a0040", "grad_bottom": "#3a0080", "accent": "#bb86fc", "sep": "dots", "icon": "DYOR"},
    {"file": "meme_132.png", "top": "Tengo nociones de trading", "bottom": "Las nociones: comprar caro vender barato", "grad_top": "#200020", "grad_bottom": "#400040", "accent": "#bb86fc", "sep": "dots", "icon": "PRO"},
    {"file": "meme_133.png", "top": "Dibujo lineas en el grafico", "bottom": "El grafico: no sabe leer", "grad_top": "#0a1020", "grad_bottom": "#1a2040", "accent": "#00d2ff", "sep": "arrow", "icon": "TA"},
    {"file": "meme_134.png", "top": "Mi analisis tecnico predice alza", "bottom": "El mercado: y a mi que me importa tu analisis", "grad_top": "#1a0a10", "grad_bottom": "#3a1a20", "accent": "#e94560", "sep": "line", "icon": "CHART"},
    {"file": "meme_135.png", "top": "Patron hombro cabeza hombro", "bottom": "Lo unico que veo es un garabato", "grad_top": "#10100a", "grad_bottom": "#28281a", "accent": "#ffc947", "sep": "dots", "icon": "HCH"},
    {"file": "meme_136.png", "top": "Puse un stop loss al 5%", "bottom": "Se ejecuta y despues sube 30%. Clasico.", "grad_top": "#0a0a18", "grad_bottom": "#1a1a38", "accent": "#79f7ff", "sep": "arrow", "icon": "SL"},
    {"file": "meme_137.png", "top": "Abro posicion larga con leverage x20", "bottom": "Liquidado en 4 minutos. Nuevo record.", "grad_top": "#1a0818", "grad_bottom": "#3a1030", "accent": "#ff0266", "sep": "line", "icon": "x20"},
    {"file": "meme_138.png", "top": "Scalping es facil dicen", "bottom": "Perdi en 47 trades de los 50 que hice", "grad_top": "#0a1810", "grad_bottom": "#1a3020", "accent": "#4ecdc4", "sep": "dots", "icon": "47/50"},
    {"file": "meme_139.png", "top": "El RSI dice sobrecomprado", "bottom": "El mercado sigue subiendo. El RSI miente.", "grad_top": "#1a1008", "grad_bottom": "#3a2818", "accent": "#f7dc6f", "sep": "arrow", "icon": "RSI"},
    {"file": "meme_140.png", "top": "Mi bot de trading gano $2 este mes", "bottom": "Gaste $40 en electricidad para correrlo", "grad_top": "#0a0810", "grad_bottom": "#1a1020", "accent": "#bb86fc", "sep": "line", "icon": "BOT"},
    {"file": "meme_141.png", "top": "Voy a hacer day trading dicen", "bottom": "Una semana despues: voy a holdear mejor", "grad_top": "#180a0a", "grad_bottom": "#301a1a", "accent": "#ff6b6b", "sep": "dots", "icon": "DAY 1"},
    {"file": "meme_142.png", "top": "Puse el take profit en +50%", "bottom": "Llego a +49% y se dio vuelta. La vida.", "grad_top": "#0a100a", "grad_bottom": "#1a281a", "accent": "#03dac6", "sep": "arrow", "icon": "49%"},
    {"file": "meme_143.png", "top": "Leverage x100: o lambo o ramen", "bottom": "Spoiler: fue ramen", "grad_top": "#1a0a0a", "grad_bottom": "#3a1a1a", "accent": "#e94560", "sep": "line", "icon": "x100"},
    {"file": "meme_144.png", "top": "Opere en base a un tweet", "bottom": "La mayor perdida de mi vida en 3 horas", "grad_top": "#08100a", "grad_bottom": "#18201a", "accent": "#4ecdc4", "sep": "dots", "icon": "TWEET"},
    {"file": "meme_145.png", "top": "Indicadores: todos en rojo", "bottom": "Yo: pero tengo un presentimiento", "grad_top": "#100810", "grad_bottom": "#201820", "accent": "#e5b8f4", "sep": "arrow", "icon": "GUT"},
    {"file": "meme_146.png", "top": "Compre por analisis fundamental", "bottom": "Sigo en -70% pero el proyecto es bueno", "grad_top": "#0a1818", "grad_bottom": "#1a3030", "accent": "#00d2ff", "sep": "line", "icon": "FA"},
    {"file": "meme_147.png", "top": "Trading con emociones", "bottom": "Miedo compro. Euforia vendo. Al reves de todo.", "grad_top": "#1a100a", "grad_bottom": "#3a201a", "accent": "#ffc947", "sep": "dots", "icon": "EMO"},
    {"file": "meme_148.png", "top": "Mi order book parece una obra de arte", "bottom": "Lastima que el resultado es un desastre", "grad_top": "#0a0a1a", "grad_bottom": "#1a1a3a", "accent": "#79f7ff", "sep": "arrow", "icon": "ART"},
    {"file": "meme_149.png", "top": "Aprendi AT en YouTube en 1 hora", "bottom": "Ya me creo el lobo de las criptos", "grad_top": "#1a0810", "grad_bottom": "#3a1020", "accent": "#ff0266", "sep": "line", "icon": "YT"},
    {"file": "meme_150.png", "top": "Market order a las 3am medio dormido", "bottom": "Al otro dia: que hice", "grad_top": "#050510", "grad_bottom": "#101020", "accent": "#bb86fc", "sep": "dots", "icon": "3 AM"},

    # =============================================
    # CATEGORÍA: FAMILIA / AMIGOS (151-170)
    # =============================================
    {"file": "meme_151.png", "top": "Le explico cripto a mi abuela", "bottom": "Mi abuela: Mejor comprate un terrenito", "grad_top": "#081020", "grad_bottom": "#102040", "accent": "#79f7ff", "sep": "dots", "icon": "ABU"},
    {"file": "meme_152.png", "top": "Le mando BTC de regalo por Beexo", "bottom": "Mi familia: Prefiero la gift card", "grad_top": "#1a0a0a", "grad_bottom": "#3a1a1a", "accent": "#e94560", "sep": "line", "icon": "GIFT"},
    {"file": "meme_153.png", "top": "Mi viejo: Y eso del bitcoin que es?", "bottom": "Yo: Es dinero digital. El: Como Mercado Pago?", "grad_top": "#0a1020", "grad_bottom": "#1a2040", "accent": "#00d2ff", "sep": "arrow", "icon": "PAPA"},
    {"file": "meme_154.png", "top": "Navidad: me preguntan de cripto", "bottom": "Les explico 20 minutos y ponen cara de nada", "grad_top": "#1a0a18", "grad_bottom": "#3a1a30", "accent": "#e5b8f4", "sep": "dots", "icon": "XMAS"},
    {"file": "meme_155.png", "top": "Mi mama: Invertiste en algo seguro?", "bottom": "Yo con un portfolio de memecoins: Si ma", "grad_top": "#0a1510", "grad_bottom": "#1a3020", "accent": "#4ecdc4", "sep": "line", "icon": "MAMA"},
    {"file": "meme_156.png", "top": "Cena familiar: No hablen de cripto", "bottom": "Yo a los 5 minutos: Sabias que BTC...", "grad_top": "#10100a", "grad_bottom": "#28281a", "accent": "#ffc947", "sep": "arrow", "icon": "CENA"},
    {"file": "meme_157.png", "top": "Mi amigo gano en cripto y me conto", "bottom": "No me conto de las 12 veces que perdio", "grad_top": "#0a0a1a", "grad_bottom": "#1a1a3a", "accent": "#bb86fc", "sep": "dots", "icon": "BRO"},
    {"file": "meme_158.png", "top": "Le recomende cripto a mi primo", "bottom": "Bajo 40% y ahora no me habla", "grad_top": "#1a0a10", "grad_bottom": "#3a1a20", "accent": "#ff6b6b", "sep": "line", "icon": "PRIMO"},
    {"file": "meme_159.png", "top": "En la reunion: Y vos de que trabajas?", "bottom": "Yo: Invierto. Ellos: Ah millonario? Yo: No.", "grad_top": "#081818", "grad_bottom": "#103030", "accent": "#03dac6", "sep": "arrow", "icon": "WORK"},
    {"file": "meme_160.png", "top": "Mi novia: Deja el telefono un rato", "bottom": "Yo: Es que BTC esta en un punto clave del RSI", "grad_top": "#180a10", "grad_bottom": "#301a20", "accent": "#ff0266", "sep": "dots", "icon": "NOVIA"},
    {"file": "meme_161.png", "top": "Mis hijos me piden plata", "bottom": "Papa no tiene cash pero tiene 0.003 BTC", "grad_top": "#0a1008", "grad_bottom": "#1a2818", "accent": "#f7dc6f", "sep": "line", "icon": "KIDS"},
    {"file": "meme_162.png", "top": "Le explico DeFi a mi tio", "bottom": "Mi tio: Eso es como los bonos? Yo: No. Bueno si. No.", "grad_top": "#100a18", "grad_bottom": "#201a30", "accent": "#79f7ff", "sep": "arrow", "icon": "TIO"},
    {"file": "meme_163.png", "top": "Mi hermano: Presta que te devuelvo", "bottom": "Yo: No tengo cash pero te mando USDT a Beexo", "grad_top": "#0a100a", "grad_bottom": "#1a201a", "accent": "#4ecdc4", "sep": "dots", "icon": "USDT"},
    {"file": "meme_164.png", "top": "Año nuevo: este anio invierto seriamente", "bottom": "Marzo: tengo 27 memecoins", "grad_top": "#1a1008", "grad_bottom": "#3a2818", "accent": "#ffc947", "sep": "line", "icon": "2026"},
    {"file": "meme_165.png", "top": "Mi amigo: Cripto es una burbuja", "bottom": "The same amigo 2 anios despues: Como compro BTC?", "grad_top": "#0a0810", "grad_bottom": "#1a1020", "accent": "#e94560", "sep": "arrow", "icon": "TOLD U"},
    {"file": "meme_166.png", "top": "Mi companiero de laburo mina cripto", "bottom": "Con la compu de la oficina. El jefe no sabe.", "grad_top": "#10100a", "grad_bottom": "#20201a", "accent": "#bb86fc", "sep": "dots", "icon": "MINING"},
    {"file": "meme_167.png", "top": "Le cuento a mi psicólogo sobre cripto", "bottom": "Ahora los dos necesitamos terapia", "grad_top": "#0a1a18", "grad_bottom": "#1a3030", "accent": "#03dac6", "sep": "line", "icon": "HELP"},
    {"file": "meme_168.png", "top": "Feliz cumple te regalo cripto", "bottom": "3 meses despues: Me debes el regalo", "grad_top": "#1a0808", "grad_bottom": "#3a1818", "accent": "#ff6b6b", "sep": "arrow", "icon": "B-DAY"},
    {"file": "meme_169.png", "top": "Mi abuela me manda cadenas de WhatsApp", "bottom": "Yo le mando alpha de cripto. Estamos iguales.", "grad_top": "#081008", "grad_bottom": "#182018", "accent": "#4ecdc4", "sep": "dots", "icon": "WAPP"},
    {"file": "meme_170.png", "top": "Cuento en la cena que gane en cripto", "bottom": "No cuento que tambien perdi el doble", "grad_top": "#180a18", "grad_bottom": "#301a30", "accent": "#e5b8f4", "sep": "line", "icon": "SHHH"},

    # =============================================
    # CATEGORÍA: BULL / BEAR MARKET (171-190)
    # =============================================
    {"file": "meme_171.png", "top": "El mercado sube 5%", "bottom": "Beexer: Les dije que iba a subir", "grad_top": "#1a1000", "grad_bottom": "#3a2a00", "accent": "#ffc947", "sep": "line", "icon": "+5%"},
    {"file": "meme_172.png", "top": "Elon tuitea sobre un perro", "bottom": "El mercado entero: CAOS TOTAL", "grad_top": "#0a1830", "grad_bottom": "#1a3060", "accent": "#00d2ff", "sep": "dots", "icon": "PUMP"},
    {"file": "meme_173.png", "top": "Bull market: todos somos genios", "bottom": "Bear market: todos somos victimas", "grad_top": "#1a0a10", "grad_bottom": "#3a1a20", "accent": "#e94560", "sep": "arrow", "icon": "CICLO"},
    {"file": "meme_174.png", "top": "Bear market: Nadie habla de cripto", "bottom": "Bull market: Hasta mi verdulero compra BTC", "grad_top": "#0a1020", "grad_bottom": "#1a2040", "accent": "#bb86fc", "sep": "line", "icon": "BULL"},
    {"file": "meme_175.png", "top": "Todo verde por primera vez en meses", "bottom": "No me lo creo. Algo malo va a pasar.", "grad_top": "#0a1a0a", "grad_bottom": "#1a3a1a", "accent": "#4ecdc4", "sep": "dots", "icon": "GREEN"},
    {"file": "meme_176.png", "top": "BTC rompe su ATH", "bottom": "Mi alt de $0.002 sigue en $0.002", "grad_top": "#10100a", "grad_bottom": "#28281a", "accent": "#f7dc6f", "sep": "arrow", "icon": "ATH"},
    {"file": "meme_177.png", "top": "Es bull run dicen todos", "bottom": "Mi portfolio: Permitime dudar", "grad_top": "#0a0a18", "grad_bottom": "#1a1a38", "accent": "#79f7ff", "sep": "line", "icon": "DOUBT"},
    {"file": "meme_178.png", "top": "En el bear market aprendo y acumulo", "bottom": "En el bull market festejo y compro el top", "grad_top": "#1a0818", "grad_bottom": "#3a1030", "accent": "#ff0266", "sep": "dots", "icon": "LEARN"},
    {"file": "meme_179.png", "top": "BTC sube 1%", "bottom": "Yo: Esto es la adopcion masiva ya empezo", "grad_top": "#0a1810", "grad_bottom": "#1a3020", "accent": "#03dac6", "sep": "arrow", "icon": "+1%"},
    {"file": "meme_180.png", "top": "Altseason dicen pero solo BTC sube", "bottom": "Mis alts: nosotras vamos a quedarnos aca abajo", "grad_top": "#1a0a0a", "grad_bottom": "#3a1a1a", "accent": "#ff6b6b", "sep": "line", "icon": "ALTS"},
    {"file": "meme_181.png", "top": "El mercado crashea un domingo a la noche", "bottom": "Yo: ni siquiera puedo sufrir en paz", "grad_top": "#050510", "grad_bottom": "#101020", "accent": "#e5b8f4", "sep": "dots", "icon": "DOM"},
    {"file": "meme_182.png", "top": "Comenzo el bull run dice el youtuber", "bottom": "Lo dijo tambien las ultimas 47 semanas", "grad_top": "#0a100a", "grad_bottom": "#1a281a", "accent": "#ffc947", "sep": "arrow", "icon": "YT"},
    {"file": "meme_183.png", "top": "El halving de BTC va a cambiar todo", "bottom": "Van 6 meses del halving y nada cambio", "grad_top": "#100a10", "grad_bottom": "#201a20", "accent": "#bb86fc", "sep": "line", "icon": "HALV"},
    {"file": "meme_184.png", "top": "En bear: esto va a 0 vendo todo", "bottom": "En bull: esto va al millon compro todo", "grad_top": "#081008", "grad_bottom": "#182018", "accent": "#4ecdc4", "sep": "dots", "icon": "MOOD"},
    {"file": "meme_185.png", "top": "BTC lateraliza 3 meses", "bottom": "Todos: ABURRIDOOOOO", "grad_top": "#10100a", "grad_bottom": "#20201a", "accent": "#f7dc6f", "sep": "arrow", "icon": "FLAT"},
    {"file": "meme_186.png", "top": "Memecoin sube x100 en una semana", "bottom": "Yo lo descubro cuando ya bajo x99", "grad_top": "#1a0a18", "grad_bottom": "#3a1a30", "accent": "#e94560", "sep": "line", "icon": "x100"},
    {"file": "meme_187.png", "top": "Se activa el mercado un feriado", "bottom": "Cripto no descansa nunca y yo tampoco", "grad_top": "#0a1818", "grad_bottom": "#1a3030", "accent": "#00d2ff", "sep": "dots", "icon": "24/7"},
    {"file": "meme_188.png", "top": "Vendi el fondo del bear market", "bottom": "Ahora soy caso de estudio de que NO hacer", "grad_top": "#180810", "grad_bottom": "#381020", "accent": "#ff0266", "sep": "arrow", "icon": "STUDY"},
    {"file": "meme_189.png", "top": "En el proximo bull voy a ser disciplinado", "bottom": "Narrator: No fue disciplinado", "grad_top": "#0a0a10", "grad_bottom": "#1a1a28", "accent": "#79f7ff", "sep": "line", "icon": "NOPE"},
    {"file": "meme_190.png", "top": "Dead cat bounce o inicio de bull?", "bottom": "Nadie sabe. Todos opinan. Yo HODL.", "grad_top": "#0a180a", "grad_bottom": "#1a301a", "accent": "#03dac6", "sep": "dots", "icon": "???"},

    # =============================================
    # CATEGORÍA: COMUNIDAD BEEXO (191-200)
    # =============================================
    {"file": "meme_191.png", "top": "Nuevo en el grupo: Que compro?", "bottom": "200 opiniones distintas en 3 minutos", "grad_top": "#1a1008", "grad_bottom": "#3a2818", "accent": "#ffc947", "sep": "arrow", "icon": "NEW"},
    {"file": "meme_192.png", "top": "Alguien pregunta por soporte en el grupo", "bottom": "Los Beexers: CUIDADO CON LOS DMs", "grad_top": "#0a1020", "grad_bottom": "#1a2040", "accent": "#00d2ff", "sep": "line", "icon": "ALERT"},
    {"file": "meme_193.png", "top": "Admin: No compartan seed phrase", "bottom": "Usuario nuevo: Y si se la mando al admin?", "grad_top": "#1a0a10", "grad_bottom": "#3a1a20", "accent": "#ff6b6b", "sep": "dots", "icon": "NO"},
    {"file": "meme_194.png", "top": "Trivia en el grupo de Beexo", "bottom": "Todos googlear freneticamente y responden", "grad_top": "#100a18", "grad_bottom": "#201a30", "accent": "#bb86fc", "sep": "arrow", "icon": "TRIVIA"},
    {"file": "meme_195.png", "top": "Grupo activo a las 3 de la maniana", "bottom": "Los cripto-adictos nunca dormimos", "grad_top": "#050510", "grad_bottom": "#101020", "accent": "#e5b8f4", "sep": "line", "icon": "3 AM"},
    {"file": "meme_196.png", "top": "Vela verde y el grupo explota", "bottom": "Vela roja y el grupo queda en silencio", "grad_top": "#0a1510", "grad_bottom": "#1a3020", "accent": "#4ecdc4", "sep": "dots", "icon": "CHAT"},
    {"file": "meme_197.png", "top": "100 mensajes sin leer en el grupo", "bottom": "90 son sobre si va a subir o bajar", "grad_top": "#10100a", "grad_bottom": "#28281a", "accent": "#f7dc6f", "sep": "arrow", "icon": "x100"},
    {"file": "meme_198.png", "top": "Alguien pone LFG en el grupo", "bottom": "Los boomers: Que significa eso?", "grad_top": "#0a0a18", "grad_bottom": "#1a1a38", "accent": "#79f7ff", "sep": "line", "icon": "LFG"},
    {"file": "meme_199.png", "top": "Beexo es mi red social principal", "bottom": "Instagram? X? No. Grupo de Telegram.", "grad_top": "#1a0a18", "grad_bottom": "#3a1a30", "accent": "#03dac6", "sep": "dots", "icon": "TG"},
    {"file": "meme_200.png", "top": "Los Beexers somos comunidad", "bottom": "Ganamos juntos perdemos juntos lloramos juntos", "grad_top": "#0a1818", "grad_bottom": "#1a3030", "accent": "#e94560", "sep": "arrow", "icon": "FAM"},
]
