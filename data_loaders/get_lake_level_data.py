from datetime import datetime, timedelta
import pandas as pd
import requests

if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

@data_loader
def get_data_lake_level():
    days = 6400
    site_number = 10337000
    # Calculate the start and end dates based on the selected time range
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    
    start_date_str = start_date.strftime("%Y-%m-%d")
    end_date_str = end_date.strftime("%Y-%m-%d")

    url = f"https://waterservices.usgs.gov/nwis/iv/?format=json&sites={site_number}&parameterCd=00065&startDT={start_date_str}&endDT={end_date_str}"

    response = requests.get(url)
    data = response.json()

    time_series_data = data["value"]["timeSeries"][0]["values"][0]["value"]

    df = pd.DataFrame(time_series_data)
    df["dateTime"] = pd.to_datetime(df["dateTime"], utc=True)
    df["value"] = pd.to_numeric(df["value"])
    df["value"] = df["value"] + 6220
    df = df.groupby(pd.Grouper(key="dateTime", freq="W"))["value"].mean().reset_index()
    return df

@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
