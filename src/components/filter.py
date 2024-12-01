import cv2 as cv

output_path = "output"

def blurFilter(img):
  blur = cv.GaussianBlur(img, (13, 13), 5, 0)
  cv.imwrite(output_path+"/blur.jpg", blur)
  return blur

def gray(img):
  gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
  cv.imwrite(output_path+"/gray.jpg", gray)
  return gray

filter_options = {
  'Blur': blurFilter,
  'Gray': gray
}