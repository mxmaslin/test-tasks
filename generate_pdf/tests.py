from generate_pdfs import build_diploma_number

# i
# num_diploma_digits
# last_diploma_numer

if __name__ == '__main__':
    assert build_diploma_number(1, 2, 10) == '01'
    assert build_diploma_number(9, 2, 10) == '09'
    assert build_diploma_number(10, 2, 10) == '10'

    assert build_diploma_number(1, 3, 100) == '001'
    assert build_diploma_number(9, 3, 100) == '009'
    assert build_diploma_number(90, 3, 100) == '090'
    assert build_diploma_number(100, 3, 100) == '100'
