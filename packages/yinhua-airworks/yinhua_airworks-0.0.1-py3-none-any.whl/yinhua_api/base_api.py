import requests
import pandas as pd

SERVICE_URL = "http://10.1.185.2:8888"


def get_indicator_values(indicator_ids):
    url = '{}/api/v1/indicator_v2/export/dataframe_json'.format(SERVICE_URL)
    deduplication_list = list(set(indicator_ids))
    response = requests.post(url, json=dict(indicator_ids=deduplication_list))
    response.raise_for_status()
    res = []
    data = response.json()
    for indicator_id, indicator_data in data.items():
        df = pd.DataFrame.from_dict(indicator_data)
        df.name = indicator_id
        res.append(df)
    return res


if __name__ == "__main__":
    indicator_ids = ['all_indexpv_chain_rank_app_by_week_all']
    result = get_indicator_values(indicator_ids)
    print(result)
