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