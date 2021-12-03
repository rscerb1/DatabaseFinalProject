from datetime import datetime

import mysql.connector
import tkinter.messagebox

# database = mysql.connector.connect(
#   host="triton.towson.edu",
#   user="acochr5",
#   password="COSC*8z32u",
#   database="acochr5db",
#   port= '3360'
# )

database=mysql.connector.connect(
  user="acochr5",
  password="COSC*8z32u",
  host="triton.towson.edu",
  port=3360,
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


# get distribution
def distroExists(d_id):
  # -1 error
  # 0 doesn't exist
  # 1 released distribution
  # 2 transfer distribution
  # 3 released distribution hatched
  # 4 transfer distribution hatched
  # 5 released distribution tagged hatched
  # 6 transfer distribution tagged hatched

  #initialized type to error
  type = -1
  cursor = database.cursor()
  cursor.execute(f"SELECT * FROM DISTRIBUTION WHERE Distribution_ID = '{d_id}';")
  result = cursor.fetchall()

  if(len(result)==0):
    type=0
  else:
    cursor.execute(f"SELECT * FROM RELEASED WHERE Distribution_ID = {d_id};")
    releasedResult = cursor.fetchall();
    cursor.execute(f"SELECT * FROM TRANSFER WHERE Distribution_ID = {d_id};")
    transferResult = cursor.fetchall();
    if(len(releasedResult)==0&len(transferResult)!=0):
      type=2
      hatched = transferResult[0][2]
    elif(len(releasedResult)!=0&len(transferResult)==0):
      type=1
      hatched = releasedResult[0][3]

    if hatched is not None:
      cursor.execute(f"SELECT * FROM HATCHED_DISTRIBUTION WHERE HID={hatched};")
      hatchedResult = cursor.fetchall()
      cursor.execute(f"SELECT * FROM TAGGED_DISTRIBUTION WHERE HID={hatched};")
      taggedResult = cursor.fetchall()
      if(type==1):
        type=3
      elif(type==2):
        type=4
      if(len(taggedResult)!=0 & type==4):
        type=6
      elif(len(taggedResult)!=0 & type==3):
        type=5

  if type!=-1:
    cursor.execute("INSERT INTO DISTRIBUTION (Date, Count, Fname, S_ITIS) VALUES (%s,%s,%s,%s);",
                   (result[0][0].strftime('%Y-%m-%d'), result[0][1], result[0][2], result[0][4]))
    tkinter.messagebox.showinfo("Database Success", "Successfully duplicated distribution!")
    #ask if we make this so it takes hatched, or not
    database.commit()
  else:
    tkinter.messagebox.showerror("Database Error", "Was not able to duplicate distribution")
  return type

def addSpecies(is_recreational, is_aquatic, ITIS, taxonomic_group, name):
  try:
    cursor = database.cursor()
    cursor.execute("INSERT INTO SPECIES (is_recreational, is_aquatic, ITIS_NUMBER, taxonomic_group, Name) VALUES (%s,"
                   "%s,%s,%s,%s);",(is_recreational, is_aquatic, ITIS, taxonomic_group, name))
    database.commit()
    tkinter.messagebox.showinfo("Database Success", "Successfully added species!")
  except mysql.connector.Error as err:
    tkinter.messagebox.showerror("Database Error", err)

def deleteDistro(d_id):
  try:
    cursor = database.cursor()
    cursor.execute(f"DELETE FROM DISTRIBUTION WHERE Distribution_ID = {d_id};")
    database.commit()
    tkinter.messagebox.showinfo("Database Success", f"Successfully deleted distribution ID {d_id}!")
  except mysql.connector.Error as err:
    tkinter.messagebox.showerror("Database Error", err)