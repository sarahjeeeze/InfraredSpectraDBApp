x <- seq(900,2300,2)
y <- seq(-10,100,20)
x1<-x[rev(order(x))] 
par(pin=c(6,4),mfrow=c(1,1),font=2,ps=10,family="sans")

ylim=c(-200,300)
plot(x1,trans[,1],ylim=c(-10,120),type="solid", xlim=rev(range(x)),xlab="Wavelengths cm^-1",ylab="Absorbance")


for (i in 1:100){
  lines(x1,trans[,i],type="solid", xlim=rev(range(x)),col="navy")
}

for (i in 100:200){
  lines(x1,trans[,i],type="solid", xlim=rev(range(x)),col="red")
}

for (i in 200:300){
  lines(x1,trans[,i],type="solid", xlim=rev(range(x)),col="forestgreen")
}

for (i in 300:400){
  lines(x1,trans[,i],type="solid", xlim=rev(range(x)),col="deeppink")
}