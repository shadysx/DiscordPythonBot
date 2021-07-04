import sqlite3

db = sqlite3.connect('members.db')



cur = db.cursor()
cur.execute("UPDATE members set score = 0")
cur.execute("SELECT * FROM members")

result = cur.fetchall()
print(result)

#Pour utiliser le resultat d'un select comme un dict
#db.row_factory = sqlite3.Row
#result = cur.fetchall()
#for member in result:
#    print(member['id'], member['pseudo'], member['score'])

db.commit()
db.close()
