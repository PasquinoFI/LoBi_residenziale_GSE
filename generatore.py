"""
LoBi_standard_GSE


Utilizzando 12 bollette dell'energia elettrica è possibile generare curve di carico orarie (8760 valori in un file .csv)

Vengono utilizzati profili standard messi a disposizione dal GSE in allegato alle "Regole tecniche per l'accesso al servizio di valorizzazione e incentivazione dell'energia elettrica condivisa" del 04/04/2022
https://www.gse.it/documenti_site/Documenti%20GSE/Servizi%20per%20te/AUTOCONSUMO/Gruppi%20di%20autoconsumatori%20e%20comunita%20di%20energia%20rinnovabile/Regole%20e%20procedure/Autoconsumatori.pdf
"""

### Leggi qua sotto e inserisci gli input richiesti

# Conosci i consumi di ogni mese divisi nelle 3 fasce orarie? Inseriscili nel file "bollette_tri.xlsx" e seleziona tipologia_bolletta='F'
# Se conosci solamente i consumi totali di ogni mese (ad esempio perchè il contratto è monoorario) inseriscili in "bolletta_mono.xlsx" e seleziona tipologia_bolletta='M'

tipologia_bolletta = 'F' # M/F = Monooraria/Fasce
numero_utenze = 1 # Se selezioni un numero X intero maggiore di uno viene generato un profilo aggregato di X utenze (uguali perchè simulate partendo dalla stessa bolletta)
name = 'profilo esempio' # scegli un nome per la serie da generare

# Adesso puoi fare Run File (F5), la serie.csv verrà generata nella cartella profili_generati/name.csv
# Se stai generando la serie per usarla su MESSpy copiala e incollala in input/loads

import core
core.genera_serie(tipologia_bolletta, numero_utenze, name)


