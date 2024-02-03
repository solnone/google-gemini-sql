import sqlite3

## Connectt to SQlite
connection=sqlite3.connect("student.db")

# Create a cursor object to insert record,create table

cursor=connection.cursor()

## create the table
table_info='''
create table student(
    NAME VARCHAR(25),
    CLASS VARCHAR(25),
    SECTION VARCHAR(25),
    MARKS INT
);
'''
cursor.execute(table_info)

## Insert Some more records

cursor.execute('''insert into student values('Krish','Data Science','A',90)''')
cursor.execute('''insert into student values('Sudhanshu','Data Science','B',100)''')
cursor.execute('''insert into student values('Darius','Data Science','A',86)''')
cursor.execute('''insert into student values('Vikash','DEVOPS','A',50)''')
cursor.execute('''insert into student values('Dipesh','DEVOPS','A',35)''')

## Disspaly ALl the records

print("The isnerted records are")
data=cursor.execute('''Select * from student''')
for row in data:
    print(row)

## Commit your changes int he databse
connection.commit()
connection.close()