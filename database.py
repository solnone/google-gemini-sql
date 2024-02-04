import sqlite3


def create_table_insert_data(cursor):
    # Create table
    table_info = '''
    create table if not exists student(
        NAME VARCHAR(25),
        CLASS VARCHAR(25),
        SECTION VARCHAR(25),
        SCORE INT
    );
    '''
    cursor.execute(table_info)

    row_count = cursor.execute('''select count(*) from student''').fetchone()[0]
    if row_count:
        print(f"Row count: {row_count}")
    else:
        # Insert Some more records
        cursor.execute('''insert into student values('Krish','Data Science','A',90)''')
        cursor.execute('''insert into student values('Sudhanshu','Data Science','B',100)''')
        cursor.execute('''insert into student values('Darius','Data Science','A',86)''')
        cursor.execute('''insert into student values('Vikash','DEVOPS','A',50)''')
        cursor.execute('''insert into student values('Dipesh','DEVOPS','A',35)''')


def main():
    # Connect to SQlite
    connection = sqlite3.connect("student.db")

    # Create a cursor object to insert record, create table
    cursor = connection.cursor()

    create_table_insert_data(cursor)

    # Display ALl the records
    print("The inserted records are")
    data = cursor.execute('''select * from student''')

    names = list(map(lambda x: x[0], cursor.description))
    print(names)

    for row in data:
        print(row)

    # Commit your changes in the database
    connection.commit()
    connection.close()


if __name__ == '__main__':
    main()
