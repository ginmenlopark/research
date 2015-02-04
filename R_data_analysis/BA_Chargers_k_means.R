##############################
# Nissan Hackathon
# April 27, 2014
# EVenture, Team #5
# Backend routing calculation step:  
# clustering charging stations to provide alternatives
# within our energy-aware routing algorithm.

require(graphics)
library(RgoogleMaps)

setwd("C://EVenture_working")
getwd()

bay_area_chargers = read.csv("BayAreaChargersInfoLatLong.csv")
colnames(bay_area_chargers)
BA_charger_data = as.data.frame(bay_area_chargers)
#summary(bay_area_chargers)
#####################################################################
#--Let's look at some interesting charge spots
north_idx = which(bay_area_chargers$Lat == max(bay_area_chargers$Lat))
south_idx = which(bay_area_chargers$Lat == min(bay_area_chargers$Lat))
north_lat = bay_area_chargers$Lat[north_idx]
north_lng = bay_area_chargers$Long[north_idx]
south_lat = bay_area_chargers$Lat[south_idx]
south_lng = bay_area_chargers$Long[south_idx]

bach = bay_area_chargers

x = cbind(bach$Lat, bach$Long)

# a 2-dimensional example
#x <- rbind(matrix(rnorm(100, sd = 0.3), ncol = 2),
#           matrix(rnorm(100, mean = 1, sd = 0.3), ncol = 2))


colnames(x) <- c("x", "y")
starbucks = c(37.4848742, -122.2298206)
x = rbind(x,starbucks)
(cl <- kmeans(x, 2))
plot(x, col = cl$cluster)
points(cl$centers, col = 1:2, pch = 8, cex = 2)

# sum of squares
ss <- function(x) sum(scale(x, scale = FALSE)^2)

## cluster centers "fitted" to each obs.:
fitted.x <- fitted(cl);  head(fitted.x)
resid.x <- x - fitted(cl)

## Equalities : ----------------------------------
cbind(cl[c("betweenss", "tot.withinss", "totss")], # the same two columns
      c(ss(fitted.x), ss(resid.x),    ss(x)))
stopifnot(all.equal(cl$ totss,        ss(x)),
          all.equal(cl$ tot.withinss, ss(resid.x)),
          ## these three are the same:
          all.equal(cl$ betweenss,    ss(fitted.x)),
          all.equal(cl$ betweenss, cl$totss - cl$tot.withinss),
          ## and hence also
          all.equal(ss(x), ss(fitted.x) + ss(resid.x))
)

kmeans(x,1)$withinss # trivial one-cluster, (its W.SS == ss(x))

## random starts do help here with too many clusters
## (and are often recommended anyway!):
(cl <- kmeans(x, 5, nstart = 25))
#(cl <- kmeans(x,70,nstart=100))

z= cbind(x[,2],x[,1])
#starbucks = c(37.4848742, -122.2298206)
#zzvec = rbind(zvec,starbucks)
plot(z, col = cl$cluster)
points(cl$centers, col = 1:5, pch = 8)

#center = c(mean(trip_gps_data$lat), mean(trip_gps_data$lon))
#center = c(37.49608,-122.2260) #--as a test
center = c(bach$Lat[311],bach$Lon[311])
center = c(north_lat, north_lng)

#--Zoom level 11 is about right for these trips.  
#--Higher values zoom in more; at 14 it's too zoomed in.
zoom = 15
MyMap <- GetMap(center=starbucks, zoom=zoom);

#--marker colors might be 'green','red','black','brown',...
tmp <- PlotOnStaticMap(MyMap, lat = north_lat,
                       lon = north_lng,
                       cex=1.5,pch=17,
                       col="black", add=FALSE); 

PlotOnStaticMap(MyMap, lat = starbucks[1],
                lon = starbucks[2],
                cex=3.0,pch=15,
                col="black", add=TRUE); 

#PlotOnStaticMap(MyMap, lat = x[,1],
#                lon = x[,2],
#                cex=1.5,pch=cl$cluster,
#                col=cl$cluster, add=TRUE); 

#text(x[,1],x[,2],label=cl$cluster,col=cl$cluster)
#TextOnStaticMap(MyMap, lat = x[,1],lon = x[,2], cl$cluster, cex=0.9, col = cl$cluster, add=TRUE)

TextOnStaticMap(MyMap, lat = x[,1],lon = x[,2], bach$OBJECTID.., cex=1.5, col = cl$cluster, add=TRUE)
