import os
import msal
import pandas as pd
import requests
import sys
import time
from src.common.util import get_secret_value, validate_is_one_word


# -------------------------------------------------------
# Authentication
# -------------------------------------------------------


def get_app():
    return msal.ConfidentialClientApplication(
        get_secret_value('POWERBI_CLIENT_ID'),
        client_credential=get_secret_value('POWERBI_CLIENT_SECRET'),
        authority=os.environ['POWERBI_AUTHORITY_URI']
    )


def get_access_token(app):
    result = app.acquire_token_for_client(scopes=[
        "https://analysis.windows.net/powerbi/api/.default"
    ])
    if 'access_token' in result:
        return result['access_token']
    else:
        raise Exception(
            result.get("error") + ": " + result.get("error_description")
        )


def get_api_headers(app):
    access_token = get_access_token(app)
    return {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {access_token}'
    }


# -------------------------------------------------------
# Conversion from database schema to Power BI schema
# -------------------------------------------------------


def as_powerbi_datatype(dtype):
    if dtype == "int64":
        return "Int64"
    if dtype == "float64":
        return "Double"  # TODO: or Decimal?
    if dtype == "bool":
        return "Boolean"
    if dtype == "datetime64[ns]":
        return "Datetime"
    return "String"


def as_powerbi_value(df, name, value):
    if df[name].dtype == "datetime64[ns]":
        return value.isoformat()
    return value


def as_powerbi_table_schema(table_name, database, table_name_prefix="public "):
    validate_is_one_word(table_name)
    columns = []
    df = pd.read_sql(f'select * from {table_name} limit 1', con=database)
    for name in df:
        columns.append({
            "name": name,
            "dataType": as_powerbi_datatype(df[name].dtype)
        })
    return {
        "name": table_name_prefix + table_name,
        "columns": columns
    }


def as_powerbi_table_data(
        table_name,
        database,
        order_by="id",
        offset=0,
        limit=None):
    validate_is_one_word(table_name)
    rows = []
    query = f'select * from {table_name}'
    params = {}
    if limit:
        query = query + ' order by ' + order_by
        query = query + ' offset %(offset)s limit %(limit)s'
        params = {
            "offset": offset,
            "limit": limit
        }
    df = pd.read_sql(query, params=params, con=database)
    for index, row in df.iterrows():
        r = {}
        for name in df:
            r[name] = as_powerbi_value(df, name, row[name])
        rows.append(r)
    return {
        "rows": rows
    }


# -------------------------------------------------------
# API operations
# -------------------------------------------------------


def __check_response(response):
    if not response.ok:
        print(response, file=sys.stderr)
        raise Exception("Response not ok")


def create_dataset(api_headers, group_id, dataset_schema):
    validate_is_one_word(group_id)
    response = requests.post(
        url=f'https://api.powerbi.com/v1.0/myorg/groups/{group_id}/datasets?defaultRetentionPolicy=basicFIFO',  # noqa: E501
        headers=api_headers,
        json=dataset_schema
    )
    __check_response(response)
    return response.json()['id']


class PowerBIDataset():

    def __init__(self, api_headers, group_id, dataset_id, table_name_prefix):
        validate_is_one_word(group_id)
        validate_is_one_word(dataset_id)
        self.api_headers = api_headers
        self.group_id = group_id
        self.dataset_id = dataset_id
        self.table_name_prefix = table_name_prefix

    def update_table_schema(self, table_name, table_schema):
        validate_is_one_word(table_name)
        response = requests.post(
            url=f'https://api.powerbi.com/v1.0/myorg/groups/{self.group_id}/datasets/{self.datasetId}/tables/{self.table_name_prefix + table_name}',  # noqa: E501
            headers=self.api_headers,
            json=table_schema
        )
        __check_response(response)
        return response.json()['id']

    def insert_table_data(self, table_name, data):
        validate_is_one_word(table_name)
        response = requests.post(
            url=f'https://api.powerbi.com/v1.0/myorg/groups/{self.group_id}/datasets/{self.dataset_id}/tables/{self.table_name_prefix + table_name}/rows',  # noqa: E501
            headers=self.api_headers,
            json=data
        )
        __check_response(response)
        return response

    def delete_table_data(self, table_name):
        validate_is_one_word(table_name)
        response = requests.delete(
            url=f'https://api.powerbi.com/v1.0/myorg/groups/{self.group_id}/datasets/{self.dataset_id}/tables/{self.table_name_prefix + table_name}/rows',  # noqa: E501
            headers=self.api_headers
        )
        __check_response(response)
        return response

    def copy_table_data(
            self,
            table_name,
            order_by,
            database,
            delete_data=False,
            limit=10000):
        validate_is_one_word(table_name)

        if delete_data:
            self.delete_table_data(table_name)

        i = 0
        while True:
            data = as_powerbi_table_data(
                table_name,
                database,
                order_by,
                offset=i*limit,
                limit=limit
            )
            if len(data['rows']) <= 0:
                return
            self.insert_table_data(table_name, data)
            # Sleep to avoid more than 120 requests per minute
            # https://docs.microsoft.com/en-us/power-bi/developer/automation/api-rest-api-limitations
            time.sleep(0.6)
            i = i + 1
