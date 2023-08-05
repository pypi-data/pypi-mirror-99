from mathmodel import dataset

data=dataset.load_boston()
print(data)

from sklearn import datasets

import pandas as pd

boston = datasets.load_boston()

df = pd.DataFrame(boston.data, columns=boston.feature_names)

df['MEDV'] = boston['target']
print(df)

