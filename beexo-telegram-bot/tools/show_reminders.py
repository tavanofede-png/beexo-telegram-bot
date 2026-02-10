import sqlite3
from ai_chat import DB_PATH
from datetime import datetime

try:
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM reminders")
    cnt = cur.fetchone()[0]
    print('reminders_count:', cnt)
    cur.execute("SELECT id, user_name, text, scheduled_at, fired FROM reminders ORDER BY scheduled_at DESC LIMIT 10")
    rows = cur.fetchall()
    for r in rows:
        id, user_name, text, scheduled_at, fired = r
        dt = datetime.utcfromtimestamp(scheduled_at).isoformat() if scheduled_at else 'NULL'
        print(id, user_name, 'fired=' + str(fired), dt, text[:120])
except Exception as e:
    print('ERROR', e)
finally:
    try:
        conn.close()
    except:
        pass
