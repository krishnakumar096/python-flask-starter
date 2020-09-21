import re
from datetime import datetime
import pytz
from app.main import db
from app.config.logger import log


class Util:
    @staticmethod
    def current_date_time():
        tz = pytz.timezone("Asia/Kolkata")
        return datetime.now(tz)

    @staticmethod
    def commit():
        try:
            db.session.commit()
            log.info('successfully data committed')
            return True
        except Exception as e:
            log.error(e.args)
            return False
