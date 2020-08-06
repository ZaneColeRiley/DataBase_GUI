from tkinter import *
import mysql.connector

LARGE_FONT = ("Verdana", 12)


# Application Class
class Project(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        self.container = Frame(self)

        self.container.pack(side='top', fill='both', expand=True)

        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (StartPage, AdminLogin, IdentityHomePage, DataAdd, UpdateData, Contact, TwitchHomePage, GameData,
                  StreamData, StreamInfo):
            frame = F(self.container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

            self.show_frame(StartPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


class StartPage(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        controller.geometry("800x650")

        self.label = Label(self, text="DataBase GUI System")
        self.label.pack(pady=10, padx=10)

        self.Admin_button = Button(self, text="Identity Database", width=30, height=3,
                                   command=lambda: controller.show_frame(IdentityHomePage))
        self.Admin_button.place(x=290, y=210)
        self.Twitch_Button = Button(self, text="Twitch Database", width=30, height=3,
                                    command=lambda: controller.show_frame(TwitchHomePage))
        self.Twitch_Button.place(x=290, y=290)


class AdminLogin(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        # Buttons
        self.login_button = Button(self, text="Login", width=40,
                                   command=lambda: controller.show_frame(IdentityHomePage))
        self.Home_button = Button(self, text="Home", width=40, command=lambda: controller.show_frame(StartPage))

        # Grid Placements
        self.login_button.place(x=245, y=200)
        self.Home_button.place(x=245, y=240)


class DataAdd(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)

        # Entry Boxes
        self.first_name = Entry(self, width=45)
        self.last_name = Entry(self, width=45)
        self.age = Entry(self, width=45)
        self.gender = Entry(self, width=45)
        self.address = Entry(self, width=45)
        self.city = Entry(self, width=45)
        self.state = Entry(self, width=45)
        self.zipcode = Entry(self, width=45)
        self.employment = Entry(self, width=45)
        self.delete_record = Entry(self, width=45)
        self.ID = Entry(self, width=45)

        # Labels
        self.first_name_label = Label(self, text="First Name")
        self.last_name_label = Label(self, text="Last Name")
        self.age_label = Label(self, text="Age")
        self.gender_label = Label(self, text="Gender")
        self.address_label = Label(self, text="Address")
        self.city_label = Label(self, text="City")
        self.state_label = Label(self, text="State")
        self.zipcode_label = Label(self, text="Zipcode")
        self.employment_label = Label(self, text="Employment")
        self.ID_Label = Label(self, text='ID')

        # Buttons
        self.submit_button = Button(self, text="Add record to database", command=self.submit)
        self.back_button = Button(self, text="Back", command=lambda: controller.show_frame(IdentityHomePage))

        # Grid placements's
        self.first_name.grid(row=0, column=2, padx=20, pady=(10, 0))
        self.first_name_label.grid(row=0, column=1, pady=(10, 0))

        self.last_name.grid(row=1, column=2)
        self.last_name_label.grid(row=1, column=1)

        self.age.grid(row=2, column=2)
        self.age_label.grid(row=2, column=1)

        self.gender.grid(row=3, column=2)
        self.gender_label.grid(row=3, column=1)

        self.address.grid(row=4, column=2)
        self.address_label.grid(row=4, column=1)

        self.city.grid(row=5, column=2)
        self.city_label.grid(row=5, column=1)

        self.state.grid(row=6, column=2)
        self.state_label.grid(row=6, column=1)

        self.zipcode.grid(row=7, column=2)
        self.zipcode_label.grid(row=7, column=1)

        self.employment.grid(row=8, column=2)
        self.employment_label.grid(row=8, column=1)

        self.ID.grid(row=9, column=2)
        self.ID_Label.grid(row=9, column=1)

        self.submit_button.grid(row=10, column=0, pady=10, sticky=W + E, columnspan=3)
        self.back_button.grid(row=12, column=0, sticky=W + E, columnspan=3, pady=10, padx=10)

    def submit(self):
        try:
            mydb = mysql.connector.connect(
                host='192.168.1.21',
                user='ZaneColeRiley',
                password='CadenRiley214569',
                database='Identity'
            )
            cursor = mydb.cursor()

            insert_table_info = f"""INSERT INTO Identity.individuals (firstname, lastname, age, gender, address, city, 
                                    state, zipcode, employment, ID) VALUES 
                               ('{self.first_name.get()}', '{self.last_name.get()}', '{self.age.get()}', 
                                '{self.gender.get()}','{self.address.get()}', '{self.city.get()}', '{self.state.get()}', 
                                '{self.zipcode.get()}', '{self.employment.get()}', '{self.ID.get()}')"""

            cursor.execute(insert_table_info)

            mydb.commit()
            print(cursor.rowcount, "Record Successfully Added in to table")
            cursor.close()

        except mysql.connector.Error as error:
            print("Failed to input Data {}".format(error))

        finally:
            if mydb.is_connected():
                mydb.close()
                print("Database Connection is closed")

            self.first_name.delete(0, END)
            self.last_name.delete(0, END)
            self.age.delete(0, END)
            self.gender.delete(0, END)
            self.address.delete(0, END)
            self.city.delete(0, END)
            self.state.delete(0, END)
            self.zipcode.delete(0, END)
            self.employment.delete(0, END)
            self.ID.delete(0, END)

    def delete(self):
        mydb = mysql.connector.connect(
            host='192.168.1.21',
            user='ZaneColeRiley',
            password='CadenRiley214569',
            database='Identity'
        )
        cursor = mydb.cursor()
        cursor.execute("DELETE from individuals WHERE oid=" + self.delete_record.get())

        mydb.commit()

        mydb.close()

    def update(self):
        mydb = mysql.connector.connect(
            host='192.168.1.21',
            user='ZaneColeRiley',
            password='CadenRiley214569',
            database='Identity'
        )
        cursor = mydb.cursor()

        record_id = self.delete_record.get()

        cursor.execute("SELECT * FROM individuals WHERE oid=" + record_id)

        records = cursor.fetchall()

        for record in records:
            self.first_name.insert(0, record[0])
            self.last_name.insert(0, record[1])
            self.age.insert(0, record[2])
            self.gender.insert(0, record[3])
            self.address.insert(0, record[4])
            self.city.insert(0, record[5])
            self.state.insert(0, record[6])
            self.zipcode.insert(0, record[7])
            self.employment.insert(0, record[8])

        mydb.commit()

        mydb.close()

    def edit(self):
        mydb = mysql.connector.connect(
            host='192.168.1.21',
            user='ZaneColeRiley',
            password='CadenRiley214569',
            database='Identity'
        )
        cursor = mydb.cursor()

        record_id = self.delete_record.get()

        cursor.execute(""" UPDATE individuals SET
                            first_name = :first,
                            last_name = :last,
                            age = :age,
                            gender = :gender,
                            address = :address,
                            city = :city,
                            state = :state,
                            zipcode = :zipcode,
                            employment = :employment,
                            face = :face

                            WHERE oid= :oid""",
                       {
                           'first': self.first_name.get(),
                           'last': self.last_name.get(),
                           'age': self.age.get(),
                           'gender': self.gender.get(),
                           'address': self.address.get(),
                           'city': self.city.get(),
                           'state': self.state.get(),
                           'zipcode': self.zipcode.get(),
                           'employment': self.employment.get(),
                           'oid': record_id
                       })

        mydb.commit()

        mydb.close()


class UpdateData(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)

        # Entry Boxes
        self.first_name = Entry(self, width=45)
        self.last_name = Entry(self, width=45)
        self.age = Entry(self, width=45)
        self.gender = Entry(self, width=45)
        self.address = Entry(self, width=45)
        self.city = Entry(self, width=45)
        self.state = Entry(self, width=45)
        self.zipcode = Entry(self, width=45)
        self.employment = Entry(self, width=45)
        self.Id = Entry(self, width=45)
        self.ti = Entry(self, width=45)

        # Labels
        self.first_name_label = Label(self, text="First Name")
        self.last_name_label = Label(self, text="Last Name")
        self.age_label = Label(self, text="Age")
        self.gender_label = Label(self, text="Gender")
        self.address_label = Label(self, text="Address")
        self.city_label = Label(self, text="City")
        self.state_label = Label(self, text="State")
        self.zipcode_label = Label(self, text="Zipcode")
        self.employment_label = Label(self, text="Employment")
        self.id = Label(self, text="ID")
        self.iDs = Label(self, text='ID')

        # Buttons
        self.edit_button = Button(self, text="Edit Record", command=self.edit)
        self.back_button = Button(self, text="Back", command=lambda: controller.show_frame(IdentityHomePage))
        self.load_identity = Button(self, text="load Identity", width=10, command=self.id)
        self.clear_button = Button(self, text='Clear', command=self.clear_all)

        # Grid placements's
        self.first_name.grid(row=0, column=2, padx=20, pady=(10, 0))
        self.first_name_label.grid(row=0, column=1, pady=(10, 0))

        self.last_name.grid(row=1, column=2)
        self.last_name_label.grid(row=1, column=1)

        self.age.grid(row=2, column=2)
        self.age_label.grid(row=2, column=1)

        self.gender.grid(row=3, column=2)
        self.gender_label.grid(row=3, column=1)

        self.address.grid(row=4, column=2)
        self.address_label.grid(row=4, column=1)

        self.city.grid(row=5, column=2)
        self.city_label.grid(row=5, column=1)

        self.state.grid(row=6, column=2)
        self.state_label.grid(row=6, column=1)

        self.zipcode.grid(row=7, column=2)
        self.zipcode_label.grid(row=7, column=1)

        self.employment.grid(row=8, column=2)
        self.employment_label.grid(row=8, column=1)

        self.iDs.grid(row=9, column=1)
        self.ti.grid(row=9, column=2)

        self.edit_button.grid(row=11, column=0, sticky=W + E, columnspan=3, pady=10, padx=10)
        self.back_button.grid(row=12, column=0, sticky=W + E, columnspan=3, pady=10, padx=10)
        self.id.grid(row=13, column=1)
        self.Id.grid(row=13, column=2)
        self.load_identity.grid(row=14, column=0, sticky=W + E, columnspan=3, pady=10, padx=10)

        self.clear_button.grid(row=15, column=0, sticky=W + E, columnspan=3, pady=10, padx=10)

    def edit(self):
        mydb = mysql.connector.connect(
            host='192.168.1.21',
            user='ZaneColeRiley',
            password='CadenRiley214569',
            database='Identity'
        )
        cursor = mydb.cursor()

        cursor.execute(""" UPDATE Identity.individuals SET
                            firstname = firstname,
                            lastname = lastname,
                            age = age,
                            gender = gender,
                            address = address,
                            city = city,
                            state = state,
                            zipcode = zipcode,
                            employment = employment

                            WHERE ID= ID""",
                       {
                           'firstname': self.first_name.get(),
                           'lastname': self.last_name.get(),
                           'age': self.age.get(),
                           'gender': self.gender.get(),
                           'address': self.address.get(),
                           'city': self.city.get(),
                           'state': self.state.get(),
                           'zipcode': self.zipcode.get(),
                           'employment': self.employment.get(),
                           'ID': self.ti.get()})

        mydb.commit()

        mydb.close()

    def id(self):
        mydb = mysql.connector.connect(
            host='192.168.1.21',
            user='ZaneColeRiley',
            password='CadenRiley214569',
            database='Identity'
        )
        cursor = mydb.cursor()

        record_id = self.Id.get()

        ids = f"select * from identity.individuals WHERE ID='{record_id}';"

        cursor.execute(ids)

        records = cursor.fetchall()

        for record in records:
            self.first_name.insert(0, record[0])
            self.last_name.insert(0, record[1])
            self.age.insert(0, record[2])
            self.gender.insert(0, record[3])
            self.address.insert(0, record[4])
            self.city.insert(0, record[5])
            self.state.insert(0, record[6])
            self.zipcode.insert(0, record[7])
            self.employment.insert(0, record[8])
            self.ti.insert(0, record[9])

    def clear_all(self):
        self.first_name.delete(0, END)
        self.last_name.delete(0, END)
        self.age.delete(0, END)
        self.gender.delete(0, END)
        self.address.delete(0, END)
        self.city.delete(0, END)
        self.state.delete(0, END)
        self.zipcode.delete(0, END)
        self.employment.delete(0, END)
        self.ti.delete(0, END)


class IdentityHomePage(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)

        self.filename = StringVar()
        mydb = mysql.connector.connect(
            host='192.168.1.21',
            user='ZaneColeRiley',
            password='CadenRiley214569',
            database='Identity'
        )
        cursor = mydb.cursor()
        cursor.execute("SELECT * FROM individuals")

        # Labels
        self.title = Label(self, text="Identity Database Home Page", font=LARGE_FONT)

        # Buttons
        self.add_data = Button(self, text="Add Data", command=lambda: controller.show_frame(DataAdd))
        self.update_data = Button(self, text="Update Data", command=lambda: controller.show_frame(UpdateData))
        self.back = Button(self, text='Back', command=lambda: controller.show_frame(StartPage))
        self.contact = Button(self, text="Contact", command=lambda: controller.show_frame(Contact))

        self.title.pack()
        self.add_data.pack(pady=10)
        self.update_data.pack(pady=10)
        self.contact.pack(pady=10)
        self.back.pack(pady=10)


class Contact(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)

        # Entry Boxes
        self.email = Entry(self, width=45)
        self.Cell_number = Entry(self, width=45)
        self.Work_number = Entry(self, width=45)
        self.ID_Change = Entry(self, width=45)
        self.ID_Set = Entry(self, width=45)

        # Labels
        self.title = Label(self, text="Contact Page", font=LARGE_FONT)
        self.email_Label = Label(self, text="Email", font=LARGE_FONT)
        self.Cell_number_label = Label(self, text="Cell Number", font=LARGE_FONT)
        self.Work_number_Label = Label(self, text="Work Number", font=LARGE_FONT)
        self.ID_Label = Label(self, text="ID", font=LARGE_FONT)
        self.ID_Set_Label = Label(self, text="ID", font=LARGE_FONT)

        # Buttons
        self.load_ID = Button(self, text="Load Identity", command=self.id)
        self.Add_entry = Button(self, text="Add Entry", command=self.add)
        self.back = Button(self, text="Back", command=lambda: controller.show_frame(IdentityHomePage))
        self.clear = Button(self, text="Clear", command=self.clear)

        # Grid Placement's

        self.title.grid(row=0, column=0, sticky=W + E, columnspan=3)

        self.email.grid(row=1, column=1)
        self.email_Label.grid(row=1, column=0)

        self.Cell_number.grid(row=2, column=1)
        self.Cell_number_label.grid(row=2, column=0)

        self.Work_number.grid(row=3, column=1)
        self.Work_number_Label.grid(row=3, column=0)

        self.ID_Change.grid(row=4, column=1)
        self.ID_Label.grid(row=4, column=0)

        self.ID_Set.grid(row=6, column=1)
        self.ID_Set_Label.grid(row=6, column=0)

        self.load_ID.grid(row=5, column=0, sticky=W + E, columnspan=3, pady=10)
        self.back.grid(row=7, column=0, sticky=W + E, columnspan=3, pady=10)
        self.Add_entry.grid(row=8, column=0, sticky=W + E, columnspan=3, pady=10)

        self.clear.grid(row=9, column=0, sticky=W + E, columnspan=3, pady=10)

    def id(self):
        mydb = mysql.connector.connect(
            host='192.168.1.21',
            user='ZaneColeRiley',
            password='CadenRiley214569',
            database='Identity'
        )
        cursor = mydb.cursor()

        record_id = self.ID_Set.get()

        ids = f"select * from identity.contactinfo WHERE ID='{record_id}';"

        cursor.execute(ids)

        records = cursor.fetchall()

        for record in records:
            self.Cell_number.insert(0, record[0])
            self.email.insert(0, record[1])
            self.Work_number.insert(0, record[2])
            self.ID_Change.insert(0, record[3])

    def add(self):
        try:
            mydb = mysql.connector.connect(
                host='192.168.1.21',
                user='ZaneColeRiley',
                password='CadenRiley214569',
                database='Identity'
            )
            cursor = mydb.cursor()

            insert_table_info = f"""INSERT INTO Identity.contactinfo (CellNumber, Email, WorkNumber, ID) VALUES 
                               ('{self.Cell_number.get()}', '{self.email.get()}', '{self.Work_number.get()}', 
                                '{self.ID_Change.get()}')"""

            cursor.execute(insert_table_info)

            mydb.commit()
            print(cursor.rowcount, "Record Successfully Added in to table")
            cursor.close()

        except mysql.connector.Error as error:
            print("Failed to input Data {}".format(error))

        finally:
            if mydb.is_connected():
                mydb.close()
                print("Database Connection is closed")

            self.Cell_number.delete(0, END)
            self.email.delete(0, END)
            self.Work_number.delete(0, END)
            self.ID_Change.delete(0, END)

    def clear(self):
        self.Cell_number.delete(0, END)
        self.email.delete(0, END)
        self.Work_number.delete(0, END)
        self.ID_Change.delete(0, END)


class TwitchHomePage(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        mydb = mysql.connector.connect(
            host='192.168.1.21',
            user='ZaneColeRiley',
            password='CadenRiley214569',
            database='twitch'
        )
        self.cursor = mydb.cursor()

        self.home_label = Label(self, text="Twitch Database HomePage", font=LARGE_FONT)

        self.Games = Button(self, text="Game", command=lambda: controller.show_frame(GameData))
        self.Stream_data = Button(self, text="Stream Data", command=lambda: controller.show_frame(StreamData))
        self.Stream_info = Button(self, text="Stream Info", command=lambda: controller.show_frame(StreamInfo))
        self.back = Button(self, text="Back", command=lambda: controller.show_frame(StartPage))

        self.home_label.pack()

        self.Games.pack(pady=10)
        self.Stream_data.pack(pady=10)
        self.Stream_info.pack(pady=10)
        self.back.pack(pady=10)


class GameData(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)

        # Labels
        self.game_name_label = Label(self, text="Game Name", font=LARGE_FONT)
        self.rating_label = Label(self, text="Rating", font=LARGE_FONT)
        self.Interest_label = Label(self, text="Interest", font=LARGE_FONT)
        self.play_time_label = Label(self, text="Play Time", font=LARGE_FONT)
        self.Story_label = Label(self, text="Story Game", font=LARGE_FONT)
        self.Game_Name_Label = Label(self, text="Game Name", font=LARGE_FONT)

        # Entry's
        self.game_name = Entry(self, width=45)
        self.rating = Entry(self, width=45)
        self.Interest = Entry(self, width=45)
        self.play_time = Entry(self, width=45)
        self.Story = Entry(self, width=45)
        self.Game_Name = Entry(self, width=45)

        # Buttons
        self.load_game = Button(self, text="Load Game Data", command=self.load_game)
        self.update_game = Button(self, text="Update Game Data", command=None)
        self.add_game = Button(self, text="Add Game Data", command=self.add)
        self.clear_button = Button(self, text="Clear", command=self.clear)
        self.back_button = Button(self, text="Back", command=lambda: controller.show_frame(TwitchHomePage))

        # Grid Placement's
        self.game_name.grid(row=1, column=2)
        self.game_name_label.grid(row=1, column=1)

        self.rating.grid(row=2, column=2)
        self.rating_label.grid(row=2, column=1)

        self.Interest.grid(row=3, column=2)
        self.Interest_label.grid(row=3, column=1)

        self.play_time.grid(row=4, column=2)
        self.play_time_label.grid(row=4, column=1)

        self.Story.grid(row=5, column=2)
        self.Story_label.grid(row=5, column=1)

        self.Game_Name.grid(row=7, column=2)
        self.Game_Name_Label.grid(row=7, column=1)

        self.load_game.grid(row=6, column=0, pady=10, columnspan=3, sticky=W + E)
        self.add_game.grid(row=8, column=0, pady=10, columnspan=3, sticky=W + E)
        self.clear_button.grid(row=9, column=0, pady=10, columnspan=3, sticky=W + E)
        self.back_button.grid(row=10, column=0, pady=10, columnspan=3, sticky=W + E)

    def load_game(self):
        mydb = mysql.connector.connect(
            host='192.168.1.21',
            user='ZaneColeRiley',
            password='CadenRiley214569',
            database='twitch'
        )
        cursor = mydb.cursor()
        gamenameid = self.Game_Name.get()

        cursor.execute(f"SELECT * FROM twitch.games WHERE GameName='{gamenameid}';")

        records = cursor.fetchall()

        for record in records:
            self.game_name.insert(0, record[0])
            self.rating.insert(0, record[1])
            self.Interest.insert(0, record[2])
            self.play_time.insert(0, record[3])
            self.Story.insert(0, record[4])

    def add(self):
        try:
            mydb = mysql.connector.connect(
                host='192.168.1.21',
                user='ZaneColeRiley',
                password='CadenRiley214569',
                database='twitch'
            )
            cursor = mydb.cursor()

            insert_table_info = f"""INSERT INTO twitch.games (GameName, Rating, Interest, Play_time, Story_Game) VALUES 
                               ('{self.game_name.get()}', '{self.rating.get()}', '{self.Interest.get()}', 
                                '{self.play_time.get()}', '{self.Story.get()}')"""

            cursor.execute(insert_table_info)

            mydb.commit()
            print(cursor.rowcount, "Record Successfully Added in to table")
            cursor.close()

        except mysql.connector.Error as error:
            print("Failed to input Data {}".format(error))

        finally:
            if mydb.is_connected():
                mydb.close()
                print("Database Connection is closed")

            self.game_name.delete(0, END)
            self.rating.delete(0, END)
            self.Interest.delete(0, END)
            self.play_time.delete(0, END)
            self.Story.delete(0, END)

    def clear(self):
        self.game_name.delete(0, END)
        self.rating.delete(0, END)
        self.Interest.delete(0, END)
        self.play_time.delete(0, END)
        self.Story.delete(0, END)


class StreamInfo(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)

        # Labels
        self.title = Label(self, text="Twitch Stream Info", font=LARGE_FONT)
        self.days_label = Label(self, text='Days Streamed', font=LARGE_FONT)
        self.time_label = Label(self, text='Time Streamed', font=LARGE_FONT)
        self.time_of_day_label = Label(self, text="Time of day", font=LARGE_FONT)
        self.not_days_label = Label(self, text="Days not Streamed", font=LARGE_FONT)
        self.start_day_label = Label(self, text='Day Started', font=LARGE_FONT)
        self.Start_date_label = Label(self, text="Start Date", font=LARGE_FONT)

        # Entry's
        self.days = Entry(self, width=45)
        self.time = Entry(self, width=45)
        self.time_of_day = Entry(self, width=45)
        self.not_days = Entry(self, width=45)
        self.start_day = Entry(self, width=45)
        self.Start_date = Entry(self, width=45)

        # Buttons
        self.add_entry = Button(self, text="Add Entry", command=self.add_entry)
        self.back = Button(self, text="Back", command=lambda: controller.show_frame(TwitchHomePage))
        self.load_entry = Button(self, text='Load Entry', command=self.load_entry)

        # Grid Placements
        self.title.grid(row=0, column=0, columnspan=3, sticky=W + E, pady=10)

        self.days_label.grid(row=1, column=0)
        self.days.grid(row=1, column=1)

        self.time_label.grid(row=2, column=0)
        self.time.grid(row=2, column=1)

        self.time_of_day_label.grid(row=3, column=0)
        self.time_of_day.grid(row=3, column=1)

        self.not_days_label.grid(row=4, column=0)
        self.not_days.grid(row=4, column=1)

        self.start_day_label.grid(row=5, column=0)
        self.start_day.grid(row=5, column=1)

        self.add_entry.grid(row=6, column=0, columnspan=3, sticky=W + E, pady=10)

        self.Start_date_label.grid(row=7, column=0)
        self.Start_date.grid(row=7, column=1)

        self.load_entry.grid(row=8, column=0, columnspan=3, sticky=W + E, pady=10)

        self.back.grid(row=9, column=0, columnspan=3, sticky=W + E, pady=10)

    def load_entry(self):
        mydb = mysql.connector.connect(
            host='192.168.1.21',
            user='ZaneColeRiley',
            password='CadenRiley214569',
            database='twitch'
        )
        cursor = mydb.cursor()

        cursor.execute(f"SELECT * FROM twitch.streaminfo WHERE StartDate='{self.Start_date.get()}';")

        records = cursor.fetchall()

        for record in records:
            self.days.insert(0, record[0])
            self.time.insert(0, record[1])
            self.time_of_day.insert(0, record[2])
            self.not_days.insert(0, record[3])
            self.start_day.insert(0, record[4])

    def add_entry(self):
        try:
            mydb = mysql.connector.connect(
                host='192.168.1.21',
                user='ZaneColeRiley',
                password='CadenRiley214569',
                database='twitch'
            )
            cursor = mydb.cursor()

            insert_table_info = f"""INSERT INTO twitch.streaminfo (DaysStreamed, TimeStreamed, 
                                    TimeofDay, DaysnotStreamed, StartDate) VALUES 
                               ('{self.days.get()}', '{self.time.get()}', '{self.time_of_day.get()}', 
                                '{self.not_days.get()}', '{self.start_day.get()}')"""

            cursor.execute(insert_table_info)

            mydb.commit()
            print(cursor.rowcount, "Record Successfully Added in to table")
            cursor.close()

        except mysql.connector.Error as error:
            print("Failed to input Data {}".format(error))

        finally:
            if mydb.is_connected():
                mydb.close()
                print("Database Connection is closed")


class StreamData(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)

        # Labels
        self.title = Label(self, text="Stream Data Page", font=LARGE_FONT)
        self.AVG_label = Label(self, text="Avg Viewer", font=LARGE_FONT)
        self.Unique_label = Label(self, text="Unique Viewer", font=LARGE_FONT)
        self.Follower_label = Label(self, text="New Followers", font=LARGE_FONT)
        self.Subs_label = Label(self, text="New Subs", font=LARGE_FONT)
        self.Total_label = Label(self, text="Total Viewers", font=LARGE_FONT)
        self.date_label = Label(self, text="Date", font=LARGE_FONT)
        self.Date_label = Label(self, text="Date", font=LARGE_FONT)

        # Entry's
        self.AVG = Entry(self, width=45)
        self.Unique = Entry(self, width=45)
        self.Follower = Entry(self, width=45)
        self.Subs = Entry(self, width=45)
        self.Total = Entry(self, width=45)
        self.Date = Entry(self, width=45)
        self.date = Entry(self, width=45)

        # Buttons
        self.load_entry = Button(self, text="Load Entry", command=self.load_entry)
        self.add_entry = Button(self, text="Add Entry", command=self.add_entry)
        self.back = Button(self, text="Back", command=lambda: controller.show_frame(TwitchHomePage))

        # Grid Placements
        self.title.grid(row=0, column=0, columnspan=3, sticky=W + E, pady=10)

        self.AVG_label.grid(row=1, column=0)
        self.AVG.grid(row=1, column=1)

        self.Unique_label.grid(row=2, column=0)
        self.Unique.grid(row=2, column=1)

        self.Follower_label.grid(row=3, column=0)
        self.Follower.grid(row=3, column=1)

        self.Subs_label.grid(row=4, column=0)
        self.Subs.grid(row=4, column=1)

        self.date_label.grid(row=6, column=0)
        self.date.grid(row=6, column=1)

        self.Total_label.grid(row=5, column=0)
        self.Total.grid(row=5, column=1)

        self.add_entry.grid(row=7, column=0, columnspan=3, sticky=W + E, pady=10)

        self.Date_label.grid(row=8, column=0)
        self.Date.grid(row=8, column=1)

        self.load_entry.grid(row=9, column=0, columnspan=3, sticky=W + E, pady=10)

        self.back.grid(row=10, column=0, columnspan=3, sticky=W + E, pady=10)

    def load_entry(self):
        mydb = mysql.connector.connect(
            host='192.168.1.21',
            user='ZaneColeRiley',
            password='CadenRiley214569',
            database='twitch'
        )
        cursor = mydb.cursor()

        cursor.execute(f"SELECT * FROM twitch.streamdata WHERE Date='{self.Date.get()}';")

        records = cursor.fetchall()

        for record in records:
            self.AVG.insert(0, record[0])
            self.Unique.insert(0, record[1])
            self.Follower.insert(0, record[2])
            self.Subs.insert(0, record[3])
            self.Total.insert(0, record[4])
            self.date.insert(0, record[5])

    def add_entry(self):
        try:
            mydb = mysql.connector.connect(
                host='192.168.1.21',
                user='ZaneColeRiley',
                password='CadenRiley214569',
                database='twitch'
            )
            cursor = mydb.cursor()

            insert_table_info = f"""INSERT INTO twitch.streamdata (Avg_Viewers, Uniqueviewers, Newfollowers, 
                                         Newsubscriptions, Totalviewercount, Date) VALUES 
                               ('{self.AVG.get()}', '{self.Unique.get()}', '{self.Follower.get()}', '{self.Subs.get()}',
                                '{self.Total.get()}', '{self.date.get()}')"""

            cursor.execute(insert_table_info)

            mydb.commit()
            print(cursor.rowcount, "Record Successfully Added in to table")
            cursor.close()

        except mysql.connector.Error as error:
            print("Failed to input Data {}".format(error))

        finally:
            if mydb.is_connected():
                mydb.close()
                print("Database Connection is closed")

                self.AVG.delete(0, END)
                self.Unique.delete(0, END)
                self.Follower.delete(0, END)
                self.Subs.delete(0, END)
                self.Total.delete(0, END)
                self.date.delete(0, END)


if __name__ == '__main__':
    app = Project()
    app.mainloop()
