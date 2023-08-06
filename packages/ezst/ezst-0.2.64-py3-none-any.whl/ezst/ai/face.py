def learn(filename, label) :
  import face_recognition as face
  image = face.load_image_file(filename)
  image_encoding = face.face_encodings(image)[0]

  known_face_encodings = [ image_encoding ]
  known_face_names = [ label ]

  known_face = {
      "encodings": known_face_encodings,
      "names": known_face_names
  }
  return known_face

def learn_list(filename_list, label_list) :
  import face_recognition as face

  known_face_encodings = []
  known_face_names = []
  for index in range(len(filename_list)) :
    
    image = face.load_image_file(filename_list[index])
    image_encoding = face.face_encodings(image)[0]

    known_face_encodings.append(image_encoding)
    known_face_names.append(label_list[index])

  known_face = {
      "encodings": known_face_encodings,
      "names": known_face_names
  }
  return known_face


def recognition(filename, known_face):
  import face_recognition 
  import cv2
  import numpy as np
  from google.colab.patches import cv2_imshow
  
  frame = cv2.imread(filename)
  small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
  rgb_small_frame = small_frame[:, :, ::-1]

  face_locations = face_recognition.face_locations(rgb_small_frame)
  face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

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
    # Scale back up face locations since the frame we detected in was scaled to 1/4 size
    top *= 4
    right *= 4
    bottom *= 4
    left *= 4

    # Draw a box around the face
    cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

    # Draw a label with a name below the face
    cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
    font = cv2.FONT_HERSHEY_DUPLEX
    cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
  
  cv2_imshow(frame)