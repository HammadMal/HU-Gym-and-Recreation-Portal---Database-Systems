# Importing essential modules
from PyQt6 import QtCore, QtWidgets, uic
from PyQt6.QtCore import QDate
from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QHeaderView,QDateEdit
import sys
import pyodbc


# Replace these with your own database connection details
# server = 'LAPTOP-J9S0E7GT'
# database = 'HU_Project_2'  # Name of your Northwind database
# use_windows_authentication = True  # Set to True to use Windows Authentication
# username = 'sa'  # Specify a username if not using Windows Authentication
# password = 'kurapikastime'  # Specify a password if not using Windows Authentication

server = 'DESKTOP-32FF7E1'
database = 'HU_Project_2'  # Name of your Northwind database
use_windows_authentication = False  # Set to True to use Windows Authentication
username = 'sa'  # Specify a username if not using Windows Authentication
password = 'kurapikastime'  # Specify a password if not using Windows Authentication

# Create the connection string based on the authentication method chosen
if use_windows_authentication:
    connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;'
else:
    connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}'


class LoginScreen(QtWidgets.QMainWindow):

    # This signal informs the main function to open the respective portal.
    open_student_portal_signal = QtCore.pyqtSignal(int)
    open_admin_portal_signal = QtCore.pyqtSignal()

    def __init__(self):
        super(LoginScreen, self).__init__()
        uic.loadUi('Login Screen.ui', self)
        self.pushButton.clicked.connect(self.login)

    def login(self):
        email = self.lineEdit.text()    
        password = self.lineEdit_2.text()

        connection = pyodbc.connect(connection_string)
        cursor = connection.cursor()

        # Check in Admin table
        cursor.execute("SELECT * FROM Admin WHERE Email = ? AND Password = ?", email, password)
        if cursor.fetchone():
            self.open_admin_portal_signal.emit()  # Emit the signal to open the admin portal
            self.close()
            return

        # Check in Student table
        cursor.execute("SELECT StudentID FROM Student WHERE Email = ? AND Password = ?", email, password)
        student_record = cursor.fetchone()
        if student_record:
            self.student_id = student_record[0]
            self.open_student_portal_signal.emit(self.student_id)  # Emit the signal with student_id
            self.close()
            return

        QtWidgets.QMessageBox.warning(self, "Error", "Invalid credentials")

    def open_admin_portal(self):
        admin_portal = AdminPortal()
        admin_portal.show()
        self.close()  # Close the login window
        

    def open_student_portal(self):
        student_portal = StudentPortal()
        student_portal.show()
        self.close()  # Close the login window
        


