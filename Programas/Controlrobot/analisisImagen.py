import cv2
import numpy as np
from matplotlib import pyplot as plt

img_para_analizar = cv2.imread('analizar.jpg', 0)
img = img_para_analizar.copy()

template = cv2.imread("segundo10.jpg", 0)
w, h = template.shape[::-1]

method = eval('cv2.TM_SQDIFF_NORMED')
res = cv2.matchTemplate(img, template, method)
min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
print("El valor es: ", str(min_val))

top_left = min_loc
bottom_right = (top_left[0] + w, top_left[1] + h)
print(top_left)
cv2.rectangle(img, top_left, bottom_right, 0, 2)

cv2.imwrite('resultado.jpg', img)
filepath = 'resultado.jpg'
print("listo")

