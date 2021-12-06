from datetime import datetime

import mysql.connector
import tkinter.messagebox

database = mysql.connector.connect(
  host="triton.towson.edu",
  user="acochr5",
  password="COSC*8z32u",
  database="acochr5db",
  port= '3360'
)


class Error(Exception):
  """Base class for other exceptions"""
  pass


class DistributionNotExist(Error):
  """Raised when there is no Distribution_ID"""
  pass

# select a list from the database, return list
def selectListQuery(sql):
  cursor = database.cursor()
  cursor.execute(sql)
  list = cursor.fetchall()
  list = [i[0] for i in list]
  return list

# Det distros
def getDistros(filters):
  sql = "SELECT * FROM DISTRIBUTION"
  sqlFilters = ""
  for i, param in enumerate(filters):
    if(i == 0):
      sqlFilters += ' WHERE '
    else:
      sqlFilters += ' AND '
    # Date Filter
    if(param[0] == 'Date'):
      sqlFilters += f"YEAR(Date) LIKE '{param[1]}'"
    # Region Filter
    if(param[0] == 'regions'):
      sqlFilters += f"Fname IN (SELECT Name FROM FACILITY WHERE R_Name = '{param[1]}')"
    # Facility Name Filter
    if(param[0] == 'facilities'):
      sqlFilters += f"Fname = '{param[1]}'"
    # taxonomic group filter
    if(param[0] == 'taxGroups'):
      sqlFilters += f"S_ITIS IN (SELECT ITIS_NUMBER FROM SPECIES WHERE taxonomic_group = '{param[1]}')"
    # life stages filter (TODO: rn this only checks the released table.. needs to also check transfer)
    if(param[0] == 'lifeStages'):
      if(param[1] == 'Egg'):
        sqlFilters += """(Distribution_ID NOT IN (SELECT Distribution_ID FROM RELEASED WHERE HID) 
        AND Distribution_ID NOT IN (SELECT Distribution_ID FROM TRANSFER WHERE HID))"""
      else:
        sqlFilters += f"""((Distribution_ID IN (SELECT Distribution_ID FROM RELEASED WHERE HID IN (
          SELECT HID FROM HATCHED_DISTRIBUTION WHERE life_stage = '{param[1]}'))) OR (Distribution_ID IN (SELECT Distribution_ID
          FROM TRANSFER WHERE HID IN (SELECT HID FROM HATCHED_DISTRIBUTION WHERE life_stage = '{param[1]}'))))"""
    # species filter
    if(param[0] == 'species'):
      sqlFilters += f"S_ITIS = (SELECT ITIS_NUMBER FROM SPECIES WHERE Name = '{param[1]}')"
    
  sql += sqlFilters + ';'
  print(sql)
  cursor = database.cursor()
  cursor.execute(sql)
  return cursor.fetchall()
      
    # TODO: test 'sqlFilters' with multiple selections then add it to 'sql, make sure to add ';' and stuff'

# Distribution ID
def getDistroID():
  sql = "SELECT Distribution_ID FROM DISTRIBUTION"
  return selectListQuery(sql)

def getITIS():
  sql = "SELECT ITIS_NUMBER FROM SPECIES"
  return selectListQuery(sql)

def getReleased(d_id):
  cursor = database.cursor()
  cursor.execute(f"SELECT * FROM RELEASED WHERE Distribution_ID = %s;", (d_id, ))
  return cursor.fetchall()

def getTransfer(d_id):
  cursor = database.cursor()
  cursor.execute(f"SELECT * FROM TRANSFER WHERE Distribution_ID = %s;", (d_id, ))
  return cursor.fetchall()


def getHatch(h_id):
  cursor = database.cursor()
  cursor.execute(f"SELECT * FROM HATCHED_DISTRIBUTION WHERE HID = %s;", (h_id, ))
  return cursor.fetchall()

def getTagged(h_id):
  cursor = database.cursor()
  cursor.execute(f"SELECT * FROM TAGGED_DISTRIBUTION WHERE HID = %s;", (h_id, ))
  return cursor.fetchall()

# Distribution ID
def getSingleDistro(d_id):
  cursor = database.cursor()
  cursor.execute(f"SELECT * FROM DISTRIBUTION WHERE Distribution_ID = %s;", (d_id, ))
  return cursor.fetchall()

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
  '''SQL INJECTION CAN HAPPEN HERE'''
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
  '''SQL INJECTION CAN HAPPEN HERE'''
  sql = f"SELECT Name FROM SPECIES WHERE taxonomic_group = '{taxGroup}'"
  if(taxGroup == None):
    sql = "SELECT Name FROM SPECIES"
  return selectListQuery(sql)