class AdminPortal(QtWidgets.QMainWindow):
    def __init__(self):
        super(AdminPortal, self).__init__()
        uic.loadUi('admin screen.ui', self)
        self.load_events()

        self.load_teams()

        self.load_locker()

        self.load_gym()

        self.pushButton_12.clicked.connect(self.view_event_details)

        self.pushButton.clicked.connect(self.addadminevent)

        self.pushButton_2.clicked.connect(self.removeevent)

        self.pushButton_5.clicked.connect(self.view_team_details)

        self.pushButton_13.clicked.connect(self.view_approved_teams)

        self.pushButton_3.clicked.connect(self.approve_status)

        self.pushButton_4.clicked.connect(self.removeteams)

        self.pushButton_9.clicked.connect(self.view_locker_details)

        self.pushButton_15.clicked.connect(self.view_approved_lockers)

        self.pushButton_10.clicked.connect(self.approve_locker)

        self.pushButton_11.clicked.connect(self.removelocker)

        self.pushButton_6.clicked.connect(self.view_gym_details)

        self.pushButton_14.clicked.connect(self.view_approved_gym)

        self.pushButton_7.clicked.connect(self.approve_gym)

        self.pushButton_8.clicked.connect(self.removegymmember)


    def load_events(self):
        connection = pyodbc.connect(connection_string)
        cursor = connection.cursor()
        
        # Fetch all columns from the AvailableEvents table
        cursor.execute("SELECT EventID, NameOfEvent, StartDate, EndDate, Supervisor, Organizer FROM AvailableEvents")
        events = cursor.fetchall()
        
        # Assuming that the AvailableEvents table includes more than just EventID and NameOfEvent,
        # you need to set the correct number of columns in the QTableWidget:
        if events:
            num_columns = len(events[0])
            self.tableWidget.setColumnCount(num_columns)
            # If you want to set header labels based on the column names from the database, you can do this:
            columns = [column[0] for column in cursor.description]
            self.tableWidget.setHorizontalHeaderLabels(columns)

        
        
        # Clear the table before inserting new rows
        self.tableWidget.setRowCount(0)
        
        # Populate the table with the event data
        for row_number, row_data in enumerate(events):
            self.tableWidget.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.tableWidget.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(data)))

        cursor.close()
        connection.close()

    def view_event_details(self):
        # Get selected event's ID
        selected_row = self.tableWidget.currentRow()

        if selected_row!=-1:
            event_id = self.tableWidget.item(selected_row, 0).text()
            
            # Fetch event details from the database
            connection = pyodbc.connect(connection_string)
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM AvailableEvents WHERE EventID = ?", event_id)
            event = cursor.fetchone()
            cursor.close()
            connection.close()
            self.event_details_window = EventDetails(event)
            self.event_details_window.show()
        else:
            QtWidgets.QMessageBox.warning(self, "No Row Selected", "Please select an event before viewing details.")
        
        # Show event details in a new window

    def load_teams(self):
        connection = pyodbc.connect(connection_string)
        cursor = connection.cursor()
        
        # Fetch all columns from the AvailableEvents table
        cursor.execute("SELECT TeamID , EventID, NameOfTeam, NoOfPlayers, TeamCaptain, Contact, Status FROM Teams WHERE STATUS=0")
        teams = cursor.fetchall()
        
        # Assuming that the AvailableEvents table includes more than just EventID and NameOfEvent,
        # you need to set the correct number of columns in the QTableWidget:
        if teams:
            num_columns = len(teams[0])
            self.tableWidget_2.setColumnCount(num_columns)
            # If you want to set header labels based on the column names from the database, you can do this:
            columns = [column[0] for column in cursor.description]
            self.tableWidget_2.setHorizontalHeaderLabels(columns)

        
        
        # Clear the table before inserting new rows
        self.tableWidget_2.setRowCount(0)
        
        # Populate the table with the event data
        for row_number, row_data in enumerate(teams):
            self.tableWidget_2.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.tableWidget_2.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(data)))

        cursor.close()
        connection.close()


        # Add admin portal functionalities here


    # def addadminevent(self):

    def addadminevent(self):
        # selected_row = self.tableWidget.currentRow()
        # event_id = self.tableWidget.item(selected_row, 0).text()

        # Open application form
        self.application_form = AddForm(self)
        self.application_form.show()
        self.application_form.application_submitted_signal.connect(self.load_events)

    def removeevent(self):
        # Get the selected row
        selected_row = self.tableWidget.currentRow()

        if selected_row != -1:
            # Get the event ID from the selected row
            event_id = self.tableWidget.item(selected_row, 0).text()

            # Remove the selected row from the QTableWidget
            self.tableWidget.removeRow(selected_row)

            # Update the database to remove the corresponding event
            connection = pyodbc.connect(connection_string)
            cursor = connection.cursor()
            delete_statement = "DELETE FROM AvailableEvents WHERE EventID = ?"

            try:
                cursor.execute(delete_statement, event_id)
                connection.commit()
                QtWidgets.QMessageBox.information(self, "Event Removed", "The event has been removed successfully.")
            except pyodbc.Error as e:
                QtWidgets.QMessageBox.warning(self, "Database Error", f"An error occurred: {e}")
            finally:
                cursor.close()
                connection.close()
        else:
            QtWidgets.QMessageBox.warning(self, "No Row Selected", "Please select an event to remove.")


    def view_team_details(self):
        # Get selected event's ID
        selected_row = self.tableWidget_2.currentRow()

        if selected_row!=-1:
        
        # Fetch event details from the database
            team_id = self.tableWidget_2.item(selected_row, 0).text()
            connection = pyodbc.connect(connection_string)
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM Teams WHERE TeamID = ?", team_id)
            teams = cursor.fetchone()
            cursor.close()
            connection.close()
            
            # Show event details in a new window
            self.event_details_window = viewTeams(teams)
            self.event_details_window.show()
        else:
            QtWidgets.QMessageBox.warning(self, "No Row Selected", "Please select an event to view.")


    def view_approved_teams(self):
        
        # Fetch event details from the database
        
        # Show event details in a new window
        self.event_details_window = viewApprovedTeams()
        self.event_details_window.show()

    def approve_status(self):

        selected_row = self.tableWidget_2.currentRow()

        if selected_row != -1:
            # Get the event ID from the selected row
            team_id = self.tableWidget_2.item(selected_row, 0).text()

            # Update the database to remove the corresponding event
            connection = pyodbc.connect(connection_string)
            cursor = connection.cursor()

            try:
                cursor.execute("UPDATE Teams SET Status = 1 WHERE TeamID = ?", team_id)
                connection.commit()
                new_status_item = QtWidgets.QTableWidgetItem("True")

            # Set the new item in the tableWidget_2
                self.tableWidget_2.setItem(selected_row, 6, new_status_item)
                QtWidgets.QMessageBox.information(self, "Team Approved", "The team status has been updated successfully.")
                self.tableWidget_2.removeRow(selected_row)
            except pyodbc.Error as e:
                QtWidgets.QMessageBox.warning(self, "Database Error", f"An error occurred: {e}")
            finally:
                cursor.close()
                connection.close()
        else:
            QtWidgets.QMessageBox.warning(self, "No Row Selected", "Please select a row to update the status.")

    def removeteams(self):
        # Get the selected row
        selected_row = self.tableWidget_2.currentRow()

        if selected_row != -1:
            # Get the event ID from the selected row
            team_id = self.tableWidget.item(selected_row, 0).text()

            # Remove the selected row from the QTableWidget
            self.tableWidget_2.removeRow(selected_row)

            # Update the database to remove the corresponding event
            connection = pyodbc.connect(connection_string)
            cursor = connection.cursor()
            delete_statement = "DELETE FROM Teams WHERE TeamID = ?"

            try:
                cursor.execute(delete_statement, team_id)
                connection.commit()
                QtWidgets.QMessageBox.information(self, "Team Removed", "The team has been removed successfully.")
            except pyodbc.Error as e:
                QtWidgets.QMessageBox.warning(self, "Database Error", f"An error occurred: {e}")
            finally:
                cursor.close()
                connection.close()
        else:
            QtWidgets.QMessageBox.warning(self, "No Row Selected", "Please select an team to remove.")



    #locker 



    def load_locker(self):
        connection = pyodbc.connect(connection_string)
        cursor = connection.cursor()
        
        # Fetch all columns from the AvailableEvents table
        cursor.execute("SELECT LockerID, Name, StudentID, Registered from Locker where Registered= 0")
        lockers = cursor.fetchall()
        
        # Assuming that the AvailableEvents table includes more than just EventID and NameOfEvent,
        # you need to set the correct number of columns in the QTableWidget:
        if lockers:
            num_columns = len(lockers[0])
            self.tableWidget_4.setColumnCount(num_columns)
            # If you want to set header labels based on the column names from the database, you can do this:
            columns = [column[0] for column in cursor.description]
            self.tableWidget_4.setHorizontalHeaderLabels(columns)
        

        self.tableWidget_4.setRowCount(0)
        
        # Populate the table with the event data
        for row_number, row_data in enumerate(lockers):
            self.tableWidget_4.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.tableWidget_4.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(data)))

        cursor.close()
        connection.close()

    def view_locker_details(self):
        # Get selected event's ID
        selected_row = self.tableWidget_4.currentRow()

        if selected_row!=-1:
            locker_id = self.tableWidget_4.item(selected_row, 0).text()
            
            # Fetch event details from the database
            connection = pyodbc.connect(connection_string)
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM Locker WHERE LockerID = ?", locker_id)
            lock = cursor.fetchone()
            cursor.close()
            connection.close()
            self.event_details_window = viewlocker(lock)
            self.event_details_window.show()
        else:
            QtWidgets.QMessageBox.warning(self, "No Row Selected", "Please select a locker to view.")
        
    def view_approved_lockers(self):
        
        # Fetch event details from the database
        
        # Show event details in a new window
        self.event_details_window = viewApprovedLockers()
        self.event_details_window.show()

    def approve_locker(self):

        selected_row = self.tableWidget_4.currentRow()

        if selected_row != -1:
            # Get the event ID from the selected row
            locker_id = self.tableWidget_4.item(selected_row, 0).text()

            # Update the database to remove the corresponding event
            connection = pyodbc.connect(connection_string)
            cursor = connection.cursor()

            try:
                cursor.execute("UPDATE Locker SET Registered = 1 WHERE LockerID = ?", locker_id)
                connection.commit()
                Registered_val = self.tableWidget_4.item(selected_row, 3).text()
                if Registered_val=="False":
                    new_status_item = QtWidgets.QTableWidgetItem("True")


            # Set the new item in the tableWidget_2
                    self.tableWidget_4.setItem(selected_row, 3, new_status_item)
                    QtWidgets.QMessageBox.information(self, "Locker Approved", "The Locker status has been updated successfully.")
                    self.tableWidget_4.removeRow(selected_row)
                else:
                    QtWidgets.QMessageBox.warning(self, "Locker is already approved", "Registered value cannot be changed.")
            finally:
                cursor.close()
                connection.close()
        else:
            QtWidgets.QMessageBox.warning(self, "No Row Selected", "Please select a row to update the status.")

    def removelocker(self):
        # Get the selected row
        selected_row = self.tableWidget_4.currentRow()

        if selected_row != -1:
            # Get the event ID from the selected row
            locker_id = self.tableWidget_4.item(selected_row, 0).text()

            # Remove the selected row from the QTableWidget
            self.tableWidget_4.removeRow(selected_row)

            # Update the database to remove the corresponding event
            connection = pyodbc.connect(connection_string)
            cursor = connection.cursor()
            delete_statement = "DELETE FROM Locker WHERE LockerID = ?"

            try:
                cursor.execute(delete_statement,  locker_id)
                connection.commit()
                QtWidgets.QMessageBox.information(self, "Student with the corresponding locker removed", "The student has been unassigned from the locker successfully.")
            except pyodbc.Error as e:
                QtWidgets.QMessageBox.warning(self, "Database Error", f"An error occurred: {e}")
            finally:
                cursor.close()
                connection.close()
        else:
            QtWidgets.QMessageBox.warning(self, "No Row Selected", "Please select an locker to unassign.")


    #gym


    def load_gym(self):
        connection = pyodbc.connect(connection_string)
        cursor = connection.cursor()
        
        # Fetch all columns from the gym table
        cursor.execute("SELECT * from Gym where Fees=1 and Registered = 0")
        gym = cursor.fetchall()
        
        # Assuming that the AvailableEvents table includes more than just EventID and NameOfEvent,
        # you need to set the correct number of columns in the QTableWidget:
        if gym:
            num_columns = len(gym[0])
            self.tableWidget_3.setColumnCount(num_columns)
            # If you want to set header labels based on the column names from the database, you can do this:
            columns = [column[0] for column in cursor.description]
            self.tableWidget_3.setHorizontalHeaderLabels(columns)
        

        self.tableWidget_3.setRowCount(0)
        
        # Populate the table with the event data
        for row_number, row_data in enumerate(gym):
            self.tableWidget_3.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.tableWidget_3.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(data)))

        cursor.close()
        connection.close()

    def view_gym_details(self):
        # Get selected event's ID
        selected_row = self.tableWidget_3.currentRow()

        if selected_row!=-1:
            gym_id = self.tableWidget_3.item(selected_row, 0).text()
            
            # Fetch event details from the database
            connection = pyodbc.connect(connection_string)
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM Gym WHERE GymID = ?", gym_id)
            lock = cursor.fetchone()
            cursor.close()
            connection.close()
            self.event_details_window = viewgym(lock)
            self.event_details_window.show()
        else:
            QtWidgets.QMessageBox.warning(self, "No Row Selected", "Please select a locker to view.")
    
    def view_approved_gym(self):
        
        # Fetch event details from the database
        
        # Show event details in a new window
        self.event_details_window = viewApprovedGym()
        self.event_details_window.show()

    def approve_gym(self):

        selected_row = self.tableWidget_3.currentRow()

        if selected_row != -1:
            # Get the event ID from the selected row
            gymid = self.tableWidget_3.item(selected_row, 0).text()

            # Update the database to remove the corresponding event
            connection = pyodbc.connect(connection_string)
            cursor = connection.cursor()

            try:
                cursor.execute("UPDATE Gym SET Registered = 1 WHERE GymID = ? AND Fees = 1", gymid)
                connection.commit()
                fees = self.tableWidget_3.item(selected_row, 7).text()
                if fees=="True":
                    new_status_item = QtWidgets.QTableWidgetItem("True")


            # Set the new item in the tableWidget_2
                    self.tableWidget_3.setItem(selected_row, 8, new_status_item)
                    QtWidgets.QMessageBox.information(self, "Gym Member Approved", "The status has been updated successfully.")
                    self.tableWidget_3.removeRow(selected_row)
                else:
                    QtWidgets.QMessageBox.warning(self, "Unpaid fees", "Registered value cannot be changed until fees is paid")
            finally:
                cursor.close()
                connection.close()
        else:
            QtWidgets.QMessageBox.warning(self, "No Row Selected", "Please select a row to update the status.")

    def removegymmember(self):
        # Get the selected row
        selected_row = self.tableWidget_3.currentRow()

        if selected_row != -1:
            # Get the event ID from the selected row
            gym_id = self.tableWidget_3.item(selected_row, 0).text()

            # Remove the selected row from the QTableWidget
            self.tableWidget_4.removeRow(selected_row)

            # Update the database to remove the corresponding event
            connection = pyodbc.connect(connection_string)
            cursor = connection.cursor()
            delete_statement = "DELETE FROM Gym WHERE GymID = ?"

            try:
                cursor.execute(delete_statement,  gym_id)
                connection.commit()
                QtWidgets.QMessageBox.information(self, "Membership removed", "The student membership has been cancelled from the gym successfully.")
                self.tableWidget_3.removeRow(selected_row)

            except pyodbc.Error as e:
                QtWidgets.QMessageBox.warning(self, "Database Error", f"An error occurred: {e}")
            finally:
                cursor.close()
                connection.close()
        else:
            QtWidgets.QMessageBox.warning(self, "No Row Selected", "Please select an row to unassign.")




