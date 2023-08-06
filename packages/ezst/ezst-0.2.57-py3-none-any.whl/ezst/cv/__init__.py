import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import requests

import cv2
from PIL import ImageFont

def read(file_path):
  return mpimg.imread(file_path)

def save(file_path, img):
  img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  
  cv2.imwrite(file_path, img)

def show(img, grid=False, size=(12,12)):
  plt.figure(figsize=size)
  plt.grid(grid)
  plt.imshow(img)
  plt.show()

def rectangle(img, lt, rb, thickness=3, color=(255, 0, 0)):
  return cv2.rectangle(img, lt, rb, color, thickness=thickness)

def line(img, pt1, pt2, thickness=3, color=(255, 0, 0)):
  return cv2.line(img, pt1, pt2, color, thickness=thickness)

def circle(img, center, axes, thickness=3, color=(255, 0, 0)):
  return cv2.circle(img, center, radius, color, thickness=thickness)




def text(img, text, pt1, size=2, color=(255, 0, 0)):
  save_path = 'malgun.ttf'

  url = 'https://www.wfonts.com/download/data/2016/06/13/malgun-gothic/malgun.ttf'
  r = requests.get(url, stream=True)
  with open(save_path, 'wb') as fd:
      for chunk in r.iter_content(chunk_size=128):
          fd.write(chunk)

  font = ImageFont.truetype("malgun.ttf", 20)
  return cv2.putText(img, text, pt1, font, size,color,2)