path ='C://Users/arkadiusz.ryszewski/Desktop/PPD - Project/bus-arrival-prediction/data/';
filename = 'all.csv';

data = read.csv(paste(path,filename,sep=''));

data = na.omit(data);

timezone = "Europe/Warsaw";
format = "%d.%m.%YT%H:%M:%S";
data$time <- as.POSIXct(data$time, format, tz = timezone);
data$plannedLeaveTime <- as.POSIXct(data$plannedLeaveTime, format, tz = timezone);
data$previousStopArrivalTime <- as.POSIXct(data$previousStopArrivalTime, format, tz = timezone);
data$previousStopLeaveTime <- as.POSIXct(data$previousStopLeaveTime, format, tz = timezone);
data$nextStopTimetableVisitTime <- as.POSIXct(data$nextStopTimetableVisitTime, format, tz = timezone);
data$plannedLeaveTime <- as.POSIXct(data$plannedLeaveTime, format, tz = timezone);

pca = prcomp(data, center = TRUE, scale. = TRUE);

print(pca)
summary(pca)

ggbiplot(pca)
ggscreeplot(pca)