import sqlite3 as m

conn=m.connect('test2.db')
conn2=m.connect('test3.db')
conn3=m.connect('fooddetails.db')
cursor2=conn2.cursor()
cursor1=conn.cursor()
cursor3=conn3.cursor()
import datetime

from prettytable import from_db_cursor


def save():
    conn.commit()
    
def save2():
    conn2.commit()   

def save3():
    conn3.commit()    
            
def getdate(a):
    error= True
    while error is True:        
            try:
                if a == 'today':      
                    y= datetime.datetime.now()
                    return y.strftime('%d/%m/%Y')
                    error=False
                    
                else:
                    y = int(a)
                    date='_/_/_'
                    date='%s/_/_ ' %y
                    print(date)
                    b=int(input('Enter date: '))
                    date='%s/%s/_' %(a,b)
                    print(date)
                    c=int(input('Enter date: '))
                    date='%s/%s/%s' %(y,b,c)
                    print(date)
                    error = False
                    return date          
            except ValueError:
                print("Enter integers only")
                error = True
                

def logging():        
        command=''
        print('_/_/_')
        command=input('''Enter workout date or enter 'today' if you want to log todays workout: ''')
        try:
            seshdate = getdate(command)
            cursor1.execute('''create table '%s' (wname, noofsets, weightsused, repsdone)''' %seshdate)
            insertingworkout(seshdate)
        except m.OperationalError:
            print('Log for this name already exists. Delete or add to existing log')

def insertingworkout(seshdate):
    complete=False
    while not complete:
        wname=input('''Enter workout name:  or 'done' ''')
        if wname =='done':
             complete=True
        else:
             noset=int(input('Enter number of sets: '))
             weightsused=[]
             repsdone=[]
             for i in range(noset):
                 x=input('Enter weight used in set%s: ' %(i+1))
                 y=input('Enter reps done in set%s: '%(i+1) )
                 weightsused.append(x)
                 repsdone.append(y)
            
             sweightsused=''
             srepsdone=''
             for i in weightsused:
                 sweightsused+='%s kgs '%i
             for i in repsdone:    
                 srepsdone+= '%s reps ' %i                       
    
             cursor1.execute('''insert into '%s' values('%s', '%s', '%s', '%s')''' %(seshdate, wname, noset, sweightsused, srepsdone))


def showtableinfo(x):
    cursor1.execute('''select * from '%s' ''' %x)
    y = from_db_cursor(cursor1)
    print(y)
 
    
def showtableinfo2(x):
    cursor2.execute('''select * from '%s' ''' %x)
    y = from_db_cursor(cursor2)
    print(y) 
 
                         
def showtables():
    cursor1.execute('''select name from sqlite_master where type='table';''') 
    a=cursor1.fetchall() 
    for i in a:
        print(i[0])  

      
def showtables2():
    cursor2.execute('''select name from sqlite_master where type='table';''')
    a= cursor2.fetchall()
    for i in a:
        print(i[0])
    
 
def collectmacros(mealname, Qty):
         cursor3.execute('''select Protein, Carbs, Fat, Calories from foods where Foodname=='%s'  ''' %mealname)
         a = cursor3.fetchall()         
         r = a[0][0] * Qty
         x = a[0][1] *Qty
         y = a[0][2] * Qty
         z = a[0][3] * Qty
         return round(r, 1),round(x,1),round(y,1), z                                                                          

def   insertingmeal(mealdate):
  complete=''
  while not complete:  
      x=input('''Enter time of meal, Breakfast, Lunch, Snacks, Dinner or 'done': ''')
      tom=x.title()  
      if tom == 'Done':
         complete=True 
      else:
          done=''
          while not done:
              x=input('''Enter mealname or 'done': ''')
              mealname=x.title()
              if mealname=='Done':
                  done=True
              else:
                  Qty=int(input('Enter Qty:  '))
                  Protein, Carbs, Fat, Calories= collectmacros(mealname, Qty)
                  cursor2.execute('''insert into '%s' values('%s','%s','%s','%s','%s','%s','%s')''' %(mealdate, mealname.title(), Qty, tom, Protein, Carbs, Fat, Calories))
                  save2()    



print('SpotmyChad')   #program starts here


