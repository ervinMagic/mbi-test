import app

def test_get():
    r = app.generate()
    assert len(r) == 11


def test_verify():
    with app.app.test_client() as c:
        rv = c.post('/verify', json={
            'mbi': '5Y20MA2KW16'
        })
        assert rv.get_json()['valid'] == True

        rv = c.post('/verify', json={
            'mbi': '5Y20MA2KW6'
        })
        assert rv.get_json()['valid'] == False

        rv = c.post('/verify', json={
            'mbi': '5Y20mA2Kw16'
        })
        assert rv.get_json()['valid'] == True

        rv = c.post('/verify', json={
            'mbi': '5Y20-mA2-Kw16'
        })
        assert rv.get_json()['valid'] == True

def test_generate_then_verify():
    with app.app.test_client() as c:
        rv = c.get('/generate')

        rv = c.post('/verify', json={
            'mbi': str(rv.get_data().decode('UTF-8'))
        })
        assert rv.get_json()['valid'] == True