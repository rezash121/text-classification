import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="",
  database="docs"
)
# print(mydb)
mycursor = mydb.cursor()

for i in range(1,2501):
    print(i)
    fileHandler= open("dataset/%s.txt"%i)
    listOfLines = fileHandler.readlines()
    dateFound=False
    categoryFound=False
    titleFound=False
    textFound=False
    text=""
    for line in listOfLines:
         if line.strip()!="":
             if line.strip()=="date :":
             #     print("date found")
             # else:
             #     print("date not found!!!!!!!!!!!!!!!!!!!!")
                dateFound=True
                continue
             elif line.strip()=="category :":
                 categoryFound=True
                 continue
             elif line.strip()=="title :":
                 titleFound=True
                 continue
             elif line.strip()=="text :":
                 textFound=True
                 continue
             # print(line.strip())
             if dateFound:
                 # print(line.strip())
                 date=line.strip()
                 dateFound=False
             elif categoryFound:
                 # print(line.strip())
                 category=line.strip()
                 categoryFound=False
             elif titleFound:
                 # print(line.strip())
                 title = line.strip()
                 titleFound = False
             elif textFound:
                 text =text+line.strip()
             # if dateFound and categoryFound and titleFound and textFound:


    print(date)
    print(category)
    print(title)
    print(text)
    # print("date is %s"%line.strip())
    sql = "INSERT INTO documents (id, date,category,title,text) VALUES (%s, %s,%s, %s,%s)"
    val = (i, date,category,title,text)
    mycursor.execute(sql, val)
    dateFound = False
    categoryFound=False
    titleFound=False
    textFound=False

    mydb.commit()

