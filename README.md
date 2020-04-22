# sunduration
Adds a new observation field containing sunshine duration to weewx: [sunshine_time]

This weewx extension was modified from https://github.com/brewster76/util-archer/blob/master/user/radiationhours.py  by applying a formula developed by MeteoFrance to estimate sunshine duration from Davis sensors. (https://forums.infoclimat.fr/f/topic/17151-calcul-duree-ensoleillement/?do=findComment&comment=1216053).  The idea is to determine at each measurements a  threshold value that is calculated depending on the date, time and geographic location (latitude and longitude) of the sensor. If the measured solar radiation is higher than the calculated threshold, the sunshine duration for this measurement will be equal to the archive interval, otherwise it will be 0.

