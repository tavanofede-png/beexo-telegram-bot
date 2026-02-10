import os, sqlite3
DB = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'beexy_history.db')
DOC = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'BeeXy_Bot_Documentacion.html')

print('DB ->', DB)
print('DOC ->', DOC)

conn = sqlite3.connect(DB)
cur = conn.cursor()
try:
    cur.execute("CREATE VIRTUAL TABLE IF NOT EXISTS kb_docs USING fts5(title, content, source)")
except Exception as e:
    print('FTS create error:', e)

try:
    with open(DOC, 'r', encoding='utf-8', errors='ignore') as f:
        raw = f.read()
    cur.execute('INSERT INTO kb_docs (title, content, source) VALUES (?, ?, ?)', (os.path.basename(DOC), raw[:200000], 'docs'))
    conn.commit()
    print('Inserted raw doc into kb_docs')
except Exception as e:
    print('Insert error:', e)

# verify
try:
    q='BeeXy'
    cur.execute('SELECT title, substr(content,1,200), source FROM kb_docs WHERE kb_docs MATCH ? LIMIT 3', (q,))
    for r in cur.fetchall():
        print('---')
        print(r[0], r[2])
        print(r[1])
except Exception as e:
    print('Query error:', e)

conn.close()
