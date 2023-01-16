import mysql.connector
from mysql.connector import Error
from bookrecords.booksdto import BookDTO


class SQLHandler:
    """This class contains the variables and methods to interact with database through SQL queries. """

    def __init__(self):
        """This is the constructor method. It initiates the connection instance with the database. """
        try:
            # Create the connection instance as a class level variable by calling "connect" method
            # and supplying the connection details and credentials.
            self.connection = mysql.connector.connect(host='localhost',
                                                      port='3306',
                                                      database='pythonapps',
                                                      user='pythonuser',
                                                      password='Welcome1')
            if self.connection.is_connected():
                db_Info = self.connection.get_server_info()
                print("Connected to MySQL Server version ", db_Info)

        # Handle exception if connectivity fails
        except Error as e:
            print("Error while connecting to MySQL", e)

    def create_book_table(self):
        """This method handles creation of the required table in database. """
        # Check that the connection is already established.
        # If not, call the class constructor to initiate connection.
        if not self.connection.is_connected():
            self.__init__()
        # Get cursor from connection.
        cursor = self.connection.cursor()
        # Set the creation query as a variable. Notice that the query itself checks for existence of the table.
        # Checking the existence of the table in database is cheaper than checking in application.
        # Set the "book_ISBN" attribute as the primary key
        create_query = "CREATE TABLE IF NOT EXISTS books (\
                          book_ISBN VARCHAR(20) NOT NULL,\
                          book_name VARCHAR(100) NOT NULL,\
                          book_writer VARCHAR(100) NOT NULL,\
                          book_genre VARCHAR(100) NOT NULL,\
                          PRIMARY KEY (book_ISBN));"
        # Enclose database call within try and except block
        try:
            # Execute the create query
            cursor.execute(create_query)
            # Return true to indicate that creation was successful
            return True
        except Error as e:
            print("Error while creating table", e)
            # Close the cursor if error.
            cursor.close()
            # Return false on failure
            return False

    def insert_book_to_db(self, book_data):
        """This method handles inserting a new record into database.
        It takes a DTO as input which contains the required details for the record. """
        # Check that the data been passed as input is a new record to be inserted into database.
        if book_data.store_flag == "new":
            # Set the insertion query as a variable.
            # Use placeholders for the values.
            # The values will be passed with a parameter to the cursor.execute method as a tuple.
            # This way, SQL injection will be avoided by passing the values through MySQL library method.
            insert_query = "INSERT INTO books " \
                           "(book_ISBN, book_name, book_writer, book_genre) " \
                           "VALUES (%s, %s, %s, %s)"
            
            # Always call the create_book_table method to create the table.
            # Checking whether the table exists or not is handled within create_book_table method.
            if self.create_book_table():
                # Get cursor instance.
                cursor = self.connection.cursor()
                # Enclose the database call within try and except
                try:
                    # Execute the insert query
                    cursor.execute(insert_query, tuple(book_data.get_as_list()))
                    # Remember to commit if successful
                    self.connection.commit()
                    # Set the flag in the DTO to indicate that storing was successful
                    book_data.store_flag = "inserted"
                except Error as e:
                    # Check for duplicate record.
                    # Checking through database failure is cheaper as we can check with single database call.
                    # The error number 1062 is specific to duplicate record failure if primary key (book_ISBN)
                    # is already present.
                    if e.errno == 1062:
                        print("Error while inserting record - duplicate record", e)
                        # Close the cursor
                        cursor.close()
                        # Set the flag in DTO to indicate failure due to duplicate record.
                        book_data.store_flag = "duplicate"
                    else:
                        # For other errors, close the cursor and set the DTO flag as normal failure.
                        # If further specific failures need to be captured, the best way would be to check
                        # the error number and handle like duplicate record block.
                        print("Error while inserting record", e)
                        cursor.close()
                        book_data.store_flag = "insert failed"
            else:
                # Set flag in DTO if creation of table itself had failed.
                book_data.store_flag = "create failed"
        # Return the DTO with the flag set
        return book_data

    def get_all_books(self):
        """This method handles retrieving all the records in the database table. """
        # Create a list for the records. This will be a list of the DTO objects
        all_books = []
        # Set the query as a variable
        get_all_query = "SELECT * FROM books LIMIT 0,500"
        # Get the cursor instance
        cursor = self.connection.cursor()
        # Enclose the database call within try and except
        try:
            # Execute the query
            cursor.execute(get_all_query)
            # Get the field names from the result
            field_names = [i[0] for i in cursor.description]
            # get all records
            records = cursor.fetchall()
            print("Total number of rows in table: ", cursor.rowcount)
            # Insert the field names as first row in the records to be returned.
            records.insert(0, field_names)
            print("\nPrinting each row")
            # Temp DTO variable for each record
            # book_data = None
            for row in records:
                # Temp DTO variable for each record
                book_data = BookDTO()
                book_data.book_ISBN = row[0]
                book_data.book_name = row[1]
                book_data.book_writer = row[2]
                book_data.book_genre = row[3]
                all_books.append(book_data)
        except Error as e:
            # Catch exception and close the cursor
            print("Error while reading data", e)
            cursor.close()
        # Return the list of DTOs
        return all_books

    def close_connection(self):
        """This method closes the connection instance in the class. """
        # Check if the connection is active and close it.
        if self.connection.is_connected():
            self.connection.close()
            print("MySQL connection is closed")

    def search_book_on_db(self, book_data):
        """This method handles retrieving records matching the search criteria.
        The search criteria is passed as a DTO"""
        # Create a list for the records. This will be a list of the DTO objects
        all_books = []
        # Count of criteria needed to form the query correctly
        criteria_count = 0
        # Create the query as a variable.
        search_query = "SELECT * FROM books WHERE "
        # Check if the attribute is present in the criteria and append to the search query.
        # Use the counter to determine whether to append "AND" between criteria
        if book_data.book_ISBN != '':
            search_query += 'book_ISBN = ' + book_data.book_ISBN
            criteria_count += 1
        if book_data.book_name != '':
            if criteria_count > 0:
                search_query += ' AND '
            search_query += 'book_name = "' + book_data.book_name + '"'
            criteria_count += 1
        if book_data.book_writer != '':
            if criteria_count > 0:
                search_query += ' AND '
            search_query += 'book_writer = "' + book_data.book_writer + '"'
            criteria_count += 1
        if book_data.book_genre != '':
            if criteria_count > 0:
                search_query += ' AND '
            search_query += 'book_genre = "' + book_data.book_genre + '"'
            criteria_count += 1
        # Get the cursor instance
        cursor = self.connection.cursor()
        # Enclose the database call within try and except
        try:
            # Execute the query
            cursor.execute(search_query)
            # Get the field names from the result
            field_names = [i[0] for i in cursor.description]
            # get all records
            records = cursor.fetchall()
            print("Total number of rows in table: ", cursor.rowcount)
            # Insert the field names as first row in the records to be returned.
            records.insert(0, field_names)
            print("\nPrinting each row")
            # book_data = None
            # Iterate through the records and append to the list of DTOs
            for row in records:
                # Temp DTO variable for each record
                book_data = BookDTO()
                book_data.book_ISBN = row[0]
                book_data.book_name = row[1]
                book_data.book_writer = row[2]
                book_data.book_genre = row[3]
                all_books.append(book_data)
        except Error as e:
            # Catch exception and close the cursor
            print("Error while reading data", e)
            cursor.close()
        # Return the list of DTOs
        return all_books


# To run this program as standalone and test the methods, sample code can be executed as below.
# Check whether the is executed from command
if __name__ == '__main__':
    sql_handler = SQLHandler()
    book_dto = BookDTO()
    book_dto.book_ISBN = '123456'
    book_dto.book_name = 'Harry Potter and Prisoner of Azkaban'
    book_dto.book_writer = 'J K Rowling'
    book_dto.book_genre = 'Fiction'
    book_dto.store_flag = 'new'
    try:
        book_dto = sql_handler.insert_book_to_db(book_dto)
        print('store_flag ->', book_dto.store_flag)
        books = sql_handler.get_all_books()
        print('Books ->', *books)
    except Error as e:
        print("Error while executing", e)
    finally:
        sql_handler.close_connection()
