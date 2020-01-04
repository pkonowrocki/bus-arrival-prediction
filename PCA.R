path ='C://Users/arkadiusz.ryszewski/Desktop/PPD - Project/bus-arrival-prediction/data/';
filename = 'all-lines.csv'

data = read.csv(paste(path,filename,sep=''))

pca = prcomp(data, center = TRUE, scale. = TRUE)

print(pca)
summary(pca)

ggbiplot(pca)
ggscreeplot(pca)