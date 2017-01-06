setwd('Z:/Users/oescha/')
library(png)
library(ggplot2)

d <- read.csv('cleanData.csv',stringsAsFactors = F)
d$date <- as.Date(d$dateStr)
coords <- unlist(lapply(LETTERS[1:22],function(i)lapply(1:34,function(j)paste0(i,j))))
coordX <- as.integer(substr(coords,2,nchar(coords)))
names(coordX) <- coords
coordY <- sapply(coords,function(i)23-grep(substr(i,0,1),LETTERS))
names(coordY) <- coords

months <- c("Nov","Dec","Jan","Feb","Mar","Apr","May")
daysPerMonth <- c(30,31,31,28,31,30,31)

monthSel <- c("Dec","Jan","Feb","Mar","Apr")
d3 <- d[d$month%in%monthSel,]

row.names(d3) <- paste0(d3$dateStr,'-',d3$coord)

isDump <- function(i){
  yesterday <- paste0(as.character(d3$date[i]-1),'-',d3$coord[i])
  cm1 <- d3[paste0(d3$dateStr[i],'-',d3$coord[i]),'cm']
  cm2 <- ifelse(yesterday %in% row.names(d3),d3[yesterday,'cm'],0)
  if (sum(c(cm1,cm2))>30){
    return(1)
  }else{
    return(0)
  }
}

d3$dump <- sapply(1:nrow(d3),isDump) 

write.csv(d3,'cleanData3.csv',row.names = F)

s<-aggregate(cm~coord+year+month,d3,sum)
s<-cbind(s,aggregate(dump~coord+year+month,d3,sum))
s$season = ifelse(as.character(s$month)=='Dec',s$year+1,s$year)

write.csv(s,'monthlySums3.csv',row.names=F)


