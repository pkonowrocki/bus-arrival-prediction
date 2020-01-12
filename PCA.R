path ='C://Users/arkadiusz.ryszewski/Desktop/PPD - Project/bus-arrival-prediction/data/';
filename = 'all.csv';

data = read.csv(paste(path,filename,sep=''));

data = na.omit(data);

pca = prcomp(data, center = TRUE, scale. = TRUE);

print(pca)
summary(pca)

require (ggbiplot)
ggbiplot(pca)
ggscreeplot(pca)