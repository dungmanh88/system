import psycopg2 as p

try:
    conn = p.connect("dbname='dvdrentail' user='postgres' host='localhost' password='postgres'")
    cur = conn.cursor()
    cur.execute("""select * from actor order by first_name limit 10""")
    rows = cur.fetchall()
    print("Show me the databases")
    for row in rows:
        print("   ", row[1], "   ", row[2], "   ", row[3])
    cur.close()
    conn.close()
except:
    print("I am unable to connect to the database")
    cur.close()
    conn.close()