# insert new distro
def newDistro(date, count, facility, itis, hatched=False, life_stage='Egg', len=None, weight=None):
  '''SQL INJECTION CAN HAPPEN HERE'''
  sql = f"INSERT INTO DISTRIBUTION (Date, Count, Fname, S_ITIS) VALUES ('{date}', {count}, '{facility}', {itis});"
  if(hatched):
      sql = (f"BEGIN {sql} INSERT INTO HATCHED_DISTRIBUTION (Average_length, life_stage, Average_weight, HID) " 
             "VALUES ('{len}', '{life_stage}, '{weight}', last_insert_id())")
  cursor = database.cursor()
  cursor.execute(sql)
  database.commit


# get distribution
def duplicateDistro(d_id):
  # -1 error
  # 1 released distribution
  # 2 transfer distribution

  #initialized type to error
  type = -1
  isHatched = False
  isTagged = False
  hatched = None
  cursor = database.cursor()
  cursor.execute(f"SELECT * FROM DISTRIBUTION WHERE Distribution_ID = %s;", (d_id, ))
  result = cursor.fetchall()

  if(len(result)==0):
    tkinter.messagebox.showerror("Database Error", f"Distribution {d_id} does not exist")
    return type
  else:
    cursor.execute(f"SELECT * FROM RELEASED WHERE Distribution_ID = %s;", (d_id, ))
    releasedResult = cursor.fetchall()
    cursor.execute(f"SELECT * FROM TRANSFER WHERE Distribution_ID = %s;", (d_id, ))
    transferResult = cursor.fetchall()
    if(len(transferResult)!=0&len(releasedResult)==0):
      type=2
      hatched = transferResult[0][2]
    elif(len(releasedResult)!=0&len(transferResult)==0):
      type=1
      hatched = releasedResult[0][3]
    if hatched is not None:
      cursor.execute(f"SELECT * FROM HATCHED_DISTRIBUTION WHERE HID= %s;", (hatched, ))
      hatchedResult = cursor.fetchall()
      cursor.execute(f"SELECT * FROM TAGGED_DISTRIBUTION WHERE HID=%s;", (hatched, ))
      taggedResult = cursor.fetchall()
      if(type==1 or type==2):
        isHatched = True
      if(len(taggedResult)!=0):
        isTagged = True

  if type!=-1:
    cursor.execute("INSERT INTO DISTRIBUTION (Date, Count, Fname, S_ITIS) VALUES (%s,%s,%s,%s);",
                   (result[0][0].strftime('%Y-%m-%d'), result[0][1], result[0][2], result[0][4]))
    if type==1:
      cursor.execute("INSERT INTO RELEASED (Distribution_ID, Latitude, Longitude) VALUES (LAST_INSERT_ID(), "
                     "%s,%s);",(releasedResult[0][1],releasedResult[0][2]))
    if type==2:
      # cursor.execute(f"INSERT INTO TRANSFER (Distribution_ID, F_Name) VALUES (LAST_INSERT_ID(), "
      #                f"'{transferResult[0][1]}');")
      cursor.execute("INSERT INTO TRANSFER (Distribution_ID, F_Name) VALUES (LAST_INSERT_ID(), %s);", (transferResult[0][1], ))

    if isHatched:
      cursor.execute("INSERT INTO HATCHED_DISTRIBUTION (Average_length, Average_weight, life_stage) VALUES (%s,%s,%s)",
                     (hatchedResult[0][0],hatchedResult[0][1],hatchedResult[0][3]))

      if type==1:
        cursor.execute("UPDATE RELEASED SET HID = LAST_INSERT_ID() WHERE DISTRIBUTION_ID = (SELECT MAX(DISTRIBUTION_ID) "
                       "FROM DISTRIBUTION);")
      if type==2:
        cursor.execute("UPDATE TRANSFER SET HID = LAST_INSERT_ID() WHERE DISTRIBUTION_ID = (SELECT MAX(DISTRIBUTION_ID) "
                       "FROM DISTRIBUTION);")

      if isTagged:
        cursor.execute("INSERT INTO TAGGED_DISTRIBUTION (tag_type, percent_tagged, HID) VALUES (%s, %s, LAST_INSERT_ID()"
                       ");",(taggedResult[0][0],taggedResult[0][1]))

    database.commit()
    tkinter.messagebox.showinfo("Database Success", "Successfully duplicated distribution!")
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
  isReleased = False
  isTransfer = False
  isHatched = False
  isTagged = False
  hid = None
  try:
    cursor = database.cursor()
    cursor.execute("SELECT * FROM DISTRIBUTION WHERE DISTRIBUTION_ID = %s;", (d_id, ))
    result = cursor.fetchall()
    if(len(result)==0):
      raise DistributionNotExist
    cursor.execute("SELECT * FROM RELEASED WHERE Distribution_ID = %s;", (d_id, ))
    releasedResult = cursor.fetchall()
    print(releasedResult)
    if(len(releasedResult)!=0):
      isReleased = True
      print(releasedResult)
      hid = releasedResult[0][3]
    cursor.execute("SELECT * FROM TRANSFER WHERE Distribution_ID = %s;", (d_id, ))
    transferResult=cursor.fetchall()
    if(len(transferResult)!=0):
      isTransfer = True
      print(transferResult)
      hid = transferResult[0][2]
    if hid is not None:
      isHatched = True
      cursor.execute("SELECT * FROM TAGGED_DISTRIBUTION WHERE HID = %s;", (hid, ))
      if cursor.fetchall() != 0:
        isTagged = True

    if isTagged:
      cursor.execute("DELETE FROM TAGGED_DISTRIBUTION WHERE HID = %s;", (hid, ))
    if isReleased:
      cursor.execute("DELETE FROM RELEASED WHERE Distribution_ID = %s;", (d_id, ))
    if isTransfer:
      cursor.execute("DELETE FROM TRANSFER WHERE Distribution_ID = %s;", (d_id, ))
    if isHatched:
      cursor.execute("DELETE FROM HATCHED_DISTRIBUTION WHERE HID = %s;", (hid, ))

    cursor.execute("DELETE FROM DISTRIBUTION WHERE Distribution_ID = %s;", (d_id, ))
    database.commit()
    tkinter.messagebox.showinfo("Database Success", f"Successfully deleted distribution ID {d_id}!")
  except mysql.connector.Error as err:
    tkinter.messagebox.showerror("Database Error", err)
  except DistributionNotExist:
    tkinter.messagebox.showerror("Database Error", f"Distribution {d_id} does not exist in the database")

