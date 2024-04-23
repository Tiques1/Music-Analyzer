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

cursor.execute("""SELECT
    column_name,
    data_type
FROM
    information_schema.columns
WHERE
    table_name = 'track';""")

cursor.execute("""
alter table track drop column year
""")
db.commit()
print(cursor.fetchall())

cursor.close()
db.close()
