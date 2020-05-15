import syslog
from math import sin,cos,pi,asin
from datetime import datetime
import time
import weewx
from weewx.wxengine import StdService
import schemas.wview

class SunshineDuration(StdService):
    def __init__(self, engine, config_dict):
        # Pass the initialization information on to my superclass:
        super(SunshineDuration, self).__init__(engine, config_dict)

        # Start intercepting events:
        self.bind(weewx.NEW_ARCHIVE_RECORD, self.newArchiveRecord)

    def newArchiveRecord(self, event):
        """Gets called on a new archive record event."""
        seuil = 0
        coeff = 0.9
        tempe = event.record.get('outTemp', 25.0)
        radiation = event.record.get('radiation')
        event.record['sunshine_time'] = 0.0
        if radiation is not None:
            utcdate = datetime.utcfromtimestamp(event.record.get('dateTime'))
            dayofyear = int(time.strftime("%j",time.gmtime(event.record.get('dateTime'))))
            theta = 360 * dayofyear / 365
            equatemps = 0.0172 + 0.4281 * cos((pi / 180) * theta) - 7.3515 * sin(
                (pi / 180) * theta) - 3.3495 * cos(2 * (pi / 180) * theta) - 9.3619 * sin(
                2 * (pi / 180) * theta)

            latitude= float(self.config_dict["Station"]["latitude"])
            longitude = float(self.config_dict["Station"]["longitude"])
            corrtemps = longitude * 4
            declinaison = asin(0.006918 - 0.399912 * cos((pi / 180) * theta) + 0.070257 * sin(
                (pi / 180) * theta) - 0.006758 * cos(2 * (pi / 180) * theta) + 0.000908 * sin(
                2 * (pi / 180) * theta)) * (180 / pi)

            minutesjour = utcdate.hour*60 + utcdate.minute
            tempsolaire = (minutesjour + corrtemps + equatemps) / 60
            angle_horaire = (tempsolaire - 12) * 15
            hauteur_soleil = asin(sin((pi / 180) * latitude) * sin((pi / 180) * declinaison) + cos(
                (pi / 180) * latitude) * cos((pi / 180) * declinaison) * cos((pi / 180) * angle_horaire)) * (180 / pi)
            if hauteur_soleil > 3:
                seuil = (0.73 + 0.06 * cos((pi / 180) * 360 * dayofyear / 365)) *1080 * pow((sin(pi / 180) * hauteur_soleil), 1.25) * coeff
                mesure = (((tempe - 25.0) * (-0.0012) * radiation) + radiation)
                if mesure > seuil:
                    event.record['sunshine_time'] = event.record['interval']

        syslog.syslog(syslog.LOG_DEBUG, "Calculated sunshine_time = %f, based on radiation = %f, and threshold = %f" %
                      (event.record['sunshine_time'], radiation, seuil))


schema_with_sunshine_time = schemas.wview.schema + [('sunshine_time', 'REAL')]
