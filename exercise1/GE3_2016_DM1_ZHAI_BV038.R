# Script DM1 hydrologie statistique


# Lecture le fichier de données

# Set defaut workspace
setwd(dir = "E:\\SCOLARITE\\Cours_3A\\GE3_Hydrologie\\GE3_Hydrologie_DM1\\")

# comment.char to skip lines
data=read.csv(file = "BV_38.txt", sep = ";",
              comment.char ="#")

# Check if the datas in file were inputed in Variables
head(data)

# Conversion des dates
data$Date = as.Date(x=data$Date)


# Calcul de pluie moyenne annuelle
data$An=format(x=data$Date, format="%Y")
Pa=aggregate(x=data$Ptot,
             by=list(An=data$An),
             FUN=sum)

# export two graphs in one version


names(Pa)<-c("An", "F_mean")

# Trier les pluies annuelles par valeur croissantes
tab_tri=data.frame(P_mman=sort(Pa$F_mean))


n=length(tab_tri$P_mman)


tab_tri$Rang = seq(from=1, to=n, by=1)
tab_tri$Freq = (tab_tri$Rang-0.5)/n

moy=mean(tab_tri$P_mman)
sd=sd(tab_tri$P_mman)

######################################################################
# Enlever les deux années incomplètes
tab_tri_correction = data.frame(P_mman=tab_tri$P_mman[3:n])
n_correction = length(tab_tri_correction$P_mman)
tab_tri_correction$Rang = seq(from=1, to=n_correction, by=1)
tab_tri_correction$Freq = (tab_tri_correction$Rang-0.5)/n_correction

moy_correction = mean(tab_tri_correction$P_mman)
sd_correction = sd(tab_tri_correction$P_mman)

######################################################################

# Tester la normalité
shapiro.test( tab_tri_correction$P_mman )
qqnorm(tab_tri_correction$P_mman)

# Calculer U
U = qnorm(p=tab_tri_correction$Freq)
tab_tri_correction$U = U


par( mar = c(5, 4, 4, 4 ) )
# Le plot de la version corrigée
plot(x = tab_tri_correction$U, y = tab_tri_correction$P_mman, pch = 3, col = "royalblue", cex = 1.0, 
     main = "Périod de retour [an]", xlab = "U[-]", ylab = "Pluie Moyenne Annuelle [mm/an]", 
     ylim = c(750, 1840), xlim = c(-2.5, 3) )

# Faire la fonction de Gauss
abline(a = moy_correction, b = sd_correction, col = "red2", lwd = 2.0)


# Faire les axis
label_x_explicit = c(2, 10, 50, 100, 1000)
label_x_implicit = c(0, 1.2819, 2.054, 2.23267, 3.09)
label_x_implicit_adj = c(0, 1.2819, 2.054, 2.28, 3.09)
label_y = label_x_implicit*sd_correction + moy_correction

# Faire une ceil
label_y_affiche = floor(label_y)
label_y_adj = label_y
label_y_adj[3] = label_y_adj[3]-7
label_y_adj[4] = label_y_adj[4]+7


axis(side = 3, at = label_x_implicit, labels = FALSE)
mtext(label_x_explicit, side = 3, at = label_x_implicit_adj , line = 1, 
      font = 2, col = "red", padj = 0.8)

axis(side = 4, at = label_y, labels = FALSE, las = 1)
mtext(label_y_affiche, side = 4, at = label_y_adj , line = 1, 
      font = 2, col = "red", adj = 0.1, las = 1)

# Draw lines on the graph
for (i in 1:5){
  abline(v = label_x_implicit[i], 
        lty = 3, col = "gray" )
  abline(h = label_y[i],
        lty = 3, col = "gray" )
}
legend("bottomright", legend = c("BV038(1959-2012)", "Loi normale"), 
       pch = c(3, NA), cex = 1, lty = c(NA, 1), lwd = 2, 
       col = c("royalblue", "red2"))

#######################################################################################################



# Figure pluie journalière

plot(x=data$Date,y=data$Ptot, main = "Les  Pluies  Journalières", type = "h", 
     xlab = "", ylab = "Pluie Journalière [mm]")


# Calcul de pluie moyenne annuelle
par( mfrow = c(1,2) )

plot(x = Pa,pch = 16, col = "blue", main = "Les  Pluies  Annuelles", 
     xlab = "Année", ylab = "Pluie Moyenne Annuelle [mm/an]")

# Boxplot
par(mar(3,4,4,4))
boxplot(x = tab_tri_correction$P_mman, col = "navyblue", notch = TRUE, 
        ylab = "Les Pluies Anuelles [mm/an]", xlab = "Boîte à Moustaches" )
title("Les Pluies Anuelles (1959-2012)")

# Faire un graphique montrant les pluies moyennes annuelles en fonction de leurs fréquences expérimentales

plot(x = tab_tri_correction$Freq, y = tab_tri_correction$P_mman,pch = 3, col = "skyblue3", 
     main = "Les  Pluies  Annuelles", xlab = "Fréquence(Hazen[-])", cex = 1.0, 
     ylab = "Pluie Moyenne Annuelle [mm/an]")

