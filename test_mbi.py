import pytest
import app

def test_get():
    r = app.generate()
    assert len(r) == 11
    assert app.verify(r) == True

def test_verify():
    r = app.verify("1EG4TE5MK73")
    assert r == True