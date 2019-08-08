library(data.table)



file <- 'C:/ftirdb/ftirdb/data/kinetics/.csv'
file2 <- 'C:/ftirdb/ftirdb/data/kinetics/ou3.csv'
spectra <- read.csv(file2, header = TRUE, row.names = 1)

#transpose data
new2 <- transpose(spectra)
pca <- prcomp(new2,
                    center = TRUE,
                    scale =TRUE,
                    rank. = 10,
              )
summary(pca)

plot(pca$x[, 1], pca$x[, 2], pch=21, bg=c("blue","cyan","green","red"), main =
       "PCA", xlab = "PC1", ylab = "PC2") 

mydata<-data.frame(pca$x[, 1],pca$x[, 2]) 
withingroupss <- (nrow(mydata)-1)*sum(apply(mydata,2,var))
for (i in 2:8) withingroupss[i] <- sum(kmeans(mydata,centers=i)$withinss)
par(pin=c(5,5),font=2,ps=10,family="sans")
plot(1:8, withingroupss[1:8], type="b", xlab="Number of Clusters",
     ylab="Within groups sum of squares") 
myclusters <- kmeans(mydata,4) 
mynewdata <- data.frame(mydata, myclusters$cluster,c(rep("A",100),rep("B",100),rep("C",100),rep("D",100)) )
View(mynewdata) 
library(cluster)
clusplot(mydata, myclusters$cluster,color=TRUE, shade=TRUE, labels=1, lines=0)
library(cluster) 
