"""Test de detección de pedidos de imagen."""
from image_tools import detect_image_request

tests = [
    # NO debe detectar (preguntas normales)
    ("busca en x cuando sera la proxima beexo radio", None),
    ("busca en google que es bitcoin", None),
    ("busca informacion sobre ethereum", None),
    ("mostra el precio de btc", None),
    ("pasa el link del sitio", None),
    ("manda un saludo al grupo", None),
    ("haceme un favor", None),
    ("poneme al dia con las noticias", None),
    ("quiero ver el precio de btc", None),
    # SEARCH - piden imagen/foto explícitamente con verbo genérico
    ("buscame una foto de cr7", "search"),
    ("buscame una imagen de bitcoin", "search"),
    ("mostrame una foto de un gato", "search"),
    ("mandame una imagen de ethereum", "search"),
    ("haceme una imagen de messi", "search"),
    ("haceme una foto de la luna", "search"),
    ("quiero una imagen de la luna", "search"),
    ("quiero una foto de bitcoin", "search"),
    ("foto de un atardecer", "search"),
    ("una imagen de bitcoin", "search"),
    ("pasame una foto de elon musk", "search"),
    # GENERATE - solo verbos de creación visual
    ("generame un dinosaurio minando btc", "generate"),
    ("dibuja un perro astronauta", "generate"),
    ("dibujame a messi", "generate"),
    ("genera una vaca en la luna", "generate"),
    ("ilustrame un dragon", "generate"),
    ("diseñame un logo cripto", "generate"),
]

ok = 0
fail = 0
for text, expected in tests:
    result = detect_image_request(text)
    action = result[0] if result else None
    status = "OK" if action == expected else "FAIL"
    if action != expected:
        fail += 1
        print(f"  FAIL: \"{text}\" -> {action} (esperado: {expected})")
    else:
        ok += 1
        print(f"  OK:   \"{text}\" -> {action}")

print(f"\n{ok}/{ok+fail} tests pasaron")
if fail:
    print(f"{fail} tests fallaron")
