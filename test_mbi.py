import pytest
import app

def test_get():
    r = app.generate()
    assert r == "1EG4TE5MK73"

def test_verify():
    r = app.verify("1EG4TE5MK73")
    assert r == True