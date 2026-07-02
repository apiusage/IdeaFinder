
import pandas as pd
def export_csv(data,path):
    pd.DataFrame(data).to_csv(path,index=False)
