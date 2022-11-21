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
            
def getdate():
    y=''
    print('_/_/_')
    a=input('''Enter workout date number by number starting with day number\nor enter 'today' if you want to log todays workout: ''')
    if a == 'today':      
        y= datetime.datetime.now()
        return y.strftime('%d/%m/%Y')                   
    else:                   
        try:
            y = int(a)
        except ValueError:
            print("\nEnter integers only") #\u001b[31m
            
        if type(y) == int:    
            #date='_/_/_'
            date='%s/_/_ ' %y
            print(date)
            b=int(input('Enter number of month: '))
            date='%s/%s/_' %(a,b)
            print(date)
            c=int(input('Enter number of year: '))
            date='%s/%s/%s' %(y,b,c)
            print(date)
            return date          
                

def logging():
    seshdate=''               
        #try:
    while True:
        try:
            seshdate = getdate()        
            cursor1.execute('''create table '%s' (wname, noofsets, weightsused, repsdone)''' %seshdate)
        except m.OperationalError:
            print('\nCheck if a log for this date already exists\nor make sure you made a valid input\n')
            continue
        else:
            break
    insertingworkout(seshdate)
            

def insertingworkout(seshdate):
    noset=0
    while True:
        wname=input('''Enter workout name:  or 'done' ''')
        if wname =='done':
             break
        else:
            while True:
                x=input('Enter number of sets: ')
                if x =='done':
                    break
                else:
                    try:
                        noset=int(x)
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
                        break
                    except:
                        print('Enter integers only')
            


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
      tom=input('''Enter time of meal, Breakfast, Lunch, Snacks, Dinner or 'done': ''').title()        
      if tom == 'Done':
         complete=True 
      else:
          done=''
          while not done:
              mealname=input('''Enter mealname or 'done': ''').title()              
              if mealname=='Done':
                  done=True
              else:
                  Qty=int(input('Enter Qty:  '))
                  Protein, Carbs, Fat, Calories= collectmacros(mealname, Qty)
                  cursor2.execute('''insert into '%s' values('%s','%s','%s','%s','%s','%s','%s')''' %(mealdate, mealname, Qty, tom, Protein, Carbs, Fat, Calories))
                  save2()    



print('SpotmyChad')   #program starts here


while exit != 1:
    command=input('\nEnter 1 to proceed with Gym log feature \nEnter 2 to proceed with Calorie Tracking Feature \nEnter 3 to exit: ')
    if command=='1':
        command=input('\nEnter 1 to log a NEW workout \nEnter 2 to VIEW previous workout logs \nEnter 3 to DELETE existing log\nEnter 4 to ADD to existing log\nEnter 5 to go BACK: '  )
                    
        if command == '1':
                        logging()
                        save()
                        
                                                                                                                                                           
        elif command=='2':
            showtables()
            while True:
                tablename=input('Enter the Session date to view its log: ')
                if tablename == 'done':
                    break
                else:
                    try:   
                        showtableinfo(tablename)
                        break
                    except:
                        print('No such table exist. Make sure you typed correctly')                               
        
        
        elif command=='3':
                        print('Delete a existing log')
                        showtables()
                        done=''
                        while True:
                            try:
                                seshdate = input('Enter date of session you want to delete: ')
                                if seshdate =='done':
                                    done=True
                                    break
                                else:                        
                                    showtableinfo(seshdate)
                                    break
                            except:
                                print('No such table exist. Make sure you typed correctly')    
                        
                        while True:
                            if done is True:
                                break
                            confirmation = input('Are you sure you want to delete this log? Y/N: ').lower()
                            if confirmation == 'y':
                                cursor1.execute('''drop table '%s' ''' %seshdate )
                                print('Log deleted succesfully')
                                break
                            elif confirmation == 'n':
                                print("No log deleted")                                 
                                break
                            else:
                                print("Enter either y/n")      
        elif command == '4':
            showtables()
            while True:
                try:                
                    seshdate= input('Enter date of session you want to add to: ')
                    if seshdate == 'done':
                        break
                    else:        
                        showtableinfo(seshdate)
                        break
                except:
                    print('No such table exist. Make sure you typed correctly')
            if seshdate != 'done':            
                insertingworkout(seshdate)
                showtableinfo(seshdate)
                save()                       
        elif command=='5':
            continue
        else:
                         print('Enter valid command')
         
        
        
    
    
    
    elif command=='2':
        command=input('\nEnter 1 to proceed with NEW Log \nEnter 2 to ADD to existng log \nEnter 3 to VIEW summary\nEnter 4 to DELETE existing log\nEnter 5 to go BACK: ')
        if command =='1':
            print('\nNew Log\n')
            while True:
                try:
                    if mealdate=='done':
                        break
                    else:
                        mealdate= getdate()
                        cursor2.execute('''create table '%s' (Fname varchar(10), Qty integer, Tom, Protein float, Carbs float, Fat float, Calories integer)''' %mealdate)
                        break
                except:
                    print('\nCheck if a log for this date already exists\nor make sure you made a valid input\n')

            insertingmeal(mealdate)
            showtableinfo2(mealdate)
                                                      
                    
            
            
            
        elif command=='2':            
            print('\nAdd to existing log\n')
            showtables2()
            while True:
                try:                
                    mealdate= input('Enter date of log you want to add to:  ')
                    if mealdate == 'done':
                        break
                    else:        
                        showtableinfo2(mealdate)
                        break
                except:
                    print('No such table exist. Make sure you typed correctly')
            if mealdate != 'done':            
                insertingmeal(mealdate)
                showtableinfo2(mealdate)
                save2()
            
            
            
        elif command=='3':
            print('View summary')
            showtables2()
            while True:
                mealdate=input('Enter the record date:  ')
                if mealdate == 'done':
                    break
                else:
                    try:   
                        showtableinfo2(mealdate)
                        break
                    except:
                        print('No such table exist. Make sure you typed correctly')
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
            done=''
            while True:
                try:
                    mealdate=input('Enter date of log to delete:  ')
                    if mealdate =='done':
                        done=True
                        break
                    else:                        
                        showtableinfo2(mealdate)
                        break
                except:
                    print('No such table exist. Make sure you typed correctly') 

            while True:
                if done is True:
                    break
                confirmation= input('Are you sure you want to delete ? Y/N ').lower() 
                if confirmation == 'y':
                    cursor2.execute('''drop table '%s' ''' %mealdate)
                    print('Log deleted succesfully')
                    break
                elif confirmation == 'n':
                    print("No log deleted")                                 
                    break
                else:
                    print("Enter either y/n") 
                  
        elif command=='5':
                continue
        else:
           print('Enter valid command')   
              
                                         
    elif command=='3':
        exit=1
    
    else:
        print('Invalid command \nEnter either 1 or 2')   