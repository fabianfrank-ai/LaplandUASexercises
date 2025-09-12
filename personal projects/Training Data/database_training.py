import sqlite3
from datetime import datetime
import tkinter as tk




#dummy data 
date="15.10.2023"
exercise="Bench Press"
weight="80"
reps="8"
sets="3"


#create/connect to a database
conn = sqlite3.connect('training_data.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS training
                (date TEXT, exercise TEXT, weight INTEGER, reps INTEGER, sets INTEGER)''')
conn.commit()

c.execute('''CREATE TABLE IF NOT EXISTS volume
                (date TEXT, volume INTEGER)''')


#have a function to insert data into the database
def insert_data(date, exercise, weight, reps, sets):
  ###ask the user what data they want to insert
  ###add data into the database based on the user input

    user_input=input("What data do you want to insert? Type 'training' or 'volume'")
    if user_input == 'training':
        date=input("Please enter date")
        exercise=input("Please enter exercise")
        weight=input("Please enter weight")
        reps=input("Please enter reps")
        sets=input("Please enter sets")
        c.execute("INSERT INTO training (date, exercise, weight, reps, sets) VALUES (?, ?, ?, ?, ?)",
                 (date, exercise, weight, reps, sets))
        conn.commit()


    elif user_input == 'volume':
        date=input("Please enter date")
        volume=input("Please enter the volume")
        c.execute("INSERT INTO volume (date, volume) VALUES (?, ?)", (date, volume))
        conn.commit()



def error_handling():
###check if the data is in the correct format, thinking about a solution for the exercise input without hardcoding all possible exercises
        datetime.strptime(date, '%d.%m.%Y')
        int(weight)
        int(reps)
        int(sets)
      


#call the function to insert the data
try:
        error_handling()
        insert_data(date, exercise, weight, reps, sets)
        print("Data inserted successfully")

except ValueError:
        print("Something went wrong, try again. Remember the date format is dd.mm.yyyy and weight, reps and sets need to be whole numbers.")


