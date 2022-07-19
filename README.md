Voir texte en français plus bas.
# sunduration
Adds a new observation field containing sunshine duration to weewx: [sunshine_time]

This weewx extension was modified from https://github.com/brewster76/util-archer/blob/master/user/radiationhours.py  by applying a formula derived from the formula developed by MeteoFrance to estimate sunshine duration from Davis sensors. (https://forums.infoclimat.fr/f/topic/17151-calcul-duree-ensoleillement/?do=findComment&comment=1216053).  The idea is to determine for each LOOP data a  threshold value that is calculated depending on the date, time and geographic location (latitude and longitude) of the sensor. If the measured solar radiation is higher than the calculated threshold, the sunshine duration for this measurement will be equal to the time interval between the last LOOP and the current LOOP.  The final archive record contain( in minutes) the sum of each LOOP value within the archive period.
At the start of weewx, missing archive records imported from the datalogger have no loop data, and the first regular archive record has only partial loop data, so for these records if the measured solar radiation is higher than the threshold, the sunsine duration for this redcord is equal to the archive interval.

## Installation
  1. Save this file to your user customisations directory (which is often /usr/share/weewx/user)
  2. Enable this service in weewx.conf by adding user.sunduration.SunshineDuration to the process_services list.
  ```python
        [Engine]
            [[Services]]
                # This section specifies the services that should be run. They are
                # grouped by type, and the order of services within each group
                # determines the order in which the services will be run.
                prep_services = weewx.engine.StdTimeSynch
                process_services = user.sunduration.SunshineDuration, weewx.engine.StdConvert, weewx.engine.StdCalibrate, weewx.engine.StdQC, weewx.wxservices.StdWXCalculate
   ```
   3. Add [sunshine_time] to the database schema so tables include this new observation field.
       In weewx.conf, change the wx_binding schema from schemas.wview.schema to user.sunduration.schema_with_sunshine_time:
       ### with sqlite database :
       ```python
        [DataBindings]
            [[wx_binding]]
                # The database must match one of the sections in [Databases].
                # This is likely to be the only option you would want to change.
                database = archive_sqlite 
                # The name of the table within the database
                table_name = archive
                # The manager handles aggregation of data for historical summaries
                manager = weewx.wxmanager.WXDaySummaryManager
                # The schema defines the structure of the database.
                # It is *only* used when the database is created.
                #schema = schemas.wview.schema
                schema = user.sunduration.schema_with_sunshine_time
         ```
       ### with mysql database :
       ```python
           [DataBindings]
               [[wx_binding]]
                   # The database must match one of the sections in [Databases].
                   # This is likely to be the only option you would want to change.
                   database = archive_mysql 
                   # The name of the table within the database
                   table_name = archive
                   # The manager handles aggregation of data for historical summaries
                   manager = weewx.wxmanager.WXDaySummaryManager
                   # The schema defines the structure of the database.
                   # It is *only* used when the database is created.
                   #schema = schemas.wview.schema
                   schema = user.sunduration.schema_with_sunshine_time
          ```
   4. Shutdown Weewx and update your database to bring in the new field. (Weewx v4.5.0 or newer)
       ```python
       wee_database --add-column=sunshine_time
       ```
  
   5. Tell Weewx about the units for this new type
        Add this to user/extensions.py:
        ```python
         #
         # Units for sunshine_time calculated field
         #
         import weewx.units
         weewx.units.obs_group_dict['sunshine_time'] = 'group_interval'
         ```
   7. Use [sunshine_time] in your graphs and html template tags.
   
   Lots more detail on this process can be found here:http://www.weewx.com/docs/customizing.htm#archive_database
   
# sunduration
Ajoute à Weewx un nouveau paramètre contenant la durée d'ensoleillement: [sunshine_time]

