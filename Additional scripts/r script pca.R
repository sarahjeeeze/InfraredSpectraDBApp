library(data.table)
library(plot3D)
file <- 'C:/ftirdb/ftirdb/data/kinetics/out.csv'
spectra <- read.csv(file, header = FALSE, row.names = 1)
#transpose data
new2 <- transpose(spectra)
pca <- prcomp(new2,
                    center = TRUE,
                    scale =TRUE,
                    rank. = 10,
              )
summary(pca)

scatter3D(pca$x[, 1], pca$x[, 2], pca$x[,3],pch=21, bg=c("blue","cyan","green","red"), main =
       "PCA", xlab = "PC1", ylab = "PC2") 

mydata<-data.frame(pca$x[, 1],pca$x[, 2]) 
data3d <-data.frame(pca$x[, 1],pca$x[, 2],pca$x[,3])
withingroupss <- (nrow(mydata)-1)*sum(apply(mydata,2,var))
withingroupss3d <- (nrow(data3d)-1)*sum(apply(data3d,2,var))
for (i in 2:8) withingroupss[i] <- sum(kmeans(mydata,centers=i)$withinss)
for (i in 2:8) withingroupss3d[i] <- sum(kmeans(data3d,centers=i)$withinss)

par(pin=c(5,5),font=2,ps=10,family="sans")
plot(1:8, withingroupss[1:8], type="b", xlab="Number of Clusters",
     ylab="Within groups sum of squares") 
myclusters <- kmeans(mydata,4) 
mynewdata <- data.frame(data3d, myclusters$cluster,c(rep("A",100),rep("B",100),rep("C",100),rep("D",100)) )
View(mynewdata) 
library(cluster)
clusplot(mynewdata, myclusters$cluster,color=TRUE, shade=TRUE, labels=1, lines=0)
library(cluster) 

plot(1:8, withingroupss3d[1:8], type="b", xlab="Number of Clusters",
     ylab="Within groups sum of squares") 

scatter3D(clusplot(mynewdata, myclusters$cluster,color=TRUE, shade=TRUE, labels=1, lines=0))

