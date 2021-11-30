import mysql.connector

# database = mysql.connector.connect(
#   host="triton.towson.edu",
#   user="acochr5",
#   password="COSC*8z32u",
#   database="acochr5db",
#   port= '3360'
# )

database = mysql.connector.connect(
  host="localhost",
  user="python",
  password="12qwaszx",
  database="dbproj"
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
  sql = "SELECT DISTINCT YEAR(DATE) FROM DISTRIBUTION"
  dates = selectListQuery(sql)
  years = []
  for x in dates:
    years.append(x)
  return years
  
# Region Names List
def getRegions():
  sql = "SELECT Name FROM REGION"
  return selectListQuery(sql)

# Facility Names List
def getFacilities(region = None):
  sql = f"SELECT NAME FROM FACILITY WHERE R_Name = '{region}';"
  if(region == None):
    sql = f"SELECT NAME FROM FACILITY;"
  return selectListQuery(sql)

# Taxonomic Groups list
def getTaxGroups():
  sql = f"SELECT DISTINCT taxonomic_group FROM SPECIES;"
  return selectListQuery(sql)

# Species List
def getSpecies(taxGroup = None):
  sql = f"SELECT Name FROM SPECIES WHERE taxonomic_group = '{taxGroup}'"
  if(taxGroup == None):
    sql = "SELECT Name FROM SPECIES"
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
