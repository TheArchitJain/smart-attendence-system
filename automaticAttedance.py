import csv
import tkinter

import tkinter as tk  # Importing the tkinter module for GUI
from tkinter import *  # Importing all classes and functions from tkinter
import os, cv2  # Importing the os and cv2 modules
import shutil  # Importing the shutil module for file operations
import csv  # Importing the csv module for working with CSV files
import numpy as np  # Importing the numpy module for numerical operations
from PIL import ImageTk, Image  # Importing classes from the PIL module for image processing
import pandas as pd  # Importing the pandas module for data manipulation
import datetime  # Importing the datetime module for working with dates and times
import time  # Importing the time module for time-related operations
import tkinter.ttk as tkk  # Importing additional classes from tkinter for GUI
import tkinter.font as font  # Importing the font module from tkinter for font-related operations

haarcasecade_path = "./haarcascade_frontalface_default.xml"  # Path to the Haar cascade XML file for face detection
trainimagelabel_path = "TrainingImageLabel/Trainner.yml"  # Path to the trained image label file
trainimage_path = "TrainingImage"  # Path to the training images directory
studentdetail_path = "StudentDetails/studentdetails.csv"  # Path to the student details CSV file
attendance_path = "Attendance"  # Path to the attendance directory

# Function for choosing subject and filling attendance
def subjectChoose(text_to_speech):
    def FillAttendance():
        sub = tx.get()  # Get the subject entered by the user
        now = time.time()  # Get the current time
        future = now + 20  # Set the future time as 20 seconds from now
        print(now)
        print(future)
        if sub == "":  # If subject is not entered
            t = "Please enter the subject name!!!"
            text_to_speech(t)  # Text-to-speech output
        else:
            try:
                recognizer = cv2.face.LBPHFaceRecognizer_create()  # Create LBPH face recognizer
                try:
                    recognizer.read(trainimagelabel_path)  # Read the trained image label file
                except:
                    e = "Model not found,please train model"
                    Notifica.configure(
                        text=e,
                        bg="black",
                        fg="yellow",
                        width=33,
                        font=("times", 15, "bold"),
                    )
                    Notifica.place(x=20, y=250)
                    text_to_speech(e)  # Text-to-speech output
                facecasCade = cv2.CascadeClassifier(haarcasecade_path)  # Create Haar cascade classifier for face detection
                df = pd.read_csv(studentdetail_path)  # Read the student details CSV file
                cam = cv2.VideoCapture(0)  # Open the default camera
                font = cv2.FONT_HERSHEY_SIMPLEX  # Set the font for drawing on images
                col_names = ["Enrollment", "Name"]  # Column names for attendance dataframe
                attendance = pd.DataFrame(columns=col_names)  # Create an empty dataframe for attendance
                while True:
                    ___, im = cam.read()  # Read an image from the camera
                    gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)  # Convert the image to grayscale
                    faces = facecasCade.detectMultiScale(gray, 1.2, 5)  # Detect faces in the image
                    for (x, y, w, h) in faces:
                        global Id

                        Id, conf = recognizer.predict(gray[y : y + h, x : x + w])  # Predict the label of the face
                        if conf < 70:  # If confidence is less than 70
                            print(conf)
                            global Subject
                            global aa
                            global date
                            global timeStamp
                            Subject = tx.get()  # Get the subject entered by the user
                            ts = time.time()  # Get the current time
                            date = datetime.datetime.fromtimestamp(ts).strftime(
                                "%Y-%m-%d"
                            )  # Get the current date
                            timeStamp = datetime.datetime.fromtimestamp(ts).strftime(
                                "%H:%M:%S"
                            )  # Get the current time
                            aa = df.loc[df["Enrollment"] == Id]["Name"].values  # Get the name of the student
                            global tt
                            tt = str(Id) + "-" + aa  # Create the attendance entry
                            attendance.loc[len(attendance)] = [
                                Id,
                                aa,
                            ]  # Add the attendance entry to the dataframe
                            cv2.rectangle(im, (x, y), (x + w, y + h), (0, 260, 0), 4)  # Draw a rectangle around the face
                            cv2.putText(
                                im, str(tt), (x + h, y), font, 1, (255, 255, 0,), 4
                            )  # Draw the attendance entry on the image
                        else:
                            Id = "Unknown"
                            tt = str(Id)
                            cv2.rectangle(im, (x, y), (x + w, y + h), (0, 25, 255), 7)  # Draw a rectangle around the face
                            cv2.putText(
                                im, str(tt), (x + h, y), font, 1, (0, 25, 255), 4
                            )  # Draw "Unknown" on the image
                    if time.time() > future:  # If current time exceeds the future time
                        break

                    attendance = attendance.drop_duplicates(
                        ["Enrollment"], keep="first"
                    )  # Remove duplicate entries from the attendance dataframe
                    cv2.imshow("Filling Attendance...", im)  # Show the image with attendance markings
                    key = cv2.waitKey(30) & 0xFF  # Wait for key press
                    if key == 27:  # If ESC key is pressed
                        break

                ts = time.time()  # Get the current time
                print(aa)
                attendance["date"] = date  # Add the date column to the attendance dataframe
                attendance["Attendance"] = "P"  # Set the attendance status as "P" for present
                attendance[date] = 1  # Set the attendance count for the date as 1
                date = datetime.datetime.fromtimestamp(ts).strftime("%Y-%m-%d")  # Get the current date
                timeStamp = datetime.datetime.fromtimestamp(ts).strftime("%H:%M:%S")  # Get the current time
                Hour, Minute, Second = timeStamp.split(":")  # Split the time into hours, minutes, and seconds
                fileName = (
                    "Attendance/" + Subject + ".csv"
                )  # Create the filename for the attendance CSV file
                path = os.path.join(attendance_path, Subject)  # Create the path for the attendance directory
                fileName = (
                    f"{path}/"
                    + Subject
                    + "_"
                    + date
                    + "_"
                    + Hour
                    + "-"
                    + Minute
                    + "-"
                    + Second
                    + ".csv"
                )  # Create the complete filename for the attendance CSV file
                attendance = attendance.drop_duplicates(["Enrollment"], keep="first")  # Remove duplicate entries from the attendance dataframe
                print(attendance)
                attendance.to_csv(fileName, index=False)  # Save the attendance dataframe to a CSV file

                m = "Attendance Filled Successfully of " + Subject
                Notifica.configure(
                    text=m,
                    bg="black",
                    fg="yellow",
                    width=33,
                    relief=RIDGE,
                    bd=5,
                    font=("times", 15, "bold"),
                )
                text_to_speech(m)  # Text-to-speech output

                Notifica.place(x=20, y=250)

                cam.release()  # Release the camera
                cv2.destroyAllWindows()  # Close all windows


                root = tkinter.Tk()  # Create a new tkinter window
                root.title("Attendance of " + Subject)  # Set the window title
                root.configure(background="black")  # Set the window background color
                cs = os.path.join(path, fileName)  # Create the complete path for the attendance CSV file
                print(cs)
                with open(cs, newline="") as file:  # Open the attendance CSV file
                    reader = csv.reader(file)  # Create a CSV reader
                    r = 0

                    for col in reader:  # Iterate over each row in the CSV file
                        c = 0
                        for row in col:  # Iterate over each column in the row
                            label = tkinter.Label(
                                root,
                                width=10,
                                height=1,
                                fg="yellow",
                                font=("times", 15, " bold "),
                                bg="black",
                                text=row,
                                relief=tkinter.RIDGE,
                            )  # Create a label widget for each cell in the CSV file
                            label.grid(row=r, column=c)  # Place the label in the tkinter window
                            c += 1
                        r += 1
                root.mainloop()  # Start the tkinter event loop
                print(attendance)
            except:
                f = "No Face found for attendance"
                text_to_speech(f)  # Text-to-speech output
                cv2.destroyAllWindows()  # Close all windows

    subject = Tk()  # Create a new tkinter window
    subject.title("Subject...")  # Set the window title
    subject.geometry("580x320")  # Set the window size
    subject.resizable(0, 0)  # Disable window resizing
    subject.configure(background="black")  # Set the window background color
    titl = tk.Label(subject, bg="black", relief=RIDGE, bd=10, font=("arial", 30))
    titl.pack(fill=X)
    titl = tk.Label(
        subject,
        text="Enter the Subject Name",
        bg="black",
        fg="green",
        font=("arial", 25),
    )
    titl.place(x=160, y=12)
    Notifica = tk.Label(
        subject,
        text="Attendance filled Successfully",
        bg="yellow",
        fg="black",
        width=33,
        height=2,
        font=("times", 15, "bold"),
    )

    def Attf():
        sub = tx.get()  # Get the subject entered by the user
        if sub == "":  # If subject is not entered
            t = "Please enter the subject name!!!"
            text_to_speech(t)  # Text-to-speech output
        else:
            os.startfile(
                f"Attendance/{sub}"
            )  # Open the attendance directory

    attf = tk.Button(
        subject,
        text="Check Sheets",
        command=Attf,
        bd=7,
        font=("times new roman", 15),
        bg="black",
        fg="yellow",
        height=2,
        width=10,
        relief=RIDGE,
    )
    attf.place(x=360, y=170)

    sub = tk.Label(
        subject,
        text="Enter Subject",
        width=10,
        height=2,
        bg="black",
        fg="yellow",
        bd=5,
        relief=RIDGE,
        font=("times new roman", 15),
    )
    sub.place(x=50, y=100)

    tx = tk.Entry(
        subject,
        width=15,
        bd=5,
        bg="black",
        fg="yellow",
        relief=RIDGE,
        font=("times", 30, "bold"),
    )
    tx.place(x=190, y=100)

    fill_a = tk.Button(
        subject,
        text="Fill Attendance",
        command=FillAttendance,
        bd=7,
        font=("times new roman", 15),
        bg="black",
        fg="yellow",
        height=2,
        width=12,
        relief=RIDGE,
    )
    fill_a.place(x=195, y=170)
    subject.mainloop()  # Start the tkinter event loop
