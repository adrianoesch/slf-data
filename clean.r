setwd('~/Documents/opendata/slf/')
d <- read.csv('rawData.csv',header=T,stringsAsFactors = F)
names(d)<-c('dateStr','coord','value')
d$date <- as.Date(d$X0)
coords <- unlist(lapply(LETTERS[1:22],function(i)lapply(1:34,function(j)paste0(i,j))))
names(daysPerMonth) <- months
naPerCoord <- unlist(lapply(coords,function(i)sum(!is.na(d$value[d$coord==i]))))
names(naPerCoord)<-coords
legendCoords <- unlist(lapply(29:30,function(i)paste0(LETTERS[1:4],i)))
coordSel <- coords[naPerCoord[coords]>2300]
  
cats <- c(0,5,12.5,27.5,65)
names(cats)<-c('0','1','2','3','4')

d2 <- subset(d,!is.na(value) & coord%in%coordSel & !coord%in%legendCoords) 
d2$date <- as.Date(d2$dateStr)
d2$year <- format(d2$date,"%Y")
d2$month <- format(d2$date,"%b")
d2$catStr <- as.character(d2$value)
d2$cm <- cats[d2$catStr]

write.csv(d2,'cleanData.csv')

