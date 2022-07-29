# YOLOv5DoaFeatureGeneration

## FeatureGen
python3 featureGen.py count --clear --start (int) --cores (int) 
  count: Anzahl an Daten, die pro Core generiert werden sollen.
  clear: Löscht bisher generiete Daten bevor neue generiert werden.
  start: Gibt die Start- Id bzw. Namen der zu generierenden Daten an. Hilfreich, wenn man Daten im Nachhinein generieren möchte (default:0)
  cores: Anzahl der Cores, die zum erstellen der Daten verwendet werden sollen. (default: Alle Cores)
  
 ## SimplifyClasses
 python3 SimplifyClasses.py count
  count: Anzahl der Klassen, die nach dem Vereinfachen übrig bleiben sollen.
