#Ítrun 1: Ráðstafaður tími:	0	5,38
#Lengd ítrunar:	4,3	0
#Ítrun 2:
#Ráðstafaður tími:	0	7,14
#Lengd ítrunar:	5	0
#Ítrun 3:
#Ráðstafaður tími:	0	12
#Lengd ítrunar:	9	0
pdf={
pdf('Burndown1.pdf')
x1<-c(6,5,4,3,2,1,0)
y1<-c(4.3,4.3,4.3,2.5,0.5,0.5,0)
plot(x1,y1,type='l',col='red',main='Burndown Ítrun 1, 30. 1. - 5. 2.',xlab='Dagar til stefnu',ylab='Vinna eftir (Í dögum)',xlim=rev(range(0:6)))
lines(c(6,0),c(4.3,0))
dev.off()
}

pdf={
pdf('Burndown2.pdf')
x2<-c(7,6,5,4,3,2,1,0)
y2<-c(5,4,4,4,4,2.3,0,0)
plot(x2,y2,type='l',col='red',main='Burndown Ítrun 2, 6. 2. - 12. 2.',xlab='Dagar til stefnu',ylab='Vinna eftir (Í dögum)',xlim=rev(range(0:7)))
lines(c(7,0),c(5,0))
dev.off()
}

pdf={
pdf('Burndown3.pdf')
x3<-c(6,5,4,3,2,1,0)
y3<-c(8,8,7,4,4,1,0)
plot(x3,y3,type='l',col='red',main='Burndown Ítrun 3, 13. 2. - 19. 2.',xlab='Dagar til stefnu',ylab='Vinna eftir (Í dögum)',xlim=rev(range(0:6)))
lines(c(6,0),c(8,0))
dev.off()
}
