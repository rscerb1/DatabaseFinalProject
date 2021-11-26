import mysql.connector

database = mysql.connector.connect(
  host="localhost",
  user="python",
  password="12qwaszx",
  database="acochr5db"
)

# select a list from the database, return list
def selectListQuery(sql):
  cursor = database.cursor()
  cursor.execute(sql)
  list = cursor.fetchall()
  return list

# facility list
def getFacilities():
    sql = f"SELECT NAME FROM FACILITY;"
    list = selectListQuery(sql)
    list = [i[0] for i in list]
    return list
