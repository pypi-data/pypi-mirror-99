import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import cv2

def rectangle(img, lt, rb):
  return cv2.rectangle(img, lt, rb, (255, 0, 0), 3)

def read(file_path):
  return mpimg.imread(file_path)

def show(img, grid=False, size=None):
  plt.figure(figsize=size)
  plt.grid(grid)
  plt.imshow(img)
  plt.show()
