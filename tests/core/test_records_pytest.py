from core.record import Amendment, Record
from datetime import datetime

def test_constructor():
    vt = datetime.utcnow()
    tp = 'test_record_type'
    rcd = Record(vt, tp)
    assert(isinstance(rcd, Record))
    assert(rcd.record_type == tp)
    # there should be exactly one amendment - the opening
    assert(len(rcd.amendments) == 1)
    # and it should be the right ammendment
    a = rcd.amendments[0]
    assert(isinstance(a, Amendment))
    assert(a.record_id == rcd.id)
    assert(a.key == 'open')
    assert(a.value == True)
    assert(a.meta['vtime'] == vt)

    
