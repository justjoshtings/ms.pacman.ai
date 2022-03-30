import mysql.connector

with open('mysql_config.txt','r') as f:
    mysql_pw = str(f.read()).strip()

mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password=mysql_pw,
        database="mspacmanai"
        )

mycursor = mydb.cursor()

# recent_game_score = -30

# query = f"INSERT INTO stats_table(game_score) VALUES ({recent_game_score});"

# mycursor.execute(query)

# mydb.commit()

print(mycursor.rowcount, "record inserted.")

mycursor.execute("SELECT * FROM stats_table;")

myresult = mycursor.fetchall()

for row in myresult:
    print(row)
