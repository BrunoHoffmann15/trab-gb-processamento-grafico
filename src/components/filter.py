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
  inverted = cv.flip(img, -1)
  cv.imwrite(output_path+"/teste.jpg", inverted)
  return inverted

filter_options = {
  'Blur': blurFilter,
  'Gray': gray,
  'Blue': blueFilter,
  'Neon': neonInverted,
  'Green Glitch': greenGlitch,
  '+Sturation': increaseSaturation,
  'Inverted': inverted,
}