from sort_table import app


def test1(client):
    """
    Test if digit is prior to zero
    input: [[" 1", "9"]]
    result: [["9", " 1"]]
    """
    req = client.post('/sort-table',
                      json={"table": [" 1\t9"]})
    resp = req.get_json()
    expected = {"table": ["9\t 1"]}
    assert resp['table'] == expected['table']


def test2(client):
    """
    Test empty row
    input: [[""]]
    result: [[""]]
    """
    req = client.post('/sort-table',
                      json={"table": [""]})
    resp = req.get_json()
    expected = {"table": [""]}
    assert resp['table'] == expected['table']


def test3(client):
    """
    Complex test
    input: [[""]]
    result: [[""]]
    """
    req = client.post('/sort-table',
                      json={"table": [
                          " 1 \tabc\t zz zz\t9 \ta1\ta ",
                          ""]})
    resp = req.get_json()
    expected = {"table": [
        "9 \t 1 \t zz zz\ta1\ta \tabc",
        ""]}
    assert resp['table'] == expected['table']


if __name__ == '__main__':
    with app.test_client() as client:
        test1(client)
        test2(client)
        test3(client)
