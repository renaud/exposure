import pandas as pd
import numpy as np
import exposure


ex = exposure.Exposure()

# simple collection objects
mydict = {'banana': 'yellow', 'mango': 'yellow', 'apple': 'red'}
ex.add(mydict, 'fruits')

mylist = ['Joe', 'Anna', 'Fred']
ex.add(mylist, 'names')

mytuples = ('one', 'two', 'tree')
ex.add(mytuples, 'mytuples')


# pandas
serie = pd.Series(np.random.randn(10))
ex.add(serie, 'pd.serie')

data_frame = pd.DataFrame(np.random.randn(8, 3), columns=['A', 'B', 'C'])
ex.add(data_frame, 'pd.data_frame')
#http://localhost:8888/ex/pd.data_frame/A>0.4


ex.start()
