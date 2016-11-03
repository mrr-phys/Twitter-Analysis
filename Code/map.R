
setwd("/Volumes/Projet2/")

###########################################################
# filemap <- read.table("Data/user_most_time.dat")
# library(maps)
# #pdf("Graphs/network_ME_users.pdf")
# map()
# #map("world",c("Syria","Iraq","Turkey","Egypt","Iran","Saudi Arabia","Yemen","Oman",
# #              "Israel","Jordan","Lebanon","United Arab Emirates"))
# Nb <- length(filemap[,1])
# coeff <- 0.5
# 
# for (i in 1:Nb) {
#     x0 <- filemap[i,1]
#     y0 <- filemap[i,2]
#     x1 <- filemap[i,3]
#     y1 <- filemap[i,4]
#     #poids <- filemap[i,5]
#     #lines(c(x0,x1),c(y0,y1),col="red",lwd=coeff*poids)
#     
# }
# #dev.off()

file <- read.table("Data/users_most_time_out.dat")
jet.colors <- colorRampPalette(c("#003399", "#7DF9FF"))(256)

edge <- function(x)
{
  maxValue <- 199
  value <- as.integer(log10(x[5])/log10(maxValue)*256)+1
  lines(y=c(x[2],x[4]),x=c(x[1],x[3]),col=jet.colors[value], lwd=log10(x[5])/log10(maxValue)*20)
}

plot_path <- function(data)
{
  library(maps)
  library(mapdata)
  map('worldHires')
  #map('worldHires', regions=c('Iraq','Jordan','Turkey','Syria','Israel','Saudi Arabia',
  #                            'Iran','Egypt',"Yemen","Oman","Lebanon","United Arab Emirates"))
  o <- order(data$V5)
  apply(data[o,], 1, edge)
  map('worldHires', bg=NA, add=T)
}

pdf("Graphs/most_used_places_out20.pdf")
plot_path(file)
dev.off()
#####################################################

######################################################
########### 2. Most visited places by users ########################
# file <- read.table("Data/most_visit_01.dat")
# library(maps)
# Nuser <- length(file[,1])
# coeff <- 0.01
# 
# #pdf("Graphs/most_visit_01_2.pdf")
# map("world")
# for (user in 1:Nuser) {
#   x <- file[user,2]
#   y <- file[user,3]
#   poids <- file[user,4]
#   points(x,y,col="red",pch=20,cex=poids*coeff)
# }
# #dev.off()
###########################################


##########################################
###### Distance VS normalized weights
# file <- read.table("Data/distance_VS_normweight_box.dat",fill=T)
# data <- t(file)
# nw <- data[1,]
# Nbweight <- length(nw)
# mean <- rep(0,Nbweight)
# 
# for (i in 1:Nbweight) {
#   mean[i] <- mean(data[,i],na.rm=T)
# }
# 
# boxplot(data ~ nw)
# 
# # plot(nw,mean,pch=20,cex=0.5
# #      #xlim=c(0,0.4),
# #      #ylim=c(0,4000)
# #      )

#print(file)
#nw <- file[,1]
#dt <- file[,2]
#length(file[,1])
# for (line in 1:3) {
#   boxplot(t(file[line,-1]))
# }

#boxplot(t(file[1,-1]))
#############################################


###############################################
# ### Graph of most used places
# file <- read.table("Data/users_most_time.dat",fill=T)
# library(maps)
# #pdf("Graphs/most_used_places_bis.pdf")
# map()
# #map("world",c("Syria","Iraq","Turkey","Egypt","Iran","Saudi Arabia","Yemen","Oman",
# #              "Israel","Jordan","Lebanon","United Arab Emirates"))
# Nb <- length(filemap[,1])
# for (i in 1:Nb) {
#   x0 <- filemap[i,2]
#   y0 <- filemap[i,3]
#   x1 <- filemap[i,4]
#   y1 <- filemap[i,5]
#   x2 <- filemap[i,6]
#   y2 <- filemap[i,7]
#   lines(c(x0,x1),c(y0,y1),col="blue",lwd=0.1)
#   if (!is.na(x2)) {lines(c(x1,x2),c(y1,y2),col="blue",lwd=0.1)}
#   points(x0,y0,col="red",pch=20,cex=0.5)
#   points(x1,y1,col="red",pch=20,cex=0.5)
#   points(x2,y2,col="red",pch=20,cex=0.5)
# }
# #dev.off()





