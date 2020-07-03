from evalPredictions import testFitAlt
import pandas as pd

bigboy = pd.read_csv('./csv_Data/test_predictionsAlt.csv', encoding = "ISO-8859-1")

testFitAlt(bigboy,5,5,100)
