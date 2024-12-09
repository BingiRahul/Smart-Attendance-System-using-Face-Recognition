import cv2

def load_cascades(cascade1_path, cascade2_path):
    face_cascade1 = cv2.CascadeClassifier(cascade1_path)
    face_cascade2 = cv2.CascadeClassifier(cascade2_path)
    return face_cascade1, face_cascade2

def detect_faces(frame, face_cascade1, face_cascade2):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces1 = face_cascade1.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)
    faces2 = face_cascade2.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)
    faces = list(faces1) + list(faces2)
    return faces

def draw_faces(frame, faces):
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
    return frame

if __name__ == "__main__":
    cascade1_path = "Cascades/Cascade1.xml"
    cascade2_path = "Cascades/Cascade2.xml"

    face_cascade1, face_cascade2 = load_cascades(cascade1_path, cascade2_path)

    video_capture = cv2.VideoCapture(0)

    while True:
        ret, frame = video_capture.read()
        if not ret:
            break

        faces = detect_faces(frame, face_cascade1, face_cascade2)
        frame = draw_faces(frame, faces)

        cv2.imshow("Face Detection", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    video_capture.release()
    cv2.destroyAllWindows()
