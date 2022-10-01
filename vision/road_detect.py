import cv2
import matplotlib.pyplot as plt

if __name__ == "__main__":
  image = cv2.imread('/home/edwin/Picohack-2022/vision/img1.png')
  grey_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
  kernel_size = 5
  blur_gray = cv2.GaussianBlur(grey_image,(kernel_size, kernel_size),0)
  imgplot = plt.imshow(blur_gray)
