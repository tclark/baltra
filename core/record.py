from uuid import uuid4
from datetime import datetime


class Record:
    def __init__(self, vtime, record_type=None):
        self.id = uuid4()
        self.record_type = record_type
        self.amendments = []
        opening = Amendment('open', True, self.id, vtime)
        self.amend(opening)


    def close(self, vtime):
        closing = Amendment('open', False, self.id, vtime)
        self.amend(closing)
        

    def amend(self, amendment):
        self.amendments.append(amendment)

class Amendment:
    
    def __init__(self, key, value, record_id, vtime):
        self.id = uuid4()
        self.record_id = record_id
        self.key = key
        self.value = value
        self.meta = {
                'vtime' : vtime,
                'ttime' : datetime.utcnow()
                }

