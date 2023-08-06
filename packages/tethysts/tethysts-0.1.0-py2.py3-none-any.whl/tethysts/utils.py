"""


"""
import requests
import xarray as xr
import pandas as pd
import orjson
from datetime import datetime
import zstandard as zstd
import pickle
import copy
import boto3
import botocore
from multiprocessing.pool import ThreadPool
from time import sleep
# import shapely

pd.options.display.max_columns = 10


##############################################
### Reference objects

key_patterns = {'results': 'tethys/v2/{dataset_id}/{station_id}/{run_date}/results.nc.zst',
                'results_buffer': 'tethys/v2/{dataset_id}/{station_id}/{run_date}/results_buffer.nc.zst',
                'datasets': 'tethys/v2/datasets.json.zst',
                'stations': 'tethys/v2/{dataset_id}/stations.json.zst',
                'station': 'tethys/v2/{dataset_id}/{station_id}/station.json.zst',
                'dataset': 'tethys/v2/{dataset_id}/dataset.json.zst',
                }

b2_public_key_pattern = '{base_url}/file/{bucket}/{obj_key}'

##############################################
### Helper functions


def read_pkl_zstd(obj, unpickle=False):
    """
    Deserializer from a pickled object compressed with zstandard.

    Parameters
    ----------
    obj : bytes or str
        Either a bytes object that has been pickled and compressed or a str path to the file object.
    unpickle : bool
        Should the bytes object be unpickled or left as bytes?

    Returns
    -------
    Python object
    """
    dctx = zstd.ZstdDecompressor()
    if isinstance(obj, str):
        with open(obj, 'rb') as p:
            obj1 = dctx.decompress(p.read())
    elif isinstance(obj, bytes):
        obj1 = dctx.decompress(obj)
    else:
        raise TypeError('obj must either be a str path or a bytes object')

    if unpickle:
        obj1 = pickle.loads(obj1)

    return obj1


def read_json_zstd(obj):
    """
    Deserializer from a compressed zstandard json object to a dictionary.

    Parameters
    ----------
    obj : bytes
        The bytes object.

    Returns
    -------
    Dict
    """
    dctx = zstd.ZstdDecompressor()
    obj1 = dctx.decompress(obj)
    dict1 = orjson.loads(obj1)

    return dict1


def s3_connection(connection_config, max_pool_connections=30):
    """
    Function to establish a connection with an S3 account. This can use the legacy connect (signature_version s3) and the curent version.

    Parameters
    ----------
    connection_config : dict
        A dictionary of the connection info necessary to establish an S3 connection. It should contain service_name, endpoint_url, aws_access_key_id, and aws_secret_access_key. connection_config can also be a URL to a public S3 bucket.
    max_pool_connections : int
        The number of simultaneous connections for the S3 connection.

    Returns
    -------
    S3 client object
    """
    s3_config = copy.deepcopy(connection_config)

    if 'config' in s3_config:
        config0 = s3_config.pop('config')
        config0.update({'max_pool_connections': max_pool_connections})
        config1 = boto3.session.Config(**config0)

        s3_config1 = s3_config.copy()
        s3_config1.update({'config': config1})

        s3 = boto3.client(**s3_config1)
    else:
        s3_config.update({'config': botocore.config.Config(max_pool_connections=max_pool_connections)})
        s3 = boto3.client(**s3_config)

    return s3


def get_object_s3(obj_key, connection_config, bucket, compression=None, counter=5):
    """
    General function to get an object from an S3 bucket.

    Parameters
    ----------
    obj_key : str
        The object key in the S3 bucket.
    connection_config : dict
        A dictionary of the connection info necessary to establish an S3 connection. It should contain service_name, s3, endpoint_url, aws_access_key_id, and aws_secret_access_key. connection_config can also be a URL to a public S3 bucket.
    bucket : str
        The bucket name.
    compression : None or str
        The compression of the object that should be decompressed. Options include zstd.
    counter : int
        Number of times to retry to get the object.

    Returns
    -------
    bytes
        bytes object of the S3 object.
    """
    counter1 = counter
    while True:
        try:
            if isinstance(connection_config, dict):
                s3 = s3_connection(connection_config)

                ts_resp = s3.get_object(Key=obj_key, Bucket=bucket)
                ts_obj = ts_resp.pop('Body').read()

            elif isinstance(connection_config, str):
                url = b2_public_key_pattern.format(base_url=connection_config, bucket=bucket, obj_key=obj_key)
                ts_obj = requests.get(url).content

            if isinstance(compression, str):
                if compression == 'zstd':
                    ts_obj = read_pkl_zstd(ts_obj, False)
                else:
                    raise ValueError('compression option can only be zstd or None')
            break
        except:
            if counter1 == 0:
                raise ValueError('Could not properly extract the object after several tries')
            else:
                print('Could not properly extract the object; trying again in 5 seconds')
                counter1 = counter1 - 1
                sleep(5)

    return ts_obj


def result_filters(ts_xr, from_date=None, to_date=None, from_mod_date=None, to_mod_date=None, remove_height=False):
    """

    """
    if isinstance(from_date, (str, pd.Timestamp, datetime)):
        from_date1 = pd.Timestamp(from_date)
    else:
        from_date1 = None
    if isinstance(to_date, (str, pd.Timestamp, datetime)):
        to_date1 = pd.Timestamp(to_date)
    else:
        to_date1 = None

    if isinstance(from_mod_date, (str, pd.Timestamp, datetime)):
        from_mod_date1 = pd.Timestamp(from_mod_date)
    else:
        from_mod_date1 = None
    if isinstance(to_mod_date, (str, pd.Timestamp, datetime)):
        to_mod_date1 = pd.Timestamp(to_mod_date)
    else:
        to_mod_date1 = None

    if (to_date1 is not None) or (from_date1 is not None):
        ts_xr1 = ts_xr.sel(time=slice(from_date1, to_date1))
    else:
        ts_xr1 = ts_xr

    if (to_mod_date1 is not None) or (from_mod_date1 is not None):
        if 'modified_date' in ts_xr1:
            ts_xr1 = ts_xr1.sel(modified_date=slice(from_mod_date1, to_mod_date1))

    if remove_height:
        ts_xr1 = ts_xr1.squeeze('height').drop('height')

    return ts_xr1


def process_results_output(ts_xr, parameter, modified_date=False, quality_code=False, output='DataArray'):
    """

    """
    out_param = [parameter]

    if quality_code:
        if 'quality_code' in ts_xr:
            out_param.extend(['quality_code'])

    if modified_date:
        if 'modified_date' in ts_xr:
            out_param.extend(['modified_date'])

    if len(out_param) == 1:
        out_param = out_param[0]

    ## Return
    if output == 'Dataset':
        return ts_xr

    elif output == 'DataArray':
        return ts_xr[out_param]

    elif output == 'Dict':
        darr = ts_xr[out_param]
        data_dict = darr.to_dict()
        if 'name' in data_dict:
            data_dict.pop('name')

        return data_dict

    elif output == 'json':
        darr = ts_xr[out_param]
        data_dict = darr.to_dict()
        if 'name' in data_dict:
            data_dict.pop('name')
        json1 = orjson.dumps(data_dict)

        return json1
    else:
        raise ValueError("output must be one of 'Dataset', 'DataArray', 'Dict', or 'json'")
