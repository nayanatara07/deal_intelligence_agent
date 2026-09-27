import sqlite3

conn = sqlite3.connect(r'C:\Users\USER\source\repos\deal_intelligence_agent\data\deals.db')
cursor = conn.cursor()

cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
print('Tables:', cursor.fetchall())

cursor.execute('SELECT COUNT(*) FROM deals')
print('Deal count:', cursor.fetchone())

cursor.execute('SELECT id, company, value FROM deals LIMIT 5')
print('Sample deals:', cursor.fetchall())

cursor.execute('SELECT COUNT(*) FROM calls')
print('Call count:', cursor.fetchone())

conn.close()
