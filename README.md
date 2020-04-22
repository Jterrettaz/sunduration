Voir texte en français plus bas.
# sunduration
Adds a new observation field containing sunshine duration to weewx: [sunshine_time]

This weewx extension was modified from https://github.com/brewster76/util-archer/blob/master/user/radiationhours.py  by applying a formula developed by MeteoFrance to estimate sunshine duration from Davis sensors. (https://forums.infoclimat.fr/f/topic/17151-calcul-duree-ensoleillement/?do=findComment&comment=1216053).  The idea is to determine at each measurements a  threshold value that is calculated depending on the date, time and geographic location (latitude and longitude) of the sensor. If the measured solar radiation is higher than the calculated threshold, the sunshine duration for this measurement will be equal to the archive interval, otherwise it will be 0.

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
   4. Shutdown Weewx and update your database to bring in the new field.
       ```python
       wee_database weewx.conf --reconfigure
       ```
      This will create a new database (nominally, weewx.sdb_new if you are using SQLite, weewx_new if you are using MySQL) using the new schema and populate it with data from the old database.
   5. Shuffle the databases. Now arrange things so WeeWX can find the new database.
   **Make sure you know what you're doing at this point, you can potentially corrupt/lose your archive data.**
   You can either shuffle the databases around so the new database has the same name as the old database, or edit weewx.conf to use the new database name. To do the former:

For SQLite:
  ```
    cd SQLITE_ROOT
    mv weewx.sdb_new weewx.sdb
  ```

For Mysql: 
  ```
    mysql -u <username> --password=<mypassword>
    mysql> DROP DATABASE weewx;                             # Delete the old database
    mysql> CREATE DATABASE weewx;                           # Create a new one with the same name
    mysql> RENAME TABLE weewx_new.archive TO weewx.archive; # Rename to the nominal name
  ```
  
   6. Tell Weewx about the units for this new type
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

Cette extensin weewx a été écrite d'après  https://github.com/brewster76/util-archer/blob/master/user/radiationhours.py  en supprimant un seuil fixe par l'application d'une formule développée par Météo France pour estimer la durée d'ensoleillement à partir des mesures du capteur de radiation solaire Davis. (https://forums.infoclimat.fr/f/topic/17151-calcul-duree-ensoleillement/?do=findComment&comment=1216053).  L'idée est de calculer pour chaque enregistrement une valeur seuil qui est calculée d'après la date, l'heure et le lieu (latitude et longitude) où est positionné le capteur. Si la radiation solaire mesurée est plus haute que le seuil d'ensoleillement calculé, la durée d'ensoleillement pour cet enregistrement sera égale au pas de mesure. SI la valeur est en dessous du seuil, la durée d'ensoleillement pour cet enreggistrement sera 0.

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
   4.  Stopper Weewx  et mettre a jour la base de donnee avec le nouveau champ "sunshine_time".
       ```python
       wee_database weewx.conf --reconfigure
       ```
       Cette commande va créer une nouvelle base de donnée (**weewx.sdb_new** si vous utilisez SQLite, **weewx_new** si vous utilisez MySQL) en utilisant le nouveau schéma et va transférer les données dans cette nouvelle base de donnée.
       
   5. Configurer Weewx pour la nouvelle base de donnée.
   **Soyez sûrs de ce que vous faites à ce point, car vous pouvez potentiellement corompre ou perdre vos données d'archives. Il vaut mieux faire une sauvegarde de la base de donnée avant..**
   
   Vous pouvez le faire soit en renommant la nouvelle base de donnée, ou en modifiant dans weewx.conf le nom de la base de données à utiliser. Pour renommer la nouvelle base de données:

Pour SQLite:
  ```
    cd SQLITE_ROOT
    mv weewx.sdb_new weewx.sdb
  ```

Pour Mysql: 
  ```
    mysql -u <username> --password=<mypassword>
    mysql> DROP DATABASE weewx;                             # Delete the old database
    mysql> CREATE DATABASE weewx;                           # Create a new one with the same name
    mysql> RENAME TABLE weewx_new.archive TO weewx.archive; # Rename to the nominal name
  ```
       
   6. Configurer dans weewx l'unité utilisée pour ce nouveau champ.
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
