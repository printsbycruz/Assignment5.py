# Program Name: Assignment5.py
# Course: IT3883/Section W01
# Student Name: Jonathan Cruz
# Assignment Number: Assignment 5
# Due Date: 07/17/2026
# Purpose: This program reads daily temperature information from a text file,
# stores the information in a SQLite database, and calculates the average
# temperatures recorded on Sunday and Thursday.
# Resources Used: Python sqlite3 documentation and understanding the SQLite database process.

import sqlite3


# Store the name of the input file. The file should be in the same folder
# as this Python program when the program is run.
temperature_file = "Assignment5input.txt"

# Connect to the database. Python creates the file if it does not exist.
database_connection = sqlite3.connect("temperature_readings.db")
database_cursor = database_connection.cursor()

# Remove the old table so running the program again will not duplicate data.
database_cursor.execute("DROP TABLE IF EXISTS Weekly_Temperatures")

# Create a table for the day and temperature values from the input file.
database_cursor.execute("""
    CREATE TABLE Weekly_Temperatures (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        Day_Of_Week TEXT,
        Temperature_Value REAL
    )
""")

# Open the input file and insert every valid line into the database table.
with open(temperature_file, "r") as file:
    for reading in file:
        reading_parts = reading.split()

        if len(reading_parts) == 2:
            day_name = reading_parts[0]
            temperature = float(reading_parts[1])

            database_cursor.execute("""
                INSERT INTO Weekly_Temperatures
                (Day_Of_Week, Temperature_Value)
                VALUES (?, ?)
            """, (day_name, temperature))

# Save all inserted records to the database.
database_connection.commit()

# Use SQL to calculate the average temperature recorded on Sunday.
database_cursor.execute("""
    SELECT AVG(Temperature_Value)
    FROM Weekly_Temperatures
    WHERE Day_Of_Week = 'Sunday'
""")
sunday_average = database_cursor.fetchone()[0]

# Use SQL to calculate the average temperature recorded on Thursday.
database_cursor.execute("""
    SELECT AVG(Temperature_Value)
    FROM Weekly_Temperatures
    WHERE Day_Of_Week = 'Thursday'
""")
thursday_average = database_cursor.fetchone()[0]

# Display both averages rounded to two decimal places.
print(f"Average temperature for Sunday: {sunday_average:.2f}")
print(f"Average temperature for Thursday: {thursday_average:.2f}")

# Close the connection after all database work is complete.
database_connection.close()
