import psycopg2

db = psycopg2.connect(database="music", user="postgres", password="1111", host='localhost')
cursor = db.cursor()

# with open('create.sql', 'r') as script:
#     lines = script.readlines()
#
# cursor.execute('\n'.join(lines))
# db.commit()

# cursor.execute("""
# ALTER TABLE track DISABLE TRIGGER ALL;
# """)
# cursor.execute('alter table track alter artist drop not null')

cursor.execute('select * from track')
db.commit()
print(cursor.fetchall())

cursor.close()
db.close()
