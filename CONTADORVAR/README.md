# ContadorVarillas

Debemos ensayar el aplicar tranformaciones morfologicas especificas a objetos individuales se puede hacer de la siguiente manera:

1. Encontrar los contornos en la imagen
2. Encontrar el bounding box
3. Para cada bounding box tomarlo como ROI recortar la imagen
4. Aplicar la tranformación dependiendo de la forma y el tamaño de dicha ROI 
5. Luego volver a la imagen completa mediante una operacion bit a bit (i.e AND) o con operaciones de máscara
6. Donde se logre mera chimbita