def editDistro(distroVals, subVals, d_id):
  try:
    cursor = database.cursor()
    cursor.execute("UPDATE DISTRIBUTION SET Date = %s, Count = %s, Fname = %s, S_ITIS=%s "
                   "WHERE Distribution_ID = %s;", (distroVals['calendar'], distroVals['count'],
                                                    distroVals['facilities'], distroVals['ITIS'], d_id ))
    if(subVals['latitude'] is not None):
      cursor.execute("UPDATE RELEASED SET Latitude = %s, Longitude = %s "
                     "WHERE Distribution_ID = %s;", (subVals['latitude'],subVals['longitude'], d_id))
      cursor.execute(f"SELECT HID FROM RELEASED WHERE Distribution_ID = %s", (d_id, ))
      h_id = cursor.fetchall()
    else:
      cursor.execute(f"UPDATE TRANSFER SET F_Name = %s WHERE Distribution_ID = %s;",
                     (subVals['transferFacility'], d_id))
      cursor.execute(f"SELECT HID FROM TRANSFER WHERE Distribution_ID = %s;", (d_id, ))
      h_id = cursor.fetchall()
    if(subVals['length'] is not None):
      cursor.execute(f"UPDATE HATCHED_DISTRIBUTION SET Average_length = %s, Average_weight = "
                     f"%s WHERE HID = %s;", (subVals['length'],subVals['weight'],h_id[0][0] ))
      if(subVals['tagged'] is not None):
        cursor.execute(f"UPDATE TAGGED_DISTRIBUTION SET percent_tagged = %s WHERE HID = %s", (subVals['tagged'],h_id[0][0] ))
    database.commit()
    tkinter.messagebox.showinfo("Database Success", f"Successfully updated distribution ID {d_id}!")
  except mysql.connect.Error as err:
    tkinter.messagebox.showerror("Database Error", err)

def isReleased(d_id):
  cursor = database.cursor()
  cursor.execute("SELECT * FROM RELEASED WHERE Distribution_ID = %s;", (d_id, ))
  result = cursor.fetchall()
  print(result)
  if(len(result)!=0):
    return True;
  else:
    return False;

