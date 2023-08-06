import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import cv2

def rectangle(img, lt, rb):
  return cv2.rectangle(img, lt, rb, (255, 0, 0), 3)

def read(file_path):
  return mpimg.imread(file_path)


def save(file_path, img):
  # image = cv2.imread('ssak.jpg', cv2.IMREAD_COLOR)
  img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  
  cv2.imwrite(file_path, img)

def save2(file_path, img):
  # image = cv2.imread('ssak.jpg', cv2.IMREAD_COLOR)
  img = cv2.cvtColor(img, cv2.IMREAD_COLOR)  
  cv2.imwrite(file_path, img)

def show(img, grid=False, size=None):
  plt.figure(figsize=size)
  plt.grid(grid)
  plt.imshow(img)
  plt.show()
