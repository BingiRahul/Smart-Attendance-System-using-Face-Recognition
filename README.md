# Smart Attendance System using Face Detection

### **Overview**
The **Smart Attendance System** is a Python-based application that automates the process of attendance marking using face detection and recognition. It utilizes OpenCV, Face Recognition, and Tkinter to provide a user-friendly interface for managing student registrations, marking attendance, and viewing logs.

---

## **Features**
- **Register Students**: Add student details (roll number and name) with a captured face image for future recognition.
- **Mark Attendance**: Automatically recognize students' faces and record their attendance with the current date and time.
- **View Registered Students**: Display the list of all registered students along with their details.
- **View Attendance Logs**: View attendance records in a table format, showing the date, time, and student details.
- **User-Friendly Interface**: A simple and intuitive GUI built using Tkinter.

---

## **Technologies Used**
- **Python**: Core programming language.
- **OpenCV**: For real-time video capture and face detection.
- **Face Recognition**: For identifying students' faces from stored images.
- **Tkinter**: For creating the graphical user interface.
- **Pillow (PIL)**: For handling and displaying images.

---

## **Requirements**

### **Hardware**
- A computer with a webcam.

### **Software and Libraries**
Ensure you have Python 3.x installed and the following Python libraries:

```bash
pip install opencv-python pillow face_recognition numpy
```

Additionally:

- **Tkinter**: Comes pre-installed with Python. For Linux users, you may need to install it separately:

  ```bash
  sudo apt install python3-tk
  ```

- Haar Cascade XML files for face detection. Download from [OpenCV Haar Cascades](https://github.com/opencv/opencv/tree/master/data/haarcascades) and place them in the `Cascades/` folder.

---

## **Installation**
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/yourusername/Smart-Attendance-System.git
   ```
2. **Navigate to the Project Directory**:
   ```bash
   cd Smart-Attendance-System
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
   *(Create a `requirements.txt` file with the required libraries if not already present.)*

4. **Set Up Directories**:
   Ensure the following folders are present:
   - `Student_Images/`: Stores images of registered students.
   - `Attendance_Record/`: Stores the attendance records in a CSV file.
   - `Cascades/`: Contains the Haar Cascade files.

---

## **Usage**
1. **Run the Application**:
   ```bash
   python app.py
   ```

2. **Features**:
   - **Register New Students**:
     - Enter the roll number and name of the student.
     - Capture the student’s face using the webcam.
   - **Take Attendance**:
     - Detect students' faces in real-time and mark their attendance automatically.
   - **View Registered Students**:
     - View the list of all registered students.
   - **View Logs**:
     - View attendance logs, including the date, time, roll number, and student name.

---

## **Project Structure**
```
Smart-Attendance-System/
│
├── app.py                   # Main application file
├── README.md                # Project documentation
├── requirements.txt         # List of required Python libraries
├── Student_Images/          # Folder for storing student face images
├── Attendance_Record/       # Folder for storing attendance logs
├── Cascades/                # Folder for Haar Cascade XML files
│   ├── Cascade1.xml
│   └── Cascade2.xml
└── images/                  # Folder for GUI icons (e.g., button images)
    ├── register.png
    ├── attendance.png
    ├── students.png
    └── logs.png
```

---

## **Future Enhancements**
- Add real-time attendance statistics (e.g., bar charts or pie charts).
- Integrate with cloud storage for storing attendance records.
- Add email notifications for attendance updates.
- Use a database (e.g., SQLite, MySQL) for better scalability.

---

## **License**
This project is open-source and available under the MIT License.

---

## **Contributors**
- **Rahul** - [GitHub Profile](https://github.com/BingiRahul)

---
