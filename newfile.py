import sqlite3 as m 
con= m.connect('fooddetails.db')
cursor1=con.cursor()

#cursor.execute('create table newone (wname char,nosets integer,weightsused , repsdone )')

def insertdata(a,b,c):
    print(a,b,c)
    cursor.execute('''insert into data1 (id,name,class) values ('{}','{}','{}')''' .format(a,b,c))
    
def save():
    con.commit()
    
tablenameq = '''select name from sqlite_master where type='table'; '''  #names of existing tables in db

def desctable(x):
    cursor1.execute('''pragma table_info('%s')''' %x)    #formattedstring
    print(cursor1.fetchall())
   
def fetch():
    print(cursor.fetchall()) 


complete=''
while not complete:
    userinput=input()
    if userinput=='done':
        complete=True
    else:     
        Foodname=input('Foodname: ')
        Protein=float(input('Protein: '))   
        Carbs=float(input('Carbs: '))
        Fat= float(input('Fat: '))
        Calories=int(input('Calories: '))          
        cursor1.execute(f' insert into foods values(?,?,?,?,?)',(Foodname,Protein,Carbs,Fat,Calories))
        con.commit()

cursor1.execute('''select * from foods ''')
print(cursor1.fetchall())