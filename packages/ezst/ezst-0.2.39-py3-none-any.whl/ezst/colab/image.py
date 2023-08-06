import matplotlib.image as mpimg
import matplotlib.pyplot as plt


def read(file_path):
  return mpimg.imread(file_path)

def show(img, grid=False, size=(12,12)):
  plt.figure(figsize=size)
  plt.grid(grid)
  plt.imshow(img)
  plt.show()
