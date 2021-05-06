from listingDetail import listingDetail
import pandas as pd

zip_list = ['85298', '85224', '49064', '85004', '49002']

full_list = list()

for zip_code in zip_list:
    detail = listingDetail(zip_code).get_detail()
    full_list = full_list + detail

df = pd.DataFrame(full_list)
print(df.to_dict(orient='records'))