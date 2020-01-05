path ="/home/tpalayda/Desktop/studying/ppd/project/2018-05-26/"
filename = "part-0-0"

data = read.csv2(paste(path, filename, sep='')) 

data.pca <- prcomp(waw, center = TRUE, scale. = TRUE)

print(waw.pca)
summary(waw.pca)

require(ggbiplot)
ggbiplot(waw.pca)
ggscreeplot(waw.pca)

#Zadanie 1

#kryterium wlasnosci wlasnej
#kazda skladowa powinna tlumaczyc zmiennosc rowna przynajmniej jednej zmiennej podstawowej
#dlatego mozna wybrac skladowe o wartosciach wiekszych niz 1 (tutaj mowimy o standard deviation)
#metoda moze powodowac wybor zbyt malej liczby skladowych dla mniej niz 20 zmiennych i zbyt duzej dla powyzej 50 zmiennych
#sa 2 powyzej 1, ale 3 jest blisko 0.9642, i ze wzgledu na mala liczbe zmiennych 
#i wartosc std trzeciej skladowej bliskiej 1 to wybieramy 3.
#
#Kryterium czesci wyjasnionej wariancji (90%)
#Kryterium wyjasnionej wariancji wielkosci wariancji wielkosci 90% nakazuje wybrac 3 skladowe??
#
#kryterium osypiskowe 4??
#
#Kryterium minimalnego zasobu zmiennosci wspolnej
#
#
power <- function(a) {
  return (a * a)
}
power(5)
power(waw.pca)
print(waw.pca)

#wartosc rotacji varimax wiecej niz 2 czynniki bo dla 2 wyniki beda takie same

#za tydzien bardzo podobne zadania na innym zbiorze, 4 zadania