import cv2 as cv

def blurFilter(img):
  return cv.GaussianBlur(img, (13, 13), 5, 0)

filter_options = {
  'blur': blurFilter
}