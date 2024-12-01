import cv2 as cv

output_path = "Output"

def blurFilter(img):
  blur = cv.GaussianBlur(img, (13, 13), 5, 0)
  _, binary = cv.threshold(blur, 128, 255, cv.THRESH_BINARY)
  cv.imwrite(output_path+"/blur.jpg", binary)
  return blur

def gray(img):
  gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
  _, binary = cv.threshold(gray, 128, 255, cv.THRESH_BINARY)
  cv.imwrite(output_path+"/gray.jpg", binary)
  return gray

filter_options = {
  'Blur': blurFilter,
  'Gray': gray
}