from core.record import Amendment, Record
from datetime import datetime
import pytest

def test_constructor():
    vt = datetime.fromisoformat('2018-01-01 00:00:00')
    tp = 'test_record_type'
    rcd = Record(vt, tp)
    assert(isinstance(rcd, Record))
    assert(rcd.record_type == tp)
    # there should be exactly one amendment - the opening
    assert(len(rcd.amendments) == 1)
    # and it should be the right ammendment
    a =  rcd.get_amendment('open', vt)
    assert(isinstance(a, Amendment))
    assert(a.record_id == rcd.id)
    assert(a.key == 'open')
    assert(a.value == True)
    assert(a.meta['vtime'] == vt)

def test_amend():
    vt = datetime.fromisoformat('2018-01-01 00:00:00')
    tp = 'test_record_type'
    rcd = Record(vt, tp)
    amendment_vt = datetime.fromisoformat('2018-01-02 00:00:00')
    a = Amendment('testkey', 'testval', rcd.id, amendment_vt)
    rcd.amend(a)
    assert(a in rcd.amendments)

def test_amendment_exception():    
    vt = datetime.fromisoformat('2018-01-01 00:00:00')
    tp = 'test_record_type'
    rcd = Record(vt, tp)
    amendment_vt = datetime.fromisoformat('2018-01-02 00:00:00')
    a1 = Amendment('testkey', 'testval', rcd.id, amendment_vt)
    a2 = Amendment('testkey', 'testval', rcd.id, amendment_vt)
    rcd.amend(a1)
    with pytest.raises(ValueError) as ex:
        rcd.amend(a2)
    assert('valid time conflicts' in str(ex.value))    

def test_superceed_amendment():    
    vt = datetime.fromisoformat('2018-01-01 00:00:00')
    tp = 'test_record_type'
    rcd = Record(vt, tp)
    amendment_vt = datetime.fromisoformat('2018-01-02 00:00:00')
    a1 = Amendment('testkey', 'testval', rcd.id, amendment_vt)
    a2 = Amendment('testkey', 'testval', rcd.id, amendment_vt)
    rcd.amend(a1)
    rcd.superceed(a1, a2)
    assert(rcd.get_amendment('testkey', amendment_vt) == a2)

def test_get_amendment():
    vt = datetime.fromisoformat('2018-01-01 00:00:00')
    tp = 'test_record_type'
    rcd = Record(vt, tp)
    amendment_vt1 = datetime.fromisoformat('2018-01-02 00:00:00')
    a1 = Amendment('testkey', 'testval', rcd.id, amendment_vt1)
    amendment_vt2 = datetime.fromisoformat('2018-01-05 00:00:00')
    a2 = Amendment('testkey', 'testval', rcd.id, amendment_vt2)
    rcd.amend(a1)
    rcd.amend(a2)
    assert(rcd.get_amendment('testkey', amendment_vt1) == a1)
    assert(rcd.get_amendment('testkey', amendment_vt2) == a2)

def test_get_amendment_by_id():    
    vt = datetime.fromisoformat('2018-01-01 00:00:00')
    tp = 'test_record_type'
    rcd = Record(vt, tp)
    amendment_vt = datetime.fromisoformat('2018-01-02 00:00:00')
    a1 = Amendment('testkey', 'testval', rcd.id, amendment_vt)
    rcd.amend(a1)
    a2 = rcd._get_amendment_by_id(a1.id)
    assert(a1 == a2)
    assert(rcd._get_amendment_by_id('nosuchid') is None)
    a3 = Amendment('testkey2', 'testval', rcd.id, amendment_vt)
    a3.id = a1.id
    rcd.amendments.add(a3)
    with pytest.raises(ValueError) as ex:
        a2 = rcd._get_amendment_by_id(a1.id)
    assert('multiple values' in str(ex.value))    
