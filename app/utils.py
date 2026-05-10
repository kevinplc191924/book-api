import numpy as np
import pandas as pd

# FastAPI expect None, not pandas NaN
# Further transformations can produce new NaNs
# For that reason, use this before creating the dictionary for the response
def clean_for_json(df: pd.DataFrame):
    return df.replace({np.nan: None})