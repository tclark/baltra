from datetime import datetime
from uuid import uuid4


class Record:

    def __init__(self, vtime, record_type=None):
        self.id_ = uuid4()
        self.record_type = record_type
        self.amendments = set()
        opening = Amendment('open', True, self.id_, vtime)
        self.amend(opening)

    def close(self, vtime):
        closing = Amendment('open', False, self.id_, vtime)
        self.amend(closing)

    def amend(self, amendment):
        possible_conflict = self.get_amendment(amendment.key,
                                               amendment.valid_from())
        if (possible_conflict
                and possible_conflict.valid_from() == amendment.valid_from()):
            raise ValueError("Valid time conflicts with a prior amendment.")
        self.amendments.add(amendment)

    def superceed(self, old, new):
        if old not in self.amendments:
            raise ValueError('Superceeded amendment not found')
        new.meta['superceeds'] = old.id_
        old.meta['superceeded_by'] = new.id_
        self.amendments.add(new)

    def get_amendment(self, key, vtime):
        all_values = [a for a in self.amendments if a.key == key]
        trimmed_values = [a for a in all_values if a.valid_from() <= vtime]
        trimmed_values.sort()
        val_as_list = trimmed_values[-1:]
        if val_as_list:
            amds = val_as_list[0]
            if 'superceeded_by' in amds.meta:
                return self._get_amendment_by_id(amds.meta['superceeded_by'])
            return amds
        return None

    def _get_amendment_by_id(self, requested_id):
        amds = [a for a in self.amendments if a.id_ == requested_id]
        if not amds:
            return None
        if len(amds) == 1:
            return amds[0]
        raise ValueError('Record._get_by_id would return multiple values')


class Amendment:

    def __init__(self, key, value, record_id, vtime):
        self.id_ = uuid4()
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
