import cv2
import numpy as np
from matplotlib import pyplot as plt

def analiza(numero, imagen_para_analizar):
    template = cv2.imread('imagenes/'+str(numero)+".jpg", 0)
    method = eval('cv2.TM_SQDIFF_NORMED')
    res = cv2.matchTemplate(imagen_para_analizar, template, method)
    min_val = cv2.minMaxLoc(res)[0]
    return min_val

img_para_analizar = cv2.imread('imagenes/analizar.jpg', 0)
img = img_para_analizar.copy()

template = cv2.imread("imagenes/10.jpg", 0)
w, h = template.shape[::-1]

method = eval('cv2.TM_SQDIFF_NORMED')
res = cv2.matchTemplate(img, template, method)
min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
#print("El valor es: ", str(min_val))


umbral = 0.09
loc = np.where( res <= umbral)
for pt in zip(*loc[::-1]):
    cv2.rectangle(img, pt, (pt[0] + w, pt[1] + h), (0,0,255), 2)

#top_left = min_loc
#bottom_right = (top_left[0] + w, top_left[1] + h)
#print(top_left)
#cv2.rectangle(img, top_left, bottom_right, 0, 2)

cv2.imwrite('imagenes/resultado.jpg', img)
filepath = 'imagenes/resultado.jpg'
print("listo")

