import sqlite3
from ai_chat import _log_interaction, DB_PATH

# Insertar interacción de prueba
_log_interaction(999999, "tester_py", "¿Esto es una prueba?", "Respuesta de prueba desde script")

# Leer y mostrar las últimas 5 interacciones
conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()
cur.execute("SELECT id, user_id, user_name, question, answer, created_at FROM interactions ORDER BY id DESC LIMIT 5")
rows = cur.fetchall()
for r in rows:
    print(r)
conn.close()