Cette extensin weewx a été écrite d'après  https://github.com/brewster76/util-archer/blob/master/user/radiationhours.py  en supprimant un seuil fixe par l'application d'une formule dérivée de celle développée par Météo France pour estimer la durée d'ensoleillement à partir des mesures du capteur de radiation solaire Davis. (https://forums.infoclimat.fr/f/topic/17151-calcul-duree-ensoleillement/?do=findComment&comment=1216053).  L'idée est de calculer pour chaque paquet LOOP (chaque 2 secondes pour une Davis VP2)  une valeur seuil qui est calculée d'après la date, l'heure et le lieu (latitude et longitude) où est positionné le capteur. Si la radiation solaire mesurée est plus haute que le seuil d'ensoleillement calculé, la durée d'ensoleillement pour cette mesure sera égale à l'intervalle de temps entre le paquet LOOP précedent et le packet LOOP actuel. Si la valeur est en dessous du seuil, la durée d'ensoleillement pour ce paquet sera 0.
La valeur finale de la durée d'ensoleillement (en minutes) pour chaque enregistrement d'archive est la somme des données de chaque paquet LOOP emis durant la période d'archivage.
Au démarrage de weewx, des enregistrement d'archives manquants sont éventuellement importés depuis le datalogger et n'ont pas de données LOOP. d'autre part, les données LOOP disponibles après le démarrage de weewx ne couvrent qu'une partie de la période d'archivage en cours.  Pour ces enregistrements,  si la radiation solaire est plus haute que le seuil, la durée d'ensoleillement est égale à la période d'archivage.

## Installation
  1. Copier ce fichier dans le dossier "utilisateur" de weewx (le plus souvent  /usr/share/weewx/user  ou /home/weewx/bin/user)
  2. Activer ce service dans  weewx.conf en ajoutant user.sunduration.SunshineDuration dans la liste process_services:
  ```python
        [Engine]
            [[Services]]
                # This section specifies the services that should be run. They are
                # grouped by type, and the order of services within each group
                # determines the order in which the services will be run.
                prep_services = weewx.engine.StdTimeSynch
                process_services = user.sunduration.SunshineDuration, weewx.engine.StdConvert, weewx.engine.StdCalibrate, weewx.engine.StdQC, weewx.wxservices.StdWXCalculate
   ```
   3. Ajouter [sunshine_time] au schéma de la base de donnee .
       Dans weewx.conf, et dans wx-binding changer le schéma : schema= user.sunduration.schema_with_sunshine_time:
       ### avec sqlite :
       ```python
        [DataBindings]
            [[wx_binding]]
                # The database must match one of the sections in [Databases].
                # This is likely to be the only option you would want to change.
                database = archive_sqlite 
                # The name of the table within the database
                table_name = archive
                # The manager handles aggregation of data for historical summaries
                manager = weewx.wxmanager.WXDaySummaryManager
                # The schema defines the structure of the database.
                # It is *only* used when the database is created.
                #schema = schemas.wview.schema
                schema = user.sunduration.schema_with_sunshine_time
         ```
       ### avec mysql :
          ```python
           [DataBindings]
               [[wx_binding]]
                   # The database must match one of the sections in [Databases].
                   # This is likely to be the only option you would want to change.
                   database = archive_mysql 
                   # The name of the table within the database
                   table_name = archive
                   # The manager handles aggregation of data for historical summaries
                   manager = weewx.wxmanager.WXDaySummaryManager
                   # The schema defines the structure of the database.
                   # It is *only* used when the database is created.
                   #schema = schemas.wview.schema
                   schema = user.sunduration.schema_with_sunshine_time
          ```
   4.  Stopper Weewx  et mettre a jour la base de donnee avec le nouveau champ "sunshine_time (Weewx V. 4.5.0 ou plus récent)
       ```python
       wee_database --add-column=sunshine_time
       ```
       et confirmer la création du nouveau champ en pressant "Y"
       
       
   5. Configurer dans weewx l'unité utilisée pour ce nouveau champ.
      Ajouter à la fin de /usr/share/weewx/user/extensions.py ( ou /home/weewx/bin/user/extensions.py selon l'installation utilisée)
        ```python
         #
         # Units for sunshine_time calculated field
         #
         import weewx.units
         weewx.units.obs_group_dict['sunshine_time'] = 'group_interval'
         ```
   7. Utiliser le tag [sunshine_time] pour vos graphiques ou templates.
   
   Pour plus de détails sur l'ajout d'un nouveau paramètre, voir::
   http://www.weewx.com/docs/customizing.htm#archive_database
