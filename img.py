import  cv2
fname = "C:/Users/INTECOL CAMPO/Pictures/Saved Pictures/Captura.PNG"

image = cv2.imread(fname)
cv2.imshow("image",image)
cv2.waitKey(0)
cv2.destroyAllWindows()