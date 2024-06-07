Voir texte en français plus bas.
# sunduration
Adds a new observation field containing sunshine duration to weewx: [sunshine_time]. This observation is calculated from the measured solar radiation of Davis Vantage Pro weather stations.

This weewx extension was modified from https://github.com/brewster76/util-archer/blob/master/user/radiationhours.py  by applying a formula derived from the formula developed by MeteoFrance to estimate sunshine duration from measured solar radiation by Davis sensors. (https://forums.infoclimat.fr/f/topic/17151-calcul-duree-ensoleillement/?do=findComment&comment=1216053). Original publications: [https://library.wmo.int/viewer/68695/?offset=#page=344&viewer=picture&o=bookmark&n=0&q=)](https://library.wmo.int/viewer/68695/?offset=#page=344&viewer=picture&o=bookmark&n=0&q=))  and [http://meteo-sciez.fr/O1_07_Vuerich_Sunshine_Duration.pdf](http://meteo-sciez.fr/O1_07_Vuerich_Sunshine_Duration.pdf) 
This extension determine for each LOOP data a threshold value that is calculated depending on the date, time and geographic location (latitude and longitude) of the sensor. If the measured solar radiation is higher than the calculated threshold, the sunshine duration for this measurement will be equal to the time interval between the last LOOP and the current LOOP.  The final archive record contain( in minutes) the sum of each LOOP value within the archive period.
When weewx is started, missing archive records imported from the datalogger have no loop data, and the first regular archive record has only partial loop data, so for these records if the measured solar radiation is higher than the threshold, the sunsine duration for this record is equal to the archive interval.

## Coefficients
By default, the coefficients of the formula used to calculate the radiation thresold are the one validated for a latitude of 44° in the south of France.
If, for your location and your weather station, the threshold is too low or too high, you can adjust globallty the value of the parameter **global_coeff**.

For instance, a value of **global_coeff = 1.05** will globally increase the thresholf value by 5%
A value of **global_coeff = 0.95** will globally decrease the threshold value by 5%.


The **B_coeff** can be changed if you observe that the threshold needs to be adjusted only for winter or summer period.

For instance, a value of **B_coeff = 0.08**  will increase the threshold value by about 3% in winter, and will decrease the threshold value by about 3% in summer.
A value of **B_coeff = 0.04** will decrease the threshold value by about 3% in winter, and will increase the threshold value by about 3% in summer.

A variability of **global_coeff** and **B_coeff** has been observed in relation to latitude : **B_coeff** tends toward negative values for the southern hemisphere, while **global_coeff** decreases with latitude
## Installation
  1. Save the file "sunduration.py" to your user customisations directory (which is often /usr/share/weewx/user or /home/weewx/bin/user)
  2. Enable this service in weewx.conf by adding user.sunduration.SunshineDuration to the process_services list.
```python
        [Engine]
            [[Services]]
                # This section specifies the services that should be run. They are
                # grouped by type, and the order of services within each group
                # determines the order in which the services will be run.
                prep_services = weewx.engine.StdTimeSynch
                process_services =  weewx.engine.StdConvert, weewx.engine.StdCalibrate, weewx.engine.StdQC, weewx.wxservices.StdWXCalculate, user.sunduration.SunshineDuration,
 ```
   3. Add the following lines to weewx.conf :
```python
       [Sunduration]
            global_coeff = 1.0
            B_coeff = 0.06
            
```
       
4. Shutdown Weewx and update your database to bring in the new field. 

Weewx v4.5.0  to V4.10.2
```python
       wee_database --add-column=sunshine_time
```

Weewx V. 5.0 or newer :
```python
       weectl database add-column sunshine_time
```
  
   5. Use [sunshine_time] in your graphs and html template tags.
   
   More detail on this process can be found here:http://www.weewx.com/docs/customizing.htm#archive_database
   
# sunduration
Ajoute à Weewx un nouveau paramètre contenant la durée d'ensoleillement: [sunshine_time]. Ce paramètre est calculé d'après les mesures de la radiation solaire d'une station météo Davis Vantage Pro.

Cette extensin weewx a été écrite d'après  https://github.com/brewster76/util-archer/blob/master/user/radiationhours.py  en supprimant un seuil fixe par l'application d'une formule dérivée de celle développée par Météo France pour estimer la durée d'ensoleillement à partir des mesures du capteur de radiation solaire Davis. (https://forums.infoclimat.fr/f/topic/17151-calcul-duree-ensoleillement/?do=findComment&comment=1216053) et publications originales:  [https://library.wmo.int/viewer/68695/?offset=#page=344&viewer=picture&o=bookmark&n=0&q=)](https://library.wmo.int/viewer/68695/?offset=#page=344&viewer=picture&o=bookmark&n=0&q=))  et [http://meteo-sciez.fr/O1_07_Vuerich_Sunshine_Duration.pdf](http://meteo-sciez.fr/O1_07_Vuerich_Sunshine_Duration.pdf) . 
L'extension calcule pour chaque paquet LOOP (environ chaque 2 secondes pour une Davis VP2)  une valeur seuil qui est calculée d'après la date, l'heure et le lieu (latitude et longitude) où est positionné le capteur. Si la radiation solaire mesurée est plus haute que le seuil d'ensoleillement calculé, la durée d'ensoleillement pour cette mesure sera égale à l'intervalle de temps entre le paquet LOOP précedent et le packet LOOP actuel. Si la valeur est en dessous du seuil, la durée d'ensoleillement pour ce paquet sera 0.
La valeur finale de la durée d'ensoleillement (en minutes) pour chaque enregistrement d'archive est la somme des données de chaque paquet LOOP emis durant la période d'archivage.
Au démarrage de weewx, des enregistrement d'archives manquants sont éventuellement importés depuis le datalogger et n'ont pas de données LOOP. d'autre part, les données LOOP disponibles après le démarrage de weewx ne couvrent qu'une partie de la période d'archivage en cours.  Pour ces enregistrements,  si la radiation solaire est plus haute que le seuil, la durée d'ensoleillement est égale à la période d'archivage.

## Installation
  1. Copier ce fichier "sunduration.py" dans le dossier "utilisateur" de weewx (le plus souvent  /usr/share/weewx/user  ou /home/weewx/bin/user)
  2. Activer ce service dans  weewx.conf en ajoutant user.sunduration.SunshineDuration dans la liste process_services:
```python
        [Engine]
            [[Services]]
                # This section specifies the services that should be run. They are
                # grouped by type, and the order of services within each group
                # determines the order in which the services will be run.
                prep_services = weewx.engine.StdTimeSynch
                process_services = weewx.engine.StdConvert, weewx.engine.StdCalibrate, weewx.engine.StdQC, weewx.wxservices.StdWXCalculate, user.sunduration.SunshineDuration
```
 3. Ajouter les lignes suivantes dans weewx.conf :
```python
       [Sunduration]
            global_coeff = 1.0
            B_coeff = 0.06
            
```
       
4. Stopper Weewx  et mettre a jour la base de donnee avec le nouveau champ "sunshine_time

Weewx V. 4.5.0 to 4.10.2 :

```python
       wee_database --add-column=sunshine_time
```

Weewx V. 5.0 ou plus récent :
```python
       weectl database add-column sunshine_time
```
       
       
   5. Utiliser le tag [sunshine_time] pour vos graphiques ou templates.
   
   Pour plus de détails sur l'ajout d'un nouveau paramètre, voir::
   http://www.weewx.com/docs/customizing.htm#archive_database
