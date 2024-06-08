# sunduration
Adds a new observation field containing sunshine duration to weewx: [sunshine_time]. This observation is calculated from the measured solar radiation by pyranometers, such as the Davis Vantage Pro weather stations.

This weewx extension was modified from https://github.com/brewster76/util-archer/blob/master/user/radiationhours.py  by applying a formula derived from the formula developed by MeteoFrance to estimate sunshine duration from measured solar radiation by pyranometers. (https://forums.infoclimat.fr/f/topic/17151-calcul-duree-ensoleillement/?do=findComment&comment=1216053). Original publications: [https://library.wmo.int/viewer/68695/?offset=#page=344&viewer=picture&o=bookmark&n=0&q=)](https://library.wmo.int/viewer/68695/?offset=#page=344&viewer=picture&o=bookmark&n=0&q=))  and [http://meteo-sciez.fr/O1_07_Vuerich_Sunshine_Duration.pdf](http://meteo-sciez.fr/O1_07_Vuerich_Sunshine_Duration.pdf) 
This extension determine for each LOOP data a threshold value that is calculated depending on the date, time and geographic location (latitude and longitude) of the sensor. If the measured solar radiation is higher than the calculated threshold, the sunshine duration for this measurement will be equal to the time interval between the last LOOP and the current LOOP.  The final archive record contain( in minutes) the sum of each LOOP value within the archive period.
When weewx is started, missing archive records imported from the datalogger have no loop data, and the first regular archive record has only partial loop data, so for these records if the measured solar radiation is higher than the threshold, the sunsine duration for this record is equal to the archive interval.

## Coefficients
By default, the coefficients of the formula used to calculate the radiation threshold are the one validated for a latitude of 44°N in the south of France using a pyranometer.
If, for your location and your weather station ( **and particularly if you are using a luxmeter with a reduced spectral range compared to pyranometers**) the threshold is too low or too high, you will have to adjust by trial and error the value of the parameter **global_coeff** until at the best the extension  will reports sunshine when shadows are visible, and no sunshine when there  is no shadows.

For instance, a value of **global_coeff = 1.05** will globally increase the threshold value by 5%
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
   