class StudentPortal(QtWidgets.QMainWindow):

    
    def __init__(self, student_id = None):
        super(StudentPortal, self).__init__()
        self.student_id = student_id
        uic.loadUi('portal screen.ui', self)  # Load your .ui file here
        self.feeButton.setEnabled(False)  # Initially disabled pay fees button
        self.load_events()
        self.pushButton_2.clicked.connect(self.view_event_details)
        self.pushButton_3.clicked.connect(self.apply_for_event)
        self.pushButton_5.clicked.connect(self.open_admission_form)
        self.feeButton.clicked.connect(self.open_payment_form)
        self.pushButton_4.clicked.connect(self.open_locker_application_form)  # Connect the locker application button
        self.admission_form = AdmissionForm(self.student_id)
        self.admission_form.admission_successful_signal.connect(self.handle_admission_success)
        

        # Check if gym admission form is already filled and set fee button status accordingly
        self.check_gym_admission_status()
        



    def showEvent(self, event):
        super().showEvent(event)
        # Check gym admission status every time the window is shown
        self.check_gym_admission_status()


    def load_events(self):
        connection = pyodbc.connect(connection_string)
        cursor = connection.cursor()
        
        # Fetch all columns from the AvailableEvents table
        cursor.execute("SELECT EventID, NameOfEvent, StartDate, EndDate, Supervisor, Organizer FROM AvailableEvents")
        events = cursor.fetchall()
        
        # Assuming that the AvailableEvents table includes more than just EventID and NameOfEvent,
        # you need to set the correct number of columns in the QTableWidget:
        if events:
            num_columns = len(events[0])
            self.tableWidget.setColumnCount(num_columns)
            # If you want to set header labels based on the column names from the database, you can do this:
            columns = [column[0] for column in cursor.description]
            self.tableWidget.setHorizontalHeaderLabels(columns)
        
        # Clear the table before inserting new rows
        self.tableWidget.setRowCount(0)
        
        # Populate the table with the event data
        for row_number, row_data in enumerate(events):
            self.tableWidget.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.tableWidget.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(data)))

        cursor.close()
        connection.close()
        
        # Adjust column widths and headers as needed

    def view_event_details(self):
        # Get selected event's ID
        selected_row = self.tableWidget.currentRow()
        if selected_row != -1 :
            event_id = self.tableWidget.item(selected_row, 0).text()

        
            # Fetch event details from the database
            connection = pyodbc.connect(connection_string)
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM AvailableEvents WHERE EventID = ?", event_id)
            event = cursor.fetchone()
            cursor.close()
            connection.close()
            
            # Show event details in a new window
            self.event_details_window = EventDetails(event)
            self.event_details_window.show()
        
        else:
            QtWidgets.QMessageBox.warning(self, "No Row Selected", "Please select an event before viewing details.")

    def apply_for_event(self):
        selected_row = self.tableWidget.currentRow()
        if selected_row == -1:
            QtWidgets.QMessageBox.warning(self, "No Event Selected", "Please select an event before applying.")
            return

        event_id = self.tableWidget.item(selected_row, 0).text()
        self.application_form = ApplicationForm(event_id, self.student_id)  # Pass the event_id and student_id
        self.application_form.show()


    def open_admission_form(self):
        # Collect admission form details and add them to the database
        # After adding to the database, enable the "Pay Fees" button
        # ...
        self.admission_form = AdmissionForm(self.student_id)
        self.admission_form.admission_successful_signal.connect(self.handle_admission_success)
        self.admission_form.show()

    def set_student_id(self, student_id):
        self.student_id = student_id
        self.show()

    def handle_admission_success(self, success):
        if success:
            self.feeButton.setEnabled(True)  # Enable the 'Pay Fees' button
            self.pushButton_5.setEnabled(False)  # Optionally disable the admission form button
        else:
            # Handle the failure case if needed
            pass
    
    def check_gym_admission_status(self):
        connection = pyodbc.connect(connection_string)
        cursor = connection.cursor()
        try:
            cursor.execute("SELECT * FROM Gym WHERE GymID = ?", (self.student_id,))
            if cursor.fetchone():
                self.feeButton.setEnabled(True)
            else:
                self.feeButton.setEnabled(False)
        except pyodbc.Error as e:
            QtWidgets.QMessageBox.warning(self, "Database Error", str(e))
        finally:
            cursor.close()
            connection.close()

    def handle_payment_success(self):
        self.feeButton.setEnabled(False)  # Disable the 'Pay Fees' button

        # Update the database to set the fee bit to 1
        try:
            connection = pyodbc.connect(connection_string)
            cursor = connection.cursor()
            cursor.execute("UPDATE Gym SET Fees = 1 WHERE GymID = ?", self.student_id)
            connection.commit()
        except Exception as e:
            QtWidgets.QMessageBox.warning(self, "Database Error", str(e))
        finally: 
            cursor.close()
            connection.close()
    
    def open_payment_form(self):
        self.payment_form = PaymentForm()
        self.payment_form.payment_successful_signal.connect(self.handle_payment_success)
        self.payment_form.show()

    def open_locker_application_form(self):
        self.locker_application_form = LockerApplicationForm(self.student_id)
        self.locker_application_form.locker_application_successful_signal.connect(self.handle_locker_application_success)
        self.locker_application_form.show()

    def handle_locker_application_success(self, success):
        if success:
            self.pushButton_4.setEnabled(False)  # Assuming 'lockerButton' is the button to apply for a locker
        else:
            # Handle the failure case if needed
            pass

    

