class BookDTO:
    """This class is a data transfer object. It contains the attributes for one record in database.
    It contains any additional variable required to maintain the state of the DTO
    or any variable required for the functionalities. """
    def __init__(self):
        """This is the constructor method. """
        self.book_ISBN = ''
        self.book_name = ''
        self.book_writer = ''
        self.book_genre = ''
        # Flag to indicate state of the record. It is initiated as new indicating that
        # it is a new record to be inserted into database.
        self.store_flag = 'new'

    def get_as_list(self):
        """This method returns the attributes of the record as a list of string variables. """
        return [str(self.book_ISBN),
                self.book_name,
                self.book_writer,
                self.book_genre]

    def __str__(self):
        """This is to override the __str__ method of the object. This will be called wherever a print version of
        the object is requested.
        This method returns the details as a joined up string, separated by ','"""
        return ', '.join(self.get_as_list())
