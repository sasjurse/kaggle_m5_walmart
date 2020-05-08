import pandas as pd
import os

#%%

import generics.postgres
#%%

import os
hmm = os.getcwd()

path = os.getcwd()

#%%

from pathlib import Path
import pandas as pd

test = Path('../raw_data')
test2 = Path('calendar.csv')

df = pd.read_csv(test / test2)


#%%

if __name__ == '__main__':
    print(os.getcwd())