# Event Details Window
class EventDetails(QtWidgets.QMainWindow):
    def __init__(self, event):
        super(EventDetails, self).__init__()
        uic.loadUi('view event.ui', self)  # Load the .ui file for event details
        
        # Assuming 'textEdit' is the QTextEdit object name in your .ui file for event details
        # and 'event' is a tuple containing details about the event.
        
        self.textEdit.setReadOnly(True)  # Make the QTextEdit read-only
        event_details = event[6]
        self.textEdit.setText(event_details)  # Set the text to the QTextEdit

        # Connect the close button signal to the close method
        self.pushButton.clicked.connect(self.close)

    # You would have additional methods or modifications depending on your application's requirements.

class ApplicationForm(QtWidgets.QMainWindow):
    def __init__(self, event_id, student_id):
        super(ApplicationForm, self).__init__()
        uic.loadUi('Apply Event.ui', self)
        self.event_id = event_id  # Store the event_id passed as an argument
        self.student_id = student_id  # Add student_id attribute
        self.init_ui()

    def init_ui(self):
        # Set the event name in the QLineEdit based on the event_id
        # Here you need to query the database to get the event name using event_id
        # and set it to self.lineEdit_6. 
        # For example:
        connection = pyodbc.connect(connection_string)
        cursor = connection.cursor()
        cursor.execute("SELECT NameOfEvent FROM AvailableEvents WHERE EventID = ?", (self.event_id))
        event_name = cursor.fetchone()[0]
        self.lineEdit_6.setText(event_name)
        self.lineEdit_6.setReadOnly(True)  # Make the QLineEdit read-only
        self.lineEdit.setText(str(self.student_id))
        self.lineEdit.setReadOnly(True)
        self.pushButton.clicked.connect(self.submit_application)    
        
    def submit_application(self):
        # Check if the student has already applied for this event
        connection = pyodbc.connect(connection_string)
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM Teams WHERE EventID = ? AND StudentID = ?", (self.event_id, self.student_id))
        if cursor.fetchone():
            QtWidgets.QMessageBox.warning(self, "Already Applied", "You have already applied for this event.")
            cursor.close()
            connection.close()
            return

        # Retrieve the form data
        team_name = self.lineEdit_2.text()
        no_of_players = self.lineEdit_3.text()
        team_captain = self.lineEdit_4.text()
        contact_no = self.lineEdit_5.text()

        # Convert no_of_players to an integer
        try:
            no_of_players = int(no_of_players)
        except ValueError:
            QtWidgets.QMessageBox.warning(self, "Invalid Input", "Number of Players must be a valid number.")
            return

        # Insert the application into the database
        try:
            insert_statement = """
                INSERT INTO Teams (EventID, NameOfTeam, NoOfPlayers, TeamCaptain, Contact, Status, StudentID)
                VALUES (?, ?, ?, ?, ?, 0, ?)
            """
            cursor.execute(insert_statement, (self.event_id, team_name, no_of_players, team_captain, contact_no, self.student_id))
            connection.commit()
            QtWidgets.QMessageBox.information(self, "Application Submitted", "Your application has been submitted successfully.")
            self.close()
        except pyodbc.Error as e:
            QtWidgets.QMessageBox.warning(self, "Database Error", f"An error occurred: {e}")
        finally:
            cursor.close()
            connection.close()
    


