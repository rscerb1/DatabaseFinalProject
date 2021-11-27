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
  list = [i[0] for i in list]
  return list

# Fiscal Years List
def getYears():
  sql = ""
  return selectListQuery(sql)
  
# Region Names List
def getRegions():
  sql = ""
  return selectListQuery(sql)

# Facility Names List
def getFacilities():
  sql = f"SELECT NAME FROM FACILITY;"
  return selectListQuery(sql)

# Taxonomic Groups list
def getTaxGroups():
  sql = f"SELECT DISTINCT taxonomic_group FROM SPECIES;"
  return selectListQuery(sql)

# Life Stages List
def getLifeStages():
  sql = ""
  return selectListQuery(sql)

# Species List
def getSpecies():
  sql = ""
  return selectListQuery(sql)


# insert new distro
def newDistro(date, count, facility, itis, hatched=False, life_stage='Egg', len=None, weight=None):
  sql = f"INSERT INTO DISTRIBUTION (Date, Count, Fname, S_ITIS) VALUES ('{date}', {count}, '{facility}', {itis});"
  if(hatched):
      sql = (f"BEGIN {sql} INSERT INTO HATCHED_DISTRIBUTION (Average_length, life_stage, Average_weight, HID) " 
             "VALUES ('{len}', '{life_stage}, '{weight}', last_insert_id())")
  cursor = database.cursor()
  cursor.execute(sql)
  database.commit

  