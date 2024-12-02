import cv2 as cv
import numpy as np

output_path = "output"

def blurFilter(img):
  blur = cv.GaussianBlur(img, (13, 13), 5, 0)
  cv.imwrite(output_path+"/blur.jpg", blur)
  return blur

def gray(img):
  gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
  cv.imwrite(output_path+"/gray.jpg", gray)
  return gray

def blueFilter(img):
  blue = cv.cvtColor(img, cv.COLOR_BGRA2RGBA)
  cv.imwrite(output_path+"/blue.jpg", blue)
  return blue

def neonInverted(img):
  neonInverted = cv.cvtColor(img, cv.COLOR_RGB2YCrCb)
  cv.imwrite(output_path+"/neonInverted.jpg", neonInverted)
  return neonInverted

def greenGlitch(img):
  greenGlitch = cv.cvtColor(img, cv.COLOR_BGR2HLS_FULL)
  cv.imwrite(output_path+"/greenGlitch.jpg", greenGlitch)
  return greenGlitch

def increaseSaturation(img):
  increaseSaturation = cv.cvtColor(img, cv.COLOR_XYZ2RGB)
  cv.imwrite(output_path+"/increaseSaturation.jpg", increaseSaturation)
  return increaseSaturation

def inverted(img):
  inverted = cv.flip(img,-1)
  cv.imwrite(output_path+"/inverted.jpg", inverted)
  return inverted

def thresholding(img):
  ret,thresh4 = cv.threshold(img,127,255,cv.THRESH_TOZERO)
  cv.imwrite(output_path+"/thresholding.jpg", thresh4)
  return thresh4

def exposure(img):
  exposure_kernel = np.array([[0, -1, 0], 
                    [-1, 7, -1], 
                    [0, -1, 0]]) 
  exposure = cv.filter2D(src=img, ddepth=-1, kernel=exposure_kernel)
  cv.imwrite(output_path+"/exposure.jpg", exposure)
  return exposure

def negative(img):
  kernel = cv.getStructuringElement(cv.MORPH_CROSS,(5,5))
  negative = cv.morphologyEx(img, cv.MORPH_GRADIENT, kernel)
  cv.imwrite(output_path+"/negative.jpg", negative)
  return negative

filter_options = {
  'Blur': blurFilter,
  'Gray': gray,
  'Blue': blueFilter,
  'Neon': neonInverted,
  'Green Glitch': greenGlitch,
  '+Sturation': increaseSaturation,
  'Inverted': inverted,
  'Thresholding': thresholding,
  '+Exposure': exposure,
  'Negative': negative,
  'Remove Filtros': None
}