class AdmissionForm(QtWidgets.QMainWindow):

    admission_successful_signal = QtCore.pyqtSignal(bool)

    def __init__(self, student_id):
        super(AdmissionForm, self).__init__()
        uic.loadUi('AdmissionFormScreen.ui', self)
        self.student_id = student_id
        self.comboBox.addItems([str(year) for year in range(2018, 2028)])
        self.submitButton.clicked.connect(self.submit_admission_form)
        self.comboBox_2.addItems(["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-", "N/A"])

    def submit_admission_form(self):
        # Check if any Line Edit is empty
        if not all([self.lineEdit.text(), self.lineEdit_5.text(), self.lineEdit_6.text()]):
            QtWidgets.QMessageBox.critical(self, "Error", "All fields must be filled.")
            return

        # Collect admission form details
        name = self.lineEdit.text()
        batch = self.comboBox.currentText()
        phone_number = self.lineEdit_5.text()
        emergency_phone = self.lineEdit_6.text()
        payment_option = "Per Semester" if self.radioButton.isChecked() else "Monthly"
        blood_group = self.comboBox_2.currentText()

        try:
            connection = pyodbc.connect(connection_string)
            cursor = connection.cursor()
            # ... existing INSERT query ...
            insert_statement = """
                INSERT INTO Gym (GymID, Name, Batch, BloodGroup, PhoneNumber, EmergencyPhoneNumber, Type, Fees, Registered)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """
            cursor.execute(insert_statement, (self.student_id, name, batch, blood_group, phone_number, emergency_phone, payment_option, 0, 0))
            connection.commit()
            QtWidgets.QMessageBox.information(self, "Success", "Admission form submitted successfully.")
            self.admission_successful_signal.emit(True)  # Emit signal on success
        except Exception:
            QtWidgets.QMessageBox.information(self, "Warning", "You have already filled the Form")
            self.admission_successful_signal.emit(False)  # Emit signal on failure
        finally:    
            cursor.close()
            connection.close()
            self.close()

