library(data.table)
library(pca3d)
library(plot3D)
library(scatterplot3d)

file <- 'C:/ftirdb/R/alldata.csv'
spectra <- read.csv(file, header = TRUE, row.names = 1)

pca <- prcomp(spectra,
              center = TRUE,
              scale =TRUE,
              rank. = 10,
)
summary(pca)

plot(pca$x[, 1], pca$x[, 2], pch=6, bg=c("blue","cyan","green","red"), main =
       "PCA", xlab = "PC1", ylab = "PC2") 

scatterplot3d(pca$x[, 1], pca$x[, 2],pca$x[, 3], main="3D Scatterplot" )


mydata<-data.frame(pca$x[, 1],pca$x[, 2], pca$x[, 3]) 
withingroupss <- (nrow(mydata)-1)*sum(apply(mydata,2,var))
for (i in 2:8) withingroupss[i] <- sum(kmeans(mydata,centers=i)$withinss)
par(pin=c(5,5),font=2,ps=10,family="sans")
plot(1:8, withingroupss[1:8], type="b", xlab="Number of Clusters",
     ylab="Within groups sum of squares") 

myclusters <- kmeans(spectra,4) 
mynewdata <- data.frame(mydata, myclusters$cluster,c(rep("A",100),rep("B",100),rep("C",100),rep("B",100) ))
View(mynewdata) 
library(cluster)
clusplot(mynewdata, myclusters$cluster,color=TRUE, shade=TRUE, labels=2, lines=0)
library(cluster) 
pca3d(mynewdata)
