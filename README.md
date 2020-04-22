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
       Make sure you know what you're doing at this point, you can potentially corrupt/lose your archive data.
       The weewx customization guide covers this in a lot more detail.
   5. Tell Weewx about the units for this new type
        Add this to user/extensions.py:
        ```python
         #
         # Units for sunshine_days calculated field
         #
         import weewx.units
         weewx.units.obs_group_dict['sunshine_time'] = 'group_interval'
         ```
   6. Use [sunshine_time] in your graphs and html template tags.
   
   Lots more detail on this process can be found here:
   http://www.weewx.com/docs/customizing.htm#Adding_a_new_observation_type