class PaymentForm(QtWidgets.QMainWindow):
    payment_successful_signal = QtCore.pyqtSignal()

    def __init__(self):
        super(PaymentForm, self).__init__()
        uic.loadUi('Gymfeesscreen.ui', self)  # Load your .ui file here

        self.pushButton.clicked.connect(self.process_payment)

    def process_payment(self):
        # Process the dummy transaction here
        # ...

        # Emit the successful payment signal
        self.payment_successful_signal.emit()
        QtWidgets.QMessageBox.information(self, "Payment Successful", "Your payment was processed successfully.")
        self.close()


class LockerApplicationForm(QtWidgets.QMainWindow):
    locker_application_successful_signal = QtCore.pyqtSignal(bool)

    def __init__(self, student_id):
        super(LockerApplicationForm, self).__init__()
        uic.loadUi('locker screen.ui', self)  # Load the .ui file for locker application
        self.student_id = student_id
        self.lineEdit_2.setText(str(self.student_id))  # Assuming 'lineEdit_id' is your QLineEdit for the student ID
        self.lineEdit_2.setReadOnly(True)  # Make the ID field read-only
        self.pushButton.clicked.connect(self.submit_application)  # Assuming 'pushButton_apply' is your QPushButton for submitting the form

    def submit_application(self):
        name = self.lineEdit.text()  # Assuming 'lineEdit_name' is your QLineEdit for the name

        if not name:
            QtWidgets.QMessageBox.critical(self, "Error", "Name field must be filled.")
            return

        try:
            connection = pyodbc.connect(connection_string)
            cursor = connection.cursor()

            # Check if the student has already applied for a locker
            cursor.execute("SELECT * FROM Locker WHERE StudentID = ?", (self.student_id))
            if cursor.fetchone():
                QtWidgets.QMessageBox.information(self, "Already Applied", "You have already applied for a locker.")
                return

            # Insert new locker application
            cursor.execute("INSERT INTO Locker (Name, Registered, StudentID) VALUES (?, ?, ?)", (name, 0, self.student_id))
            connection.commit()
            QtWidgets.QMessageBox.information(self, "Success", "Locker application submitted successfully.")
            self.locker_application_successful_signal.emit(True)
        except Exception as e:
            QtWidgets.QMessageBox.warning(self, "Database Error", str(e))
            self.locker_application_successful_signal.emit(False)
        finally:
            cursor.close()
            connection.close()
            self.close()



