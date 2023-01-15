import tkinter
from tkinter import *
from tkinter import ttk
from tkinter.messagebox import showinfo

from mysql.connector import Error

# Import the other classes in the package
from bookrecords import SQLHandler
from bookrecords import BookDTO


class BookEntry:
    """This class contains the methods to support inserting new book details into the database.
    This class contains the methods to render the UI elements and to handle user input. """

    def __init__(self):
        """This is the constructor method.
        It initializes the class variables required to support the functionality."""
        self.input_book_ISBN = None
        self.input_book_name = None
        self.input_book_writer = None
        self.input_book_genre = None
        self.store_flag_variable = None

    def show_fields(self):
        """This method renders the screen elements for user to input details and submit. """
        # Reset Tk surface
        surface.destroy()
        surface.__init__()
        # Set dimension as appropriate for the contained elements and the position of the root surface..
        surface.geometry('500x500+20+10')
        # Assign title for the dialog window
        surface.title("Enter new book details")

        # Create a container for the ISBN field.
        book_ISBN_container = ttk.LabelFrame(surface, text="Enter book ISBN")
        # Create the ISBN entry field
        self.input_book_ISBN = Text(book_ISBN_container, height=20, width=100)
        # Pack to the container
        self.input_book_ISBN.pack()
        # Place the container on the surface with required height and width.
        book_ISBN_container.place(x=30, y=50, height=40, width=400)

        # Similar to the ISBN container and entry field, create the field to capture book name.
        book_name_container = ttk.LabelFrame(surface, text="Enter book name")
        self.input_book_name = Text(book_name_container, height=20, width=300)
        self.input_book_name.pack()
        book_name_container.place(x=30, y=100, height=40, width=400)

        # Create container and field to capture writer name.
        book_writer_container = ttk.LabelFrame(surface, text="Enter book writer")
        self.input_book_writer = Text(book_writer_container, height=20, width=300)
        self.input_book_writer.pack()
        book_writer_container.place(x=30, y=150, height=40, width=400)

        # Create container and field to capture book genre.
        book_genre_container = ttk.LabelFrame(surface, text="Enter book genre")
        self.input_book_genre = Text(book_genre_container, height=20, width=300)
        self.input_book_genre.pack()
        book_genre_container.place(x=30, y=200, height=40, width=400)

        # Create a Submit button to store the details. Call "save_book_record" method when clicked.
        Button(surface, text='Submit', command=self.save_book_record,
               width=15, bg='brown', fg='white').place(x=70, y=260)

        # Create a Back button to go back to selection screen.
        # Call "show_fields" method of BookManagement class when clicked.
        Button(surface, text='Back', command=show_fields,
               width=15, bg='brown', fg='white').place(x=260, y=260)

        # Create a StringVar variable for containing any message to user.
        self.store_flag_variable = StringVar(surface)
        self.store_flag_variable.set('Enter new book details and click Submit to save.')
        result_label = Label(surface, textvariable=self.store_flag_variable,
                             font=("bold", 10), wraplength=300, justify="left")
        result_label.place(x=30, y=300)

        # Render the dialog box with all fields
        surface.mainloop()

    def validate_entry(self):
        """This method validates whether the required input is given in the entry fields"""
        # Use "get" method of field to retrieve the field value. Use "end-1c" as the end position
        if self.input_book_ISBN.get(1.0, "end-1c") == "" \
                or self.input_book_name.get(1.0, "end-1c") == "" \
                or self.input_book_writer.get(1.0, "end-1c") == "" \
                or self.input_book_genre.get(1.0, "end-1c") == "":
            # Return false if any of the fields is left blank
            return False
        else:
            # Return true if all details are present
            return True

    def save_book_record(self):
        """This method is called when user clicks on submit.
        This method will call necessary class the method to store the data into database. """
        # Check whether required data are entered by calling "validate_entry" method.
        if self.validate_entry():
            # Create DTO instance to pass to database method.
            book_data = BookDTO()
            # Store the UI field values into the DTO
            book_data.book_ISBN = self.input_book_ISBN.get(1.0, "end-1c")
            book_data.book_name = self.input_book_name.get(1.0, "end-1c")
            book_data.book_writer = self.input_book_writer.get(1.0, "end-1c")
            book_data.book_genre = self.input_book_genre.get(1.0, "end-1c")

            # Create instance of the SQLHandler class from package.
            # This will initiate the connection to database.
            sql_handler = SQLHandler()
            # Enclose the SQLHandler call within try and except to handle any uncaught error
            try:
                # Call "insert_book_to_db" method of SQLHandler and store the returned DTO
                book_data = sql_handler.insert_book_to_db(book_data)
                # Check the flag in the returned DTO.
                # If the DTO is successfully stored, proceed to empty the entry fields again.
                if book_data.store_flag == "inserted":
                    self.input_book_ISBN.delete(1.0, "end-1c")
                    self.input_book_ISBN.insert("end-1c", "")
                    self.input_book_name.delete(1.0, "end-1c")
                    self.input_book_name.insert("end-1c", "")
                    self.input_book_writer.delete(1.0, "end-1c")
                    self.input_book_writer.insert("end-1c", "")
                    self.input_book_genre.delete(1.0, "end-1c")
                    self.input_book_genre.insert("end-1c", "")

                    # Show message to user confirming that data is saved.
                    self.store_flag_variable.set('Entry saved!\nEnter new book details and click Submit to save.')
                elif book_data.store_flag == "duplicate":
                    # Check if the data is detected as duplicate and update the message to user.
                    self.store_flag_variable.set('Entry failed! This ISBN already exists.\n'
                                                 'Enter new book details and click Submit to save.')
                else:
                    # For any other status in returned DTO flag, show message that storing failed.
                    self.store_flag_variable.set('Entry failed! Please contact tech support.\n'
                                                 'Or try to enter new book details and click Submit again to save.')
            except Error as e:
                # Handle any uncaught exception
                print("Error while executing", e)
            finally:
                # Close the connection with database
                sql_handler.close_connection()

            print('Saved')
        else:
            # Show message that all details are required if validation fails.
            self.store_flag_variable.set('Please provide all details.\n'
                                         'Enter new book details and click Submit to save.')


