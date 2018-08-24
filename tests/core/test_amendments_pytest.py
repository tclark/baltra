from core.record import Amendment
from datetime import datetime

def test_constructor():
    vt = datetime.utcnow()
    a = Amendment('testkey', 'testvalue', 'testrecord', vt)
    assert(isinstance(a, Amendment))
    assert(a.key == 'testkey')
    assert(a.value == 'testvalue')
    assert(a.record_id == 'testrecord')
    assert(a.meta['vtime'] == vt)
    