# Add form for admin

class AddForm(QtWidgets.QMainWindow):
    application_submitted_signal = QtCore.pyqtSignal()
    def __init__(self,event_id):
        super(AddForm, self).__init__()
        uic.loadUi('addevent.ui', self)  # Load your application form .ui file here
        self.pushButton.clicked.connect(self.submit_application)

    def submit_application(self):
        # Get the data from the form fields


        event_name = self.lineEdit.text()
        # hu_club = self.lineEdit_2.text()
        start_date = self.dateEdit.text()
        end_date= self.dateEdit_2.text()

        organiser= self.lineEdit_7.text()
        supervisor= self.lineEdit_5.text()

        description = self.lineEdit_6.text()


        # # Convert to appropriate data types if necessary
        # # For example, if the ID and no_of_players should be integers:
        # try:
        #     team_id = int(team_id)
        #     no_of_players = int(no_of_players)
        # except ValueError:
        #     QtWidgets.QMessageBox.warning(self, "Invalid Input", "Please enter valid numbers for ID and Number of Players.")
        #     return

        # Connect to the database and insert the new application
        connection = pyodbc.connect(connection_string)
        cursor = connection.cursor()
        insert_statement = """
            INSERT INTO AvailableEvents (NameOfEvent , StartDate, EndDate , Organizer, Supervisor, Description)
            VALUES (?, ?, ?, ?, ?, ?)
        """
        try:
            # start_date = start_date.toPython()
            # end_date = end_date.toPython()
            cursor.execute(insert_statement, (event_name, start_date ,end_date, organiser ,supervisor, description))
            connection.commit()
            QtWidgets.QMessageBox.information(self, "Application Submitted", "Your application has been submitted successfully.")
            self.application_submitted_signal.emit()
            self.close()
        except pyodbc.Error as e:
            QtWidgets.QMessageBox.warning(self, "Database Error", f"An error occurred: {e}")
        finally:
            cursor.close()
            connection.close()



class viewTeams(QtWidgets.QMainWindow):
    def __init__(self, teams):
        super(viewTeams, self).__init__()
        uic.loadUi('view_teams.ui', self)  # Load the .ui file for event details
        
        # Assuming 'textEdit' is the QTextEdit object name in your .ui file for event details
        # and 'event' is a tuple containing details about the event.
        
        self.lineEdit.setReadOnly(True)
        self.lineEdit_2.setReadOnly(True)   # Make the QTextEdit read-only
        self.lineEdit_3.setReadOnly(True) 
        self.lineEdit_4.setReadOnly(True) 
        self.lineEdit_5.setReadOnly(True) 
        self.lineEdit_6.setReadOnly(True) 
        self.lineEdit_7.setReadOnly(True) 


        Team_id= teams[0] 
        event_id= teams[1]
        nameofteam= teams[2]
        no_of_players= teams[3]
        captain= teams[4]
        contact= teams[5] 
        status= teams[6]    


        self.lineEdit.setText(str(Team_id))  # Set the text to the QTextEdit
        self.lineEdit_2.setText(str(event_id))
        self.lineEdit_3.setText(nameofteam) 
        self.lineEdit_4.setText(str(no_of_players))
        self.lineEdit_5.setText(captain) 
        self.lineEdit_6.setText(str(contact))
        self.lineEdit_7.setText(str(status))


        # Connect the close button signal to the close method
        self.pushButton.clicked.connect(self.close)


class viewApprovedTeams(QtWidgets.QMainWindow):
    def __init__(self):
        super(viewApprovedTeams, self).__init__()
        uic.loadUi('viewapprovedteams.ui', self)
        
        connection = pyodbc.connect(connection_string)
        cursor = connection.cursor()
        
        # Fetch all columns from the AvailableEvents table
        cursor.execute("SELECT TeamID , EventID, NameOfTeam, NoOfPlayers, TeamCaptain, Contact,Status FROM Teams WHERE Status =1")
        teams = cursor.fetchall()
        
        # Assuming that the AvailableEvents table includes more than just EventID and NameOfEvent,
        # you need to set the correct number of columns in the QTableWidget:
        if teams:
            num_columns = len(teams[0])
            self.tableWidget.setColumnCount(num_columns)
            # If you want to set header labels based on the column names from the database, you can do this:
            columns = [column[0] for column in cursor.description]
            self.tableWidget.setHorizontalHeaderLabels(columns)

        
        
        # Clear the table before inserting new rows
        self.tableWidget.setRowCount(0)
        
        # Populate the table with the event data
        for row_number, row_data in enumerate(teams):
            self.tableWidget.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.tableWidget.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(data)))

        cursor.close()
        connection.close()  # Load the .ui file for event details
        

        # Connect the close button signal to the close method
        self.pushButton.clicked.connect(self.close)


