import os
import csv
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from PIL import Image, ImageTk
from datetime import datetime
from face_recognition import detect_faces, load_cascades, draw_faces
import cv2

# Initialize directories
os.makedirs("Student_Images", exist_ok=True)
os.makedirs("Attendance_Record", exist_ok=True)

# CSV file for attendance
attendance_file = "Attendance_Record/attendance.csv"
if not os.path.exists(attendance_file):
    with open(attendance_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Date", "Time", "Student Roll Number", "Student Name"])

# Load cascades
cascade1_path = "Cascades/Cascade1.xml"
cascade2_path = "Cascades/Cascade2.xml"
face_cascade1, face_cascade2 = load_cascades(cascade1_path, cascade2_path)

# Styles for the UI
STYLE = {
    "button": {
        "font": ("Helvetica", 12),
        "bg": "#4CAF50",
        "fg": "#fff",
        "activebackground": "#45a049",
        "relief": "raised",
        "bd": 2,
        "width": 20
    },
    "label": {
        "font": ("Helvetica", 14),
        "fg": "#333",
        "bg": "#f0f0f0",
        "padx": 10,
        "pady": 5
    },
    "entry": {
        "font": ("Helvetica", 12),
        "bd": 2,
        "relief": "solid",
        "width": 30,
        "padx": 10
    },
    "treeview": {
        "font": ("Helvetica", 12),
        "background": "#f9f9f9",
        "foreground": "#333",
        "height": 10
    },
    "treeview_scrollbar": {
        "width": 16
    }
}

# Capture and display camera feed
def show_camera(window, canvas, video_capture, name_label):
    ret, frame = video_capture.read()
    if ret:
        frame = cv2.flip(frame, 1)
        faces = detect_faces(frame, face_cascade1, face_cascade2)
        frame = draw_faces(frame, faces)

        detected_name = ""
        if faces:
            for (x, y, w, h) in faces:
                cropped_face = frame[y:y+h, x:x+w]
                for student_file in os.listdir("Student_Images"):
                    student_image = cv2.imread(os.path.join("Student_Images", student_file))
                    if student_image is not None:
                        student_gray = cv2.cvtColor(student_image, cv2.COLOR_BGR2GRAY)
                        cropped_gray = cv2.cvtColor(cropped_face, cv2.COLOR_BGR2GRAY)
                        res = cv2.matchTemplate(student_gray, cropped_gray, cv2.TM_CCOEFF_NORMED)
                        _, max_val, _, _ = cv2.minMaxLoc(res)
                        if max_val > 0.8:  # Threshold for match
                            roll_number, name = student_file.split("_")[0], student_file.split("_")[1].split(".")[0]
                            detected_name = f"{name} (Roll Number: {roll_number})"
                            cv2.putText(frame, detected_name, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)
                            break

        name_label.config(text=detected_name if detected_name else "Detecting...")
        img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(img)
        imgtk = ImageTk.PhotoImage(image=img)
        canvas.create_image(0, 0, anchor=tk.NW, image=imgtk)
        canvas.imgtk = imgtk
        window.after(10, show_camera, window, canvas, video_capture, name_label)

def register_student():
    def capture_image():
        ret, frame = video_capture.read()
        if not ret:
            messagebox.showerror("Error", "Failed to capture image from camera.")
            return

        faces = detect_faces(frame, face_cascade1, face_cascade2)
        frame = draw_faces(frame, faces)

        if faces:
            roll_number = roll_entry.get()
            name = name_entry.get()
            if roll_number and name:
                try:
                    # Ensure the "Student_Images" folder exists
                    os.makedirs("Student_Images", exist_ok=True)
                    
                    # Create the file path
                    file_path = f"Student_Images/{roll_number}_{name}.jpg"
                    
                    # Save the captured image
                    cv2.imwrite(file_path, frame)
                    messagebox.showinfo("Success", f"Student {name} (Roll Number: {roll_number}) registered.")
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to save image: {e}")
            else:
                messagebox.showerror("Error", "Please enter both roll number and name.")
        else:
            messagebox.showerror("Error", "No face detected. Please try again.")
    
    register_window = tk.Toplevel(root)
    register_window.title("Register Student")

    # Create the user interface for student registration
    tk.Label(register_window, text="Enter Student Roll Number:").pack(pady=5)
    roll_entry = tk.Entry(register_window)
    roll_entry.pack(pady=5)

    tk.Label(register_window, text="Enter Student Name:").pack(pady=5)
    name_entry = tk.Entry(register_window)
    name_entry.pack(pady=5)

    capture_button = tk.Button(register_window, text="Capture", command=capture_image, **STYLE["button"])
    capture_button.pack(pady=5)

    canvas = tk.Canvas(register_window, width=640, height=480)
    canvas.pack()

    show_camera(register_window, canvas, video_capture, tk.Label(register_window))

# Take attendance page
def take_attendance():
    def mark_attendance():
        ret, frame = video_capture.read()
        if ret:
            faces = detect_faces(frame, face_cascade1, face_cascade2)
            frame = draw_faces(frame, faces)
            if faces:
                timestamp = datetime.now()
                date = timestamp.strftime("%Y-%m-%d")
                time = timestamp.strftime("%H:%M:%S")
                for (x, y, w, h) in faces:
                    cropped_face = frame[y:y+h, x:x+w]
                    for student_file in os.listdir("Student_Images"):
                        student_image = cv2.imread(os.path.join("Student_Images", student_file))
                        if student_image is not None:
                            student_gray = cv2.cvtColor(student_image, cv2.COLOR_BGR2GRAY)
                            cropped_gray = cv2.cvtColor(cropped_face, cv2.COLOR_BGR2GRAY)
                            res = cv2.matchTemplate(student_gray, cropped_gray, cv2.TM_CCOEFF_NORMED)
                            _, max_val, _, _ = cv2.minMaxLoc(res)
                            if max_val > 0.8:  # Threshold for match
                                roll_number, name = student_file.split("_")[0], student_file.split("_")[1].split(".")[0]
                                with open(attendance_file, mode='a', newline='') as file:
                                    writer = csv.writer(file)
                                    writer.writerow([date, time, roll_number, name])
                                messagebox.showinfo("Success", f"Attendance marked for {name} (Roll Number: {roll_number}).")
                                return
                messagebox.showerror("Error", "No match found for detected faces.")
            else:
                messagebox.showerror("Error", "No face detected.")
    
    attendance_window = tk.Toplevel(root)
    attendance_window.title("Take Attendance")

    name_label = tk.Label(attendance_window, text="Detecting...", font=("Helvetica", 16))
    name_label.pack(pady=5)

    capture_button = tk.Button(attendance_window, text="Mark Attendance", command=mark_attendance, **STYLE["button"])
    capture_button.pack(pady=5)

    canvas = tk.Canvas(attendance_window, width=640, height=480)
    canvas.pack()

    show_camera(attendance_window, canvas, video_capture, name_label)

#view registered students
def view_registered_students():
    # Check if the Student_Images directory exists
    if not os.path.exists("Student_Images"):
        messagebox.showerror("Error", "No registered students found!")
        return

    # Get all student images in the directory
    student_files = os.listdir("Student_Images")
    if not student_files:
        messagebox.showinfo("Info", "No students registered.")
        return

    # Create a new window to display registered students
    students_window = tk.Toplevel(root)
    students_window.title("Registered Students")

    # Create a listbox to display student names and roll numbers
    listbox = tk.Listbox(students_window, width=50, height=15)
    listbox.pack(pady=10)

    # Add student names and roll numbers to the listbox
    for student_file in student_files:
        # Extract roll number and name from the file name
        roll_number, name = student_file.split("_")[0], student_file.split("_")[1].split(".")[0]
        listbox.insert(tk.END, f"{name} (Roll Number: {roll_number})")

#view student logs
def view_logs():
    # Check if the attendance log file exists
    if not os.path.exists(attendance_file):
        messagebox.showerror("Error", "Attendance log file not found!")
        return

    # Read the attendance logs
    with open(attendance_file, mode='r') as file:
        reader = csv.reader(file)
        logs = list(reader)

    if len(logs) == 1:
        messagebox.showinfo("Info", "No logs found.")
        return

    # Create a new window to display logs
    log_window = tk.Toplevel(root)
    log_window.title("Attendance Logs")

    # Create a treeview to display the logs
    treeview = ttk.Treeview(log_window, columns=("Date", "Time", "Roll Number", "Name"), show="headings")
    treeview.heading("Date", text="Date")
    treeview.heading("Time", text="Time")
    treeview.heading("Roll Number", text="Roll Number")
    treeview.heading("Name", text="Name")

    # Insert the logs into the treeview
    for log in logs[1:]:  # Skip header row
        treeview.insert("", "end", values=log)

    treeview.pack(pady=10)

# Main window
root = tk.Tk()
root.title("Smart Attendance System")

# Load images
image_paths = ["Images/register.png", "Images/Take_Attendance.png", "Images/View_Images.png", "Images/View_Logs.png"]
images = [ImageTk.PhotoImage(Image.open(path).resize((100, 100))) for path in image_paths]

# Initialize video capture globally
video_capture = cv2.VideoCapture(0)

# Layout: First Row - Two images with buttons, Second Row - Two images with buttons
frame = tk.Frame(root)
frame.pack(pady=20)

# First row
img1_label = tk.Label(frame, image=images[0])
img1_label.grid(row=0, column=0, padx=10)
register_button = tk.Button(frame, text="Register New Student", command=register_student, **STYLE["button"])
register_button.grid(row=0, column=1, padx=10)

img2_label = tk.Label(frame, image=images[1])
img2_label.grid(row=0, column=2, padx=10)
take_attendance_button = tk.Button(frame, text="Take Attendance", command=take_attendance, **STYLE["button"])
take_attendance_button.grid(row=0, column=3, padx=10)

# Second row
img3_label = tk.Label(frame, image=images[2])
img3_label.grid(row=1, column=0, padx=10)
view_registered_button = tk.Button(frame, text="View Registered Students", command=view_registered_students, **STYLE["button"])
view_registered_button.grid(row=1, column=1, padx=10)

img4_label = tk.Label(frame, image=images[3])
img4_label.grid(row=1, column=2, padx=10)
view_logs_button = tk.Button(frame, text="View Logs", command=view_logs, **STYLE["button"])
view_logs_button.grid(row=1, column=3, padx=10)

root.mainloop()

video_capture.release()
cv2.destroyAllWindows()
