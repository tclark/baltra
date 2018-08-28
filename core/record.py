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
        possible_conflict = self.get_amendment(amendment.key, amendment.valid_from())
        if possible_conflict and possible_conflict.valid_from() == amendment.valid_from():
            raise ValueError("Amendment valid time conflicts with a prior amendment.")
        self.amendments.append(amendment)

    def get_amendment(self, key, vtime):
        all_values = [a for a in self.amendments if a.key == key]
        trimmed_values = [a for a in all_values if a.valid_from() <= vtime]
        trimmed_values.sort()
        val_as_list = trimmed_values[-1:]
        if val_as_list:
            return val_as_list[0]
        return None



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


    def valid_from(self):
        return self.meta['vtime']

    def __lt__(self, other):
        return self.valid_from() < other.valid_from()

    def __gt__(self, other):
        return other < self
