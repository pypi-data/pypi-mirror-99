import accuasset
import pandas as pd

df = pd.read_csv('../test_data/dir_list.csv')


print(df.columns)
accuasset.domain.eda.visualize.get_cloud(df,target_column='type')
#accuasset.domain.eda.visualize.test()
