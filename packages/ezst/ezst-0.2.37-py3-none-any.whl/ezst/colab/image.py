import matplotlib.image as mpimg
import matplotlib.pyplot as plt


def show(file_path, grid=False, size=(12,12)):
  img = mpimg.imread(file_path)
  plt.grid(grid)
  plt.figure(figsize=size)
  plt.imshow(img)
  plt.show()


