from core.record import Amendment
from datetime import datetime

def test_constructor():
    vt = datetime.fromisoformat('2018-08-01 12:25:00')
    a = Amendment('testkey', 'testvalue', 'testrecord', vt)
    assert(isinstance(a, Amendment))
    assert(a.key == 'testkey')
    assert(a.value == 'testvalue')
    assert(a.record_id == 'testrecord')
    assert(a.meta['vtime'] == vt)

def test_valid_from():
    vt = datetime.fromisoformat('2018-08-01 12:25:00')
    a = Amendment('testkey', 'testvalue', 'testrecord', vt)
    assert(a.valid_from() == vt)

def test_less_than():
    earlier_time = datetime.fromisoformat('2018-08-01 00:00:00')
    later_time = datetime.fromisoformat('2018-08-02 00:00:00')
    earlier = Amendment('testkey', 'earlier', 'testrecord', earlier_time)
    later = Amendment('testkey', 'later', 'testrecord', later_time)
    assert(earlier < later)
    assert(not (later < earlier))

def test_greater_than():
    earlier_time = datetime.fromisoformat('2018-08-01 00:00:00')
    later_time = datetime.fromisoformat('2018-08-02 00:00:00')
    earlier = Amendment('testkey', 'earlier', 'testrecord', earlier_time)
    later = Amendment('testkey', 'later', 'testrecord', later_time)
    assert(later > earlier) 
    assert(not (earlier > later))
