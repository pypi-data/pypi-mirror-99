import pandas as pd

transformers_df = pd.DataFrame(
    {
        'id':[1,1,2,3,3],
        'x':[0,1,2,3,4],
        'y':[5,6,7,8,9]
    }
)

impute_df = pd.DataFrame(
    {
        'id':[1,1,2,3,3,1,2,2,4,3,4,4],
        'x':[1,1,2,2,1,1,2,2,1,1,2,2],
        'y':[1,1,0,0,1,1,0,0,1,1,0,0]
    }
)