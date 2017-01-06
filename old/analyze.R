setwd('~/Documents/opendata/slf/')
# setwd('Z:/')
library(png)
library(ggplot2)

d <- read.csv('cleanData.csv',stringsAsFactors = F)
coords <- unlist(lapply(LETTERS[1:22],function(i)lapply(1:34,function(j)paste0(i,j))))
coordX <- as.integer(substr(coords,2,nchar(coords)))
names(coordX) <- coords
coordY <- sapply(coords,function(i)23-grep(substr(i,0,1),LETTERS))
names(coordY) <- coords

months <- c("Nov","Dec","Jan","Feb","Mar","Apr","May")
daysPerMonth <- c(30,31,31,28,31,30,31)

monthSel <- c("Dec","Jan","Feb","Mar","Apr")
d3 <- d2[d2$month%in%monthSel,]

isDump <- function(i){
  cms <- d3[d3$date>d3$date[i]-1&d3$date<=d3$date[i]&d3$coord==d$coord[i],'cm']
  if (sum(cms,na.rm=T)>50){
    return(1)
  }else{
    return(0)
  }
}

d3$dump <- sapply(1:nrow(d3),isDump) 


d3 <- read.csv('cleanData2.csv',stringsAsFactors = F)

s1<-data.frame(aggregate(cm~coord+year+month,d3,sum))
s2<-data.frame(aggregate(dump~coord+year+month,d3,sum))

s<-merge(s1,s2,by=c('coord','year','month'))

write.csv(s,'monthlySums.csv',row.names=F)

# bg <- readPNG('template_transparent.png')
# 
# withoutTicks <- theme(
#   axis.ticks=element_blank(),
#   axis.text=element_blank(),
#   axis.title=element_blank(),
#   panel.background=element_blank())

# p<-ggplot(data=y[y$month=='Dec',],aes(x=coordX[coord],y=coordY[coord],fill=cm))+
#   ylim(c(0,22))+xlim(0,34)+geom_tile()+withoutTicks+coord_fixed()+
#   annotation_custom(rasterGrob(bg),xmin=0,ymin=0,xmax=33,ymax=24)
# p<-ggplot(data=y[y$month=='Dec',],aes(x=coordX[coord],y=coordY[coord],fill=cm))+
#   ylim(c(0,22))+xlim(0,33)+geom_tile()+withoutTicks+coord_fixed()


# ggplotly(p)
# ,
#          layout =
#            images = list(
#              list(source = "https://images.plot.ly/language-icons/api-home/python-logo.png",
#                   xref = "paper",
#                   yref = "paper",
#                   x= 0,
#                   y= 0,
#                   sizex = 1,
#                   sizey = 1,
#                   opacity = 0.8
#              )))

