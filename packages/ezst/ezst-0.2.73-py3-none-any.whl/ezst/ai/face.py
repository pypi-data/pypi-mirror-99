from ezst import cv
import face_recognition 
import numpy as np
import cv2
import os
  

def learn(filename_list) :
  
  known_face_encodings = []
  known_face_names = []
  for index in range(len(filename_list)) :
    
    image = face_recognition.load_image_file(filename_list[index])
    image_encoding = face_recognition.face_encodings(image)[0]

    known_face_encodings.append(image_encoding)

    name = os.path.splitext(filename_list[index])
    name = os.path.split(name[0])
    known_face_names.append(name[1])

  known_face = {
      "encodings": known_face_encodings,
      "names": known_face_names
  }
  return known_face


def recognition(filename, known_face):
  image = cv.read(filename)

  face_locations = face_recognition.face_locations(image)
  face_encodings = face_recognition.face_encodings(image, face_locations)

  face_names = []

  for face_encoding in face_encodings:
    matches = face_recognition.compare_faces(known_face["encodings"], face_encoding)
    name = "Unknown"

    face_distances = face_recognition.face_distance(known_face["encodings"], face_encoding)
    best_match_index = np.argmin(face_distances)
    if matches[best_match_index]:
        name = known_face["names"][best_match_index]

    face_names.append(name)

  for (top, right, bottom, left), name in zip(face_locations, face_names):
    # Draw a box around the face
    cv2.rectangle(image, (left, top), (right, bottom), (0, 0, 255), 2)

    # Draw a label with a name below the face
    cv2.rectangle(image, (left, bottom + 35), (right, bottom), (0, 0, 255), cv2.FILLED)
    font = cv2.FONT_HERSHEY_DUPLEX
    cv2.putText(image, name, (left + 6, bottom + 29), font, 0.8, (255, 255, 255), 1)
  
  cv.show(image, size=(14,14))