class viewlocker(QtWidgets.QMainWindow):
    def __init__(self, lock):
        super(viewlocker, self).__init__()
        uic.loadUi('view_locker.ui', self)  # Load the .ui file for event details
        
        # Assuming 'textEdit' is the QTextEdit object name in your .ui file for event details
        # and 'event' is a tuple containing details about the event.
        
        self.lineEdit.setReadOnly(True)
        self.lineEdit_2.setReadOnly(True)   # Make the QTextEdit read-only
        self.lineEdit_3.setReadOnly(True) 
        self.lineEdit_4.setReadOnly(True) 
        # self.lineEdit_5.setReadOnly(True) 


        Locker_id= lock [0] 
        name=lock[1]
        student_id= lock[3]
        registerd= lock[2]
        # fees= lock[4]

        self.lineEdit.setText(str(Locker_id))  # Set the text to the QTextEdit
        self.lineEdit_2.setText(str(name))
        self.lineEdit_3.setText(str(student_id)) 
        self.lineEdit_4.setText(str(registerd))
        # self.lineEdit_5.setText(str(fees)) 


        # Connect the close button signal to the close method
        self.pushButton.clicked.connect(self.close)


class viewApprovedLockers(QtWidgets.QMainWindow):
    def __init__(self):
        super(viewApprovedLockers, self).__init__()
        uic.loadUi('viewapprovedlockers.ui', self)
        
        connection = pyodbc.connect(connection_string)
        cursor = connection.cursor()
        
        # Fetch all columns from the AvailableEvents table
        cursor.execute("SELECT LockerID, Name, Registered, StudentID from Locker where Registered = 1")
        approvedlock = cursor.fetchall()
        
        # Assuming that the AvailableEvents table includes more than just EventID and NameOfEvent,
        # you need to set the correct number of columns in the QTableWidget:
        if approvedlock:
            num_columns = len(approvedlock[0])
            self.tableWidget.setColumnCount(num_columns)
            # If you want to set header labels based on the column names from the database, you can do this:
            columns = [column[0] for column in cursor.description]
            self.tableWidget.setHorizontalHeaderLabels(columns)

        
        
        # Clear the table before inserting new rows
        self.tableWidget.setRowCount(0)
        
        # Populate the table with the event data
        for row_number, row_data in enumerate(approvedlock):
            self.tableWidget.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.tableWidget.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(data)))

        cursor.close()
        connection.close()
        
        self.pushButton.clicked.connect(self.close)  # Load the .ui file for event details
        

        # Connect the close button signal to the clos

class viewgym(QtWidgets.QMainWindow):
    def __init__(self, lock):
        super(viewgym, self).__init__()
        uic.loadUi('view_gym.ui', self)  # Load the .ui file for event details
        
        # Assuming 'textEdit' is the QTextEdit object name in your .ui file for event details
        # and 'event' is a tuple containing details about the event.
        
        self.lineEdit.setReadOnly(True)
        self.lineEdit_2.setReadOnly(True)   # Make the QTextEdit read-only
        self.lineEdit_3.setReadOnly(True) 
        self.lineEdit_4.setReadOnly(True)
        self.lineEdit_5.setReadOnly(True)
        self.lineEdit_6.setReadOnly(True)   # Make the QTextEdit read-only
        self.lineEdit_7.setReadOnly(True) 
        self.lineEdit_8.setReadOnly(True)

        # self.lineEdit_5.setReadOnly(True) 


        gym_id = lock [0] 
        name = lock[1]
        batch = lock[2]
        blood = lock[3]
        phone = lock[4]
        emphone = lock[5]
        type = lock[6]
        fees = lock[7]
        registered = lock[8]

        self.lineEdit.setText(str(gym_id))  # Set the text to the QTextEdit
        self.lineEdit_2.setText(str(name))
        self.lineEdit_3.setText(batch) 
        self.lineEdit_4.setText(str(blood))
        self.lineEdit_5.setText(str(phone))
        self.lineEdit_6.setText(str(emphone))
        self.lineEdit_7.setText(str(type))
        self.lineEdit_8.setText(str(fees))
        self.lineEdit_9.setText(str(registered))


        # Connect the close button signal to the close method
        self.pushButton.clicked.connect(self.close)

class viewApprovedGym(QtWidgets.QMainWindow):
    def __init__(self):
        super(viewApprovedGym, self).__init__()
        uic.loadUi('viewapprovedgym.ui', self)
        
        connection = pyodbc.connect(connection_string)
        cursor = connection.cursor()
        
        # Fetch all columns from the AvailableEvents table
        cursor.execute("SELECT * from Gym where Registered = 1 and Fees = 1")
        approvedlock = cursor.fetchall()
        
        # Assuming that the AvailableEvents table includes more than just EventID and NameOfEvent,
        # you need to set the correct number of columns in the QTableWidget:
        if approvedlock:
            num_columns = len(approvedlock[0])
            self.tableWidget.setColumnCount(num_columns)
            # If you want to set header labels based on the column names from the database, you can do this:
            columns = [column[0] for column in cursor.description]
            self.tableWidget.setHorizontalHeaderLabels(columns)

        
        
        # Clear the table before inserting new rows
        self.tableWidget.setRowCount(0)
        
        # Populate the table with the event data
        for row_number, row_data in enumerate(approvedlock):
            self.tableWidget.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.tableWidget.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(data)))

        cursor.close()
        connection.close()
        
        self.pushButton.clicked.connect(self.close)


def main():
    app = QtWidgets.QApplication(sys.argv)

    login = LoginScreen()

    student_portal = StudentPortal()
    login.open_student_portal_signal.connect(student_portal.set_student_id)

    admin_portal = AdminPortal()
    login.open_admin_portal_signal.connect(admin_portal.show)

    # Show the login screen
    login.show()

    # Start the application's main loop
    sys.exit(app.exec())


if __name__ == "__main__":
    main()