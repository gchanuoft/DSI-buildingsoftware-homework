from pytest import raises
import pandas as pd
import sys

def test_pdAllStrToOneCol(monkeypatch):
    monkeypatch.setattr('sys.argv', [sys.argv[0], 'user_config.yml', 'outputPNG'])
    from building_software_homework3 import pdAllStrToOneCol
    testDataFrame =  pd.DataFrame({'A': [1, 2, 3, 4],
                                   'B': [5, 6, 7, 8],
                                   'C': ['Str1', 'Str2', 'Str3', 'Str4']})
    assert len(pdAllStrToOneCol(testDataFrame).columns) == 1
    
def test_pdAllStrToOneCol_errors(monkeypatch):
    monkeypatch.setattr('sys.argv', [sys.argv[0], 'user_config.yml', 'outputPNG'])
    from building_software_homework3 import pdAllStrToOneCol
    NotADataFrame = 0
    with raises(TypeError):
        pdAllStrToOneCol(NotADataFrame)

    emptyDataFrame =  pd.DataFrame()
    with raises(ValueError):
        pdAllStrToOneCol(emptyDataFrame)

    