class BookMonitor:
    """This class contains the methods to support inserting new book details into the database.
    This class contains the methods to render the UI elements and to handle user input. """

    def __init__(self):
        """This is the constructor method"""
        self.input_book_ISBN = None
        self.input_book_name = None
        self.input_book_writer = None
        self.input_book_genre = None
        self.store_flag_variable = None

    def show_fields(self):
        """This method renders the UI elements for user to input search criteria,
        buttons to choose the function and to display the records. """
        # Reset Tk surface
        surface.destroy()
        surface.__init__()
        # Set the dimension of the root surface and the position of the root surface.
        surface.geometry('900x700+20+10')
        # Assign title for the dialog window
        surface.title("View recorded book details")

        # Create a container for the ISBN field.
        book_ISBN_container = ttk.LabelFrame(surface, text="Enter book ISBN")
        # Create the ISBN entry field
        self.input_book_ISBN = Text(book_ISBN_container, height=20, width=100)
        # Pack to the container
        self.input_book_ISBN.pack()
        # Place the container on the surface with required height and width.
        book_ISBN_container.place(x=30, y=50, height=40, width=400)

        # Similar to the ISBN container and entry field, create the field to capture book name.
        book_name_container = ttk.LabelFrame(surface, text="Enter book name")
        self.input_book_name = Text(book_name_container, height=20, width=300)
        self.input_book_name.pack()
        book_name_container.place(x=30, y=100, height=40, width=400)

        # Create container and field to capture writer name.
        book_writer_container = ttk.LabelFrame(surface, text="Enter book writer")
        self.input_book_writer = Text(book_writer_container, height=20, width=300)
        self.input_book_writer.pack()
        book_writer_container.place(x=30, y=150, height=40, width=400)

        # Create container and field to capture book genre.
        book_genre_container = ttk.LabelFrame(surface, text="Enter book genre")
        self.input_book_genre = Text(book_genre_container, height=20, width=300)
        self.input_book_genre.pack()
        book_genre_container.place(x=30, y=200, height=40, width=400)

        # Create a Search button to search with the entered details.
        # Call "search_book_record" method when clicked.
        Button(surface, text='Search', command=self.search_book_record,
               width=15, bg='brown', fg='white').place(x=30, y=260)
        # Create a button to show all records. Call "show_book_record" method when clicked.
        Button(surface, text='Show all (500)', command=self.show_book_records,
               width=15, bg='brown', fg='white').place(x=175, y=260)

        # Create a Back button to go back to selection screen.
        # Call "show_fields" method of BookManagement class when clicked.
        Button(surface, text='Back', command=show_fields,
               width=15, bg='brown', fg='white').place(x=315, y=260)

        # Create a StringVar variable for containing any message to user.
        self.store_flag_variable = StringVar(surface)
        self.store_flag_variable.set('Enter search details and click "Search" to find the book.\n'
                                     'Click "Show all" to show the first 500 entries.')
        result_label = Label(surface, textvariable=self.store_flag_variable,
                             font=("bold", 10), wraplength=700, justify="left")
        result_label.place(x=30, y=300)

        # Render the dialog box with all fields
        surface.mainloop()

    def validate_entry(self):
        """This method validates whether the required input is given in the entry fields"""
        # Use "get" method of field to retrieve the field value. Use "end-1c" as the end position
        if self.input_book_ISBN.get(1.0, "end-1c") == "" \
                and self.input_book_name.get(1.0, "end-1c") == "" \
                and self.input_book_writer.get(1.0, "end-1c") == "" \
                and self.input_book_genre.get(1.0, "end-1c") == "":
            # Return false when all fields are left blank.
            return False
        else:
            # Return true when at least one field has value entered for search
            return True

    def search_book_record(self):
        """This method is called when user clicks on Search.
        This method will call necessary class and method to search in database. """
        # Validate if the required data are input in the criteria fields
        if self.validate_entry():
            # Read the data from the entry fields and store into a DTO instance
            book_data = BookDTO()
            # Read with the Get method of entry fields and by using position range between 1 and end-1c
            book_data.book_ISBN = self.input_book_ISBN.get(1.0, "end-1c")
            book_data.book_name = self.input_book_name.get(1.0, "end-1c")
            book_data.book_writer = self.input_book_writer.get(1.0, "end-1c")
            book_data.book_genre = self.input_book_genre.get(1.0, "end-1c")

            # Create SQLHandler instance. This initiates the connection to database
            sql_handler = SQLHandler()
            # Enclose the SQLHandler call with try and except
            try:
                # Call search_book_on_db() method to get a list of results from database matching the criteria
                books = sql_handler.search_book_on_db(book_data)

                # Create a LabelFrame for the results
                book_results = ttk.LabelFrame(surface, text="Records found")
                # Place the frame mentioning the position and the dimension
                book_results.place(x=30, y=300, height=280, width=850)

                # Define columns with the first DTO instance in the list.
                # Use the get_as_list method to get a list from the DTO
                columns = books[0].get_as_list()

                # Create a TreeView representation within the LabelFrame area. Use the columns as headings.
                tree = ttk.Treeview(book_results, columns=tuple(columns), show='headings')
                # define headings texts with same value from the columns list
                for column in columns:
                    tree.heading(column, text=column)
                    # Place the heading as center aligned
                    tree.column(column, anchor=CENTER)

                # Check if there are results returned
                if len(books) > 1:
                    # Get the data from index 1. 0 was the column headers.
                    for book_data in books[1::]:
                        # Insert each record by converting the list from DTO into a tuple.
                        tree.insert('', tkinter.END, values=tuple(book_data.get_as_list()))

                # Create a method which will handle the event when one row of the TreeView is clicked.
                def item_selected(event):
                    for selected_item in tree.selection():
                        item = tree.item(selected_item)
                        record = str(item['values'])
                        # show a message
                        showinfo(title='Information', message=''.join(record))

                # Bind the method with TreeViewSelect event.
                tree.bind('<<TreeviewSelect>>', item_selected)

                # Place the TreeView at 0,0 position and stacking from top left.
                tree.grid(row=0, column=0, sticky='NSEW')

                # add a vertical scrollbar to the LabelFrame
                scrollbar = ttk.Scrollbar(book_results, orient=tkinter.VERTICAL, command=tree.yview)
                tree.configure(yscrollcommand=scrollbar.set)
                # Stack the scrollbar on right side
                scrollbar.grid(row=0, column=1, sticky='NS')
            except Error as e:
                # Catch any unexpected error
                print("Error while executing", e)
            finally:
                # Close the connection
                sql_handler.close_connection()

    def show_book_records(self):
        """This method is called when user clicks on Show All.
        This method will call necessary class and method to retrieve from database. """
        # Create SQLHandler instance. This initiates the connection to database
        sql_handler = SQLHandler()
        # Enclose the SQLHandler call with try and except
        try:
            # Call get_all_books() method to get list of all records from database
            books = sql_handler.get_all_books()

            # Create a LabelFrame for the results
            book_results = ttk.LabelFrame(surface, text="Records found")
            # Place the frame mentioning the position and the dimension
            book_results.place(x=30, y=300, height=280, width=850)

            # define columns with the first DTO instance in the list.
            # Use the get_as_list method to get a list from the DTO
            columns = books[0].get_as_list()

            # Create a TreeView representation within the LabelFrame area. Use the columns as headings.
            tree = ttk.Treeview(book_results, columns=tuple(columns), show='headings')
            # define headings texts with same value from the columns list
            for column in columns:
                tree.heading(column, text=column)
                # Place the heading as center aligned
                tree.column(column, anchor=CENTER)

            # Check if there are results returned
            if len(books) > 1:
                # Get the data from index 1. 0 was the column headers.
                for book_data in books[1::]:
                    # Insert each record by converting the list from DTO into a tuple.
                    tree.insert('', tkinter.END, values=tuple(book_data.get_as_list()))

            # Create a method which will handle the event when one row of the TreeView is clicked.
            def item_selected(event):
                for selected_item in tree.selection():
                    item = tree.item(selected_item)
                    record = str(item['values'])
                    # show a message
                    showinfo(title='Information', message=''.join(record))

            # Bind the method with TreeViewSelect event.
            tree.bind('<<TreeviewSelect>>', item_selected)

            # Place the TreeView at 0,0 position and stacking from top left.
            tree.grid(row=0, column=0, sticky='NSEW')

            # add a vertical scrollbar to the LabelFrame
            scrollbar = ttk.Scrollbar(book_results, orient=tkinter.VERTICAL, command=tree.yview)
            tree.configure(yscrollcommand=scrollbar.set)
            # Stack the scrollbar on right side
            scrollbar.grid(row=0, column=1, sticky='NS')
        except Error as e:
            # Catch any unexpected error
            print("Error while executing", e)
        finally:
            # Close the connection
            sql_handler.close_connection()


# Initiate a global Tk surface so that multiple classes can access
surface = Tk()


def show_fields():
    """This method renders the screen elements for user to select mode of usage of the tool. """
    # Reset and initiate the Tk surface
    surface.destroy()
    surface.__init__()
    # Set dimension as appropriate for the contained elements and the position of the root surface..
    surface.geometry('500x120+20+10')
    # Assign title for the dialog window
    surface.title("Select mode of usage")

    # Create instances of the two classes used for the two modes.
    book_entry = BookEntry()
    book_monitor = BookMonitor()
    # Create a button to show the entry related screen.
    Button(surface, text='Book entry', command=book_entry.show_fields,
           width=15, bg='brown', fg='white').place(x=100, y=40)
    # Create a button to show the monitoring related screen.
    Button(surface, text='Book Monitor', command=book_monitor.show_fields,
           width=15, bg='brown', fg='white').place(x=250, y=40)

    # Render the dialog box with all fields
    surface.mainloop()


# Check whether the tool is executed from command
if __name__ == '__main__':
    # Initiate method to display screen components
    show_fields()
