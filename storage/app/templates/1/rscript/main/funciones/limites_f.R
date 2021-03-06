limites_f <- function(info_name,ts_seriesFull) {
  # L�mites para evaluadores fisicos 
  #------------------------------------------------------------------------------------------------------------
  # De acuerdo al plan de expansi�n 2015 se proponen los siguientes evaluadores de error. 
  # Los par�metros que se calculan son i) media, ii) desviaci�n est�ndar, iii) mediana, 
  # iv) coeficiente de variaci�n, v) desviaci�n media, vi) percentiles 97.5 y 2.5% y 
  # vii) valores m�ximo y m�nimo.
  # Luego, para cada una de las series se cuantifican los indicadores p y q, que establecen el potencial impacto
  # de la serie en los resultados del SDDP, determinando cuantas plantas de la totalidad simulada est�n asociada
  # a una serie que estad�sticamente no satisface los intervalos de confianza fijados. Adicionalmente, se determina
  # para ese mismo n�mero de plantas, la capacidad instalada comprometida. Las siguientes expresiones
  # matem�ticas resumen este c�lculo.
  
  #   Par�metro                   Variaci�n m�xima 
  # Evaluaci�n de medias                35%
  # Desv. Estandar                      50%
  # Mediana                             35%
  # Coef. de variaci�n                  35%
  # Desv. media                         40%
  # Percentil 97.5%                     30%
  # percentil 2.5%                      30%
  # M�ximo valor caudal                 50%
  # M�nimo valor caudal                 50%
  #------------------------------------------------------------------------------------------------------------
  
  # Valores de referencia 
  # 1. Evaluaci�n de medias
  ts_series_medias = array(dim=c(length(info_name),1))
  for (i in 1:length(info_name)) {
    ts_series_medias[i] = mean(ts_seriesFull[,i])
  }
  limMax_medias = ts_series_medias*(1+0.35)
  limMin_medias = ts_series_medias*(1-0.35)
  
  # 2. Desv. Estandar
  ts_series_desvE = array(dim=c(length(info_name),1))
  for (i in 1:length(info_name)) {
    ts_series_desvE[i] = sd(ts_seriesFull[,i])
  }
  limMax_desvE = ts_series_desvE*(1+0.5)
  limMin_desvE = ts_series_desvE*(1-0.5)
  
  # 3. Mediana  
  ts_series_mediana= array(dim=c(length(info_name),1))
  for (i in 1:length(info_name)) {
    ts_series_mediana[i] = median(ts_seriesFull[,i])
  }
  limMax_mediana= ts_series_mediana*(1+0.35)
  limMin_mediana= ts_series_mediana*(1-0.35)
  
  # 4. Coeficiente de variaci�n 
  ts_series_CV = ts_series_desvE/ts_series_medias
  limMax_CV = ts_series_CV*(1+0.35)
  limMin_CV = ts_series_CV*(1-0.35)
  
  # 5. Mean. Dev
  ts_series_meanD = array(dim=c(length(info_name),1))
  for (i in 1:length(info_name)) {
    ts_series_meanD[i] = mad(ts_seriesFull[,i], center = median(ts_seriesFull[,i]))
  }
  limMax_meanD = ts_series_meanD*(1+0.40)
  limMin_meanD = ts_series_meanD*(1-0.40)
  
  # 6. Percentil 97.5%
  ts_series_qtl975 = array(dim=c(length(info_name),1))
  for (i in 1:length(info_name)) {
    ts_series_qtl975[i] = quantile(ts_seriesFull[,i],0.975)
  }
  limMax_qtl975= ts_series_qtl975*(1+0.3)
  limMin_qtl975= ts_series_qtl975*(1-0.3)
  
  # 7. Percentil 2.5%
  ts_series_qtl25= array(dim=c(length(info_name),1))
  for (i in 1:length(info_name)) {
    ts_series_qtl25[i] = quantile(ts_seriesFull[,i],0.025)
  }
  limMax_qtl25= ts_series_qtl25*(1+0.3)
  limMin_qtl25= ts_series_qtl25*(1-0.3)
  
  # 8. M�ximo valor
  ts_series_max= array(dim=c(length(info_name),1))
  for (i in 1:length(info_name)) {
    ts_series_max[i] = max(ts_seriesFull[,i])
  }
  limMax_max= ts_series_max*(1+0.5)
  limMin_max= ts_series_max*(1-0.5)
  
  # 9. M�nimo valor
  ts_series_min= array(dim=c(length(info_name),1))
  for (i in 1:length(info_name)) {
    ts_series_min[i] = min(ts_seriesFull[,i])
  }
  limMax_min= ts_series_min*(1+0.5)
  limMin_min= ts_series_min*(1-0.5)
  
  limites_f = list()
  limites_f[[1]]=limMax_medias
  limites_f[[2]]=limMin_medias
  limites_f[[3]]=limMax_desvE
  limites_f[[4]]=limMin_desvE
  limites_f[[5]]=limMax_mediana
  limites_f[[6]]=limMin_mediana
  limites_f[[7]]=limMax_CV
  limites_f[[8]]=limMin_CV
  limites_f[[9]]=limMax_meanD
  limites_f[[10]]=limMin_meanD
  limites_f[[11]]=limMax_qtl975
  limites_f[[12]]=limMin_qtl975
  limites_f[[13]]=limMax_qtl25
  limites_f[[14]]=limMin_qtl25
  limites_f[[15]]=limMax_max
  limites_f[[16]]=limMin_max
  limites_f[[17]]=limMax_min
  limites_f[[18]]=limMin_min
  
  return(limites_f)
}
