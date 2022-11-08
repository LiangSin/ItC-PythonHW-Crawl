import pandas as pd

file = pd.read_csv('output.csv', encoding='utf-8')

print(file.to_string())