while exit != 1:
    print('\nEnter 1 to proceed with Gym log feature \nEnter 2 to proceed with Calorie Tracking Feature \nEnter 3 to exit ')
    command=input()
    if command=='1':
        command=input('\nEnter 1 to log a NEW workout \nEnter 2 to VIEW previous workout logs \nEnter 3 to DELETE existing log\nEnter 4 to ADD to existing log\nEnter 5 to go BACK: '  )
                    
        if command == '1':
                        logging()
                        save()
                        
                            
                                
                       
                        
                 
                        
                                                                                                                               
        elif command=='2':
                        showtables()                        
                        tablename=input('Enter the Session date to view its log: ')   
                        showtableinfo(tablename)                               
        elif command=='3':
                         print('Delete a existing log')
                         showtables()
                         seshdate = input('Enter date of session you want to delete: ')
                         showtableinfo(seshdate)
                         confirmation = input('Are you sure you want to delete this log? Y/N: ')
                         if confirmation == 'y' or 'Y':
                               cursor1.execute('''drop table '%s' ''' %seshdate )
                               print('Log deleted succesfully')
                         else:
                               print("No log deleted") 
                               continue      
        elif command == '4':
            showtables()
            seshdate= input('Enter date of session you want to add to: ')
            showtableinfo(seshdate)
            insertingworkout(seshdate)
            showtableinfo(seshdate)
            save()                       
        elif command=='5':
            continue
        else:
                         print('Enter valid command')
         
        
        
    
    
    
    elif command=='2':
        command=input('\nEnter 1 to proceed with NEW Log \nEnter 2 to ADD to existng log \nEnter 3 to VIEW summary\nEnter 4 to DELETE existing log\nEnter 5 to go BACK  ')
        if command =='1':
            print('\nNew Log\n')
            print('_/_/_')
            mealdate= getdate(input('''Enter date or 'today: '''))
            cursor2.execute('''create table '%s' (Fname varchar(10), Qty integer, Tom, Protein float, Carbs float, Fat float, Calories integer)''' %mealdate)
            insertingmeal(mealdate)
            showtableinfo2(mealdate)
                                                      
                    
            
            
            
        elif command=='2':            
            print('\nAdd to existing log\n')
            showtables2()
            mealdate = input('Enter date of log you want to add to:  ')
            showtableinfo2(mealdate)
            insertingmeal(mealdate)
            showtableinfo2(mealdate)
            
            
            
        elif command=='3':
            print('View summary')
            showtables2()
            mealdate=input('Enter the record date:  ')
            showtableinfo2(mealdate)
            totalcal=0
            cursor2.execute('''select Calories from '%s' ;''' %mealdate) 
            x = cursor2.fetchall()
            for i in x:
                totalcal += int(i[0])
               

            totalprotein=0
            cursor2.execute('''select Protein from '%s' ''' %mealdate)
            x = cursor2.fetchall()
            for i in x:
                totalprotein += int(i[0])

            totalcarbs=0
            cursor2.execute('''select Carbs from '%s' ''' %mealdate)
            x = cursor2.fetchall()
            for i in x:
                totalcarbs += int(i[0])


            totalfat=0
            cursor2.execute('''select Fat from '%s' ''' %mealdate)
            x = cursor2.fetchall()
            for i in x:
                totalfat += int(i[0])
            
            print('Total calories: ', totalcal)
            print('Total Protein: ', totalprotein)
            print('Total Carbs: ', totalcarbs)  
               
                                                                                                                                                                                                                                                                                
            proteincal = 4*totalprotein
            carbscal = 4*totalcarbs
            fatcal = 9*totalfat
            others= totalcal - (proteincal+carbscal+fatcal)     
                                                                                                                                                                                                                                                                                                                            
        elif command =='4':
            showtables2()
            mealdate=input('Enter date of log to delete:  ')
            showtableinfo2(mealdate)
            confirmation= input('Are you sure you want to delete ? Y/N ')
            if confirmation == 'Y' or 'y':
                cursor2.execute('''drop table '%s' ''' %mealdate)
                print("Log deleted succesfully")
            else:
                  continue
                  
        elif command=='5':
                continue
        else:
           print('Enter valid command')   
              
                                         
    elif command=='3':
        exit =1
    
    else:
        print('Invalid command \nEnter either 1 or 2')   