import app

def test_get():
    r = app.generate()
    assert len(r) == 11


def test_verify():
    app.request = {'json': {'mbi': '5Y20MA2KW16'}}
    r = app.verify()
    assert r == True

def test_generate_then_verify():
    r = app.generate()
    app.request = {'json': {'mbi': r}}
    r = app.verify()
    assert r == True