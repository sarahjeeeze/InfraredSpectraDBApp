library(data.table)
library(pca3d)
library(plot3D)
library(scatterplot3d)
par(pin=c(3,3),mfrow=c(1,1),font=2,ps=10,family="sans")

file <- 'C:/ftirdb/R/alldata.csv'
spectra <- read.csv(file, header = TRUE, row.names = 1)

pca <- prcomp(spectra,
              center = TRUE,
              scale =TRUE,
              rank. = 10,
)
summary(pca)

plot(pca$x[, 1], pca$x[, 2], pch=10, bg=c("blue","cyan","green","red"), main =
       "PCA", xlab = "PC1", ylab = "PC2") 

scatterplot3d(pca$x[, 1], pca$x[, 2],pca$x[, 3], main="3D Scatterplot" )


mydata<-data.frame(pca$x[, 1],pca$x[, 2]) 
withingroupss <- (nrow(mydata)-1)*sum(apply(mydata,2,var))
for (i in 2:10) withingroupss[i] <- sum(kmeans(mydata,centers=i)$withinss)
plot(1:10, withingroupss[1:10], type="b", xlab="Number of Clusters",
     ylab="Within groups sum of squares") 

myclusters <- kmeans(spectra,3) 
one <- c(rep("Lympho",0),rep("Epithel",101),rep("Erythr",100),rep("Fibro",100))
mynewdata <- data.frame(mydata, myclusters$cluster,one)
View(mynewdata) 
library(cluster)
clusplot(mynewdata, myclusters$cluster,color=TRUE, shade=TRUE, labels=3, lines=0)
library(cluster) 
pca3d(mynewdata)
