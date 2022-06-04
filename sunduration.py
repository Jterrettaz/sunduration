import syslog
from math import sin, cos, pi, asin
from datetime import datetime
import time
import weewx
from weewx.wxengine import StdService
import schemas.wview

try:
    # Test for new-style weewx logging by trying to import weeutil.logger
    import weeutil.logger
    import logging

    log = logging.getLogger(__name__)


    def logdbg(msg):
        log.debug(msg)


    def loginf(msg):
        log.info(msg)


    def logerr(msg):
        log.error(msg)

except ImportError:
    # Old-style weewx logging
    import syslog


    def logmsg(level, msg):
        syslog.syslog(level, 'meteotemplate: %s' % msg)


    def logdbg(msg):
        logmsg(syslog.LOG_DEBUG, msg)


    def loginf(msg):
        logmsg(syslog.LOG_INFO, msg)


    def logerr(msg):
        logmsg(syslog.LOG_ERR, msg)




class SunshineDuration(StdService):
    def __init__(self, engine, config_dict):
        # Pass the initialization information on to my superclass:
        super(SunshineDuration, self).__init__(engine, config_dict)

        # Start intercepting events:
        self.bind(weewx.NEW_LOOP_PACKET, self.newLoopPacket)
        self.bind(weewx.NEW_ARCHIVE_RECORD, self.newArchiveRecord)
        self.lastdateTime = 0
        self.LoopDuration = 0
        self.sunshineSeconds = 0



    def newLoopPacket(self, event):
        """Gets called on a new archive record event."""
        seuil = 0
        coeff = 0.9
        radiation = event.packet.get('radiation')
        if radiation is not None:
            if self.lastdateTime == 0:
                self.lastdateTime = event.packet.get('dateTime')
            self.LoopDuration=event.packet.get('dateTime')-self.lastdateTime
            self.lastdateTime = event.packet.get('dateTime')
            utcdate = datetime.utcfromtimestamp(event.packet.get('dateTime'))
            
            dayofyear = int(time.strftime("%j", time.gmtime(event.packet.get('dateTime'))))
            theta = 360 * dayofyear / 365
            equatemps = 0.0172 + 0.4281 * cos((pi / 180) * theta) - 7.3515 * sin(
                (pi / 180) * theta) - 3.3495 * cos(2 * (pi / 180) * theta) - 9.3619 * sin(
                2 * (pi / 180) * theta)

            latitude = float(self.config_dict["Station"]["latitude"])
            longitude = float(self.config_dict["Station"]["longitude"])
            corrtemps = longitude * 4
            declinaison = asin(0.006918 - 0.399912 * cos((pi / 180) * theta) + 0.070257 * sin(
                (pi / 180) * theta) - 0.006758 * cos(2 * (pi / 180) * theta) + 0.000908 * sin(
                2 * (pi / 180) * theta)) * (180 / pi)

            minutesjour = utcdate.hour * 60 + utcdate.minute
            tempsolaire = (minutesjour + corrtemps + equatemps) / 60
            angle_horaire = (tempsolaire - 12) * 15
            hauteur_soleil = asin(sin((pi / 180) * latitude) * sin((pi / 180) * declinaison) + cos(
                (pi / 180) * latitude) * cos((pi / 180) * declinaison) * cos((pi / 180) * angle_horaire)) * (180 / pi)
            if hauteur_soleil > 3:
                seuil = (0.73 + 0.06 * cos((pi / 180) * 360 * dayofyear / 365)) * 1080 * pow(
                    (sin(pi / 180) * hauteur_soleil), 1.25) * coeff
                if radiation > seuil:
                    self.sunshineSeconds += self.LoopDuration

            logdbg("Calculated LOOP sunshine duration (seconds) = %f, based on radiation = %f, and threshold = %f" % (self.LoopDuration, radiation, seuil))


    def newArchiveRecord(self, event):
        event.record['sunshine_time'] = self.sunshineSeconds/60
        self.sunshineSeconds = 0
        loginf("Calculated sunshine duration (minutes) for archive period = %f" % (event.record['sunshine_time']))
        
    schema_with_sunshine_time = schemas.wview.schema + [('sunshine_time', 'REAL')]
