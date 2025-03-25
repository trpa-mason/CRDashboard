from datetime import datetime, timedelta
import pandas as pd
import requests

if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

@data_loader
def get_data_lake_level():
    # Tahoe City Dam 10337000
    site_number = 10337000
    # record goes back to ~2007
    start_date = datetime(2007, 1, 1)
    end_date   = datetime.now()
    start_date_str = start_date.strftime("%Y-%m-%d")
    end_date_str = end_date.strftime("%Y-%m-%d")
    # usgs api url
    url = f"https://waterservices.usgs.gov/nwis/iv/?format=json&sites={site_number}&parameterCd=00065&startDT={start_date_str}&endDT={end_date_str}"
    # get json data
    response = requests.get(url)
    data     = response.json()
    # Extract time series data
    time_series = data['value']['timeSeries']
    # the JSON data has two index values for each time series, splitting the recrod on 04/29/2024
    indexes = [0,1]
    # Extract values and datetime from timeSeries JSON data
    values  = []
    for i in indexes:
        for series in time_series:
            for value in series['values'][i]['value']:
                values.append({
                    'dateTime': value['dateTime'],
                    'value': value['value']
                })
    # Convert to DataFrame
    df = pd.DataFrame(values)
    # format values and group by weekly mean
    df["dateTime"] = pd.to_datetime(df["dateTime"], utc=True)
    df["value"]    = pd.to_numeric(df["value"])
    # add datum value
    df["value"]    = df["value"] + 6220
    df = df.groupby(pd.Grouper(key="dateTime", freq="W"))["value"].mean().reset_index()
    return df

@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'