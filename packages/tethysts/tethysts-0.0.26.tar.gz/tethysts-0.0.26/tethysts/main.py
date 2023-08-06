"""
Created on 2020-11-05.

@author: Mike K
"""
import os
import numpy as np
import xarray as xr
import pandas as pd
import orjson
# import yaml
from datetime import datetime
import copy
from multiprocessing.pool import ThreadPool
# import shapely
from tethysts.utils import get_object_s3, result_filters, process_results_output, read_json_zstd, key_patterns

pd.options.display.max_columns = 10


##############################################
### Parameters



##############################################
### Class


class Tethys(object):
    """
    The base Tethys object.

    Parameters
    ----------
    remotes_list : list of dict
        list of dict of the S3 remotes to access. The dicts must contain:
        bucket and connection_config. bucket is a string with the bucket name. connection_config is a dict of service_name, s3, endpoint_url, aws_access_key_id, and aws_secret_access_key.

    Returns
    -------
    tethys object
    """

    ## Initial import and assignment function
    def __init__(self, remotes_list=None):
        """

        """
        setattr(self, 'datasets', [])
        setattr(self, '_datasets', {})
        setattr(self, '_remotes', {})
        setattr(self, '_stations', {})
        setattr(self, '_key_patterns', key_patterns)

        if isinstance(remotes_list, list):
            datasets = self.get_remotes(remotes_list)

        else:
            pass


    def get_remotes(self, remotes_list, threads=20):
        """
        The function to get many datasets from many remotes.

        Parameters
        ----------
        remotes_list : list of dict
            list of dict of the S3 remotes to access. The dicts must contain:
            bucket and connection_config. bucket is a string with the bucket name. connection_config is a dict of service_name, endpoint_url, aws_access_key_id, and aws_secret_access_key. connection_config can also be a URL to a public S3 bucket.
        threads : int
            The number of threads to use. I.E. the number of simultaneous remote reads.

        Returns
        -------
        dict
            of datasets
        """
        output = ThreadPool(threads).map(self.get_datasets, remotes_list)

        return self.datasets


    def get_datasets(self, remote):
        """
        Get datasets from an individual remote. Saves result into the object.

        Parameters
        ----------
        remote : dict
            dict of the S3 remote to access. The dict must contain:
            bucket and connection_config. bucket is a string with the bucket name. connection_config is a dict of service_name, endpoint_url, aws_access_key_id, and aws_secret_access_key. connection_config can also be a URL to a public S3 bucket.

        Returns
        -------
        None
        """
        try:
            ds_obj = get_object_s3(self._key_patterns['datasets'], remote['connection_config'], remote['bucket'])
            ds_list = read_json_zstd(ds_obj)

            ds_list2 = copy.deepcopy(ds_list)
            # [l.pop('properties') for l in ds_list2]
            self.datasets.extend(ds_list2)

            ds_dict = {d['dataset_id']: d for d in ds_list}
            remote_dict = {d: {'dataset_id': d, 'bucket': remote['bucket'], 'connection_config': remote['connection_config']} for d in ds_dict}

            self._datasets.update(ds_dict)
            self._remotes.update(remote_dict)

        except:
            print('No datasets.json.zst file in S3 bucket')


    def get_stations(self, dataset_id):
        """
        Method to return the stations associated with a dataset.

        Parameters
        ----------
        dataset_id : str
            The dataset_id of the dataset.

        Returns
        -------
        list of dict
            of station data
        """
        # dataset = self._datasets_sites[dataset_id]
        # if not hasattr(self, '_datasets_sites'):

        remote = self._remotes[dataset_id]

        site_key = self._key_patterns['stations'].format(dataset_id=dataset_id)

        try:
            stn_obj = get_object_s3(site_key, remote['connection_config'], remote['bucket'])
            stn_list = read_json_zstd(stn_obj)
            stn_list = [s for s in stn_list if isinstance(s, dict)]

            self._stations.update({dataset_id: {s['station_id']: s for s in stn_list}})

            ## Run spatial query here!

            return stn_list

        except:
            print('No stations.json.zst file in S3 bucket')


    def get_run_dates(self, dataset_id, station_id):
        """
        Function to get the run dates of a particular dataset and station.

        Parameters
        ----------
        dataset_id : str
            The dataset_id of the dataset.
        station_id : str
            The station_id of the associated station.

        Returns
        -------
        list
        """
        if dataset_id not in self._stations:
            stns = self.get_stations(dataset_id)

        dataset_stn = self._stations[dataset_id][station_id]

        run_dates = np.unique([ob['run_date'].split('+')[0] if '+' in ob['run_date'] else ob['run_date'] for ob in dataset_stn['results_object_key']]).tolist()

        return run_dates


    def _get_results_obj_key_s3(self, dataset_id, station_id, run_date):
        """

        """
        if dataset_id not in self._stations:
            stns = self.get_stations(dataset_id)

        dataset_stn = self._stations[dataset_id][station_id]

        obj_keys = dataset_stn['results_object_key']
        obj_keys_df = pd.DataFrame(obj_keys)
        obj_keys_df['run_date'] = pd.to_datetime(obj_keys_df['run_date']).dt.tz_localize(None)
        last_run_date = obj_keys_df['run_date'].max()
        last_key = obj_keys_df[obj_keys_df['run_date'] == last_run_date]['key']

        # bucket = obj_keys[0]['bucket']

        ## Set the correct run_date
        if isinstance(run_date, (str, pd.Timestamp)):
            run_date1 = pd.Timestamp(run_date)

            obj_key_df = obj_keys_df[obj_keys_df['run_date'] == run_date1]

            if obj_key_df.empty:
                print('Requested run_date is not available, returning last run_date results')
                obj_key = last_key
            else:
                obj_key = obj_key_df['key']
        else:
            obj_key = last_key

        return obj_key


    def get_results(self, dataset_id, station_id, from_date=None, to_date=None, from_mod_date=None, to_mod_date=None, modified_date=False, quality_code=False, run_date=None, remove_height=False, output='DataArray', max_connections=10):
        """
        Function to query the time series data given a specific dataset_id and station_id. Multiple optional outputs.

        Parameters
        ----------
        dataset_id : str
            The dataset_id of the dataset.
        station_id : str
            The station_id of the associated station.
        from_date : str, Timestamp, datetime, or None
            The start date of the selection.
        to_date : str, Timestamp, datetime, or None
            The end date of the selection.
        from_mod_date : str, Timestamp, datetime, or None
            Only return data post the defined modified date.
        to_mod_date : str, Timestamp, datetime, or None
            Only return data prior to the defined modified date.
        modified_date : bool
            Should the modified dates be returned if they exist?
        quality_code : bool
            Should the quality codes be returned if they exist?
        run_date : str or Timestamp
            The run_date of the results to be returned. Defaults to None which will return the last run date.
        remove_height : bool
            Should the height dimension be removed from the output?
        output : str
            Output format of the results. Options are:
                Dataset - return the entire contents of the netcdf file as an xarray Dataset,
                DataArray - return the requested dataset parameter as an xarray DataArray,
                Dict - return a dictionary of results from the DataArray,
                json - return a json str of the Dict.

        Returns
        -------
        Whatever the output was set to.
        """

        ## Get parameters
        dataset = self._datasets[dataset_id]
        parameter = dataset['parameter']
        remote = self._remotes[dataset_id]

        ## Get object key
        obj_key = self._get_results_obj_key_s3(dataset_id, station_id, run_date)

        ## Get results
        # data_list = []
        # for key in obj_key:
        #     ts_obj = get_object_s3(key, remote['connection_config'], remote['bucket'], 'zstd')
        #     ts_xr = xr.open_dataset(ts_obj)
        #     data_list.append(ts_xr)

        # xr2 = xr.concat(data_list, dim='time', data_vars='minimal')
        # xr3 = xr2.sel(time=~xr2.get_index('time').duplicated('last'))

        ts_obj = get_object_s3(obj_key.iloc[0], remote['connection_config'], remote['bucket'], 'zstd')
        xr3 = xr.open_dataset(ts_obj)

        ## Filters
        ts_xr1 = result_filters(xr3, from_date, to_date, from_mod_date, to_mod_date, remove_height)

        ## Output
        output1 = process_results_output(ts_xr1, parameter, modified_date, quality_code, output)

        return output1


    def get_bulk_results(self, dataset_id, station_ids, from_date=None, to_date=None, from_mod_date=None, to_mod_date=None, modified_date=False, quality_code=False, run_date=None, remove_height=False, output='DataArray', threads=10):
        """
        Function to bulk query the time series data given a specific dataset_id and a list of site_ids. Multiple optional outputs.

        Parameters
        ----------
        dataset_id : str
            The hashed str of the dataset_id.
        site_ids : list of str
            A list of hashed str of the site_ids.
        from_date : str, Timestamp, datetime, or None
            The start date of the selection.
        to_date : str, Timestamp, datetime, or None
            The end date of the selection.
        from_mod_date : str, Timestamp, datetime, or None
            Only return data post the defined modified date.
        to_mod_date : str, Timestamp, datetime, or None
            Only return data prior to the defined modified date.
        modified_date : bool
            Should the modified dates be returned if they exist?
        quality_code : bool
            Should the quality codes be returned if they exist?
        run_date : str or Timestamp
            The run_date of the results to be returned. Defaults to None which will return the last run date.
        remove_height : bool
            Should the height dimension be removed from the output?
        output : str
            Output format of the results. Options are:
                Dataset - return the entire contents of the netcdf file as an xarray Dataset,
                DataArray - return the requested dataset parameter as an xarray DataArray,
                Dict - return a dictionary of results from the DataArray,
                json - return a json str of the Dict.

        Returns
        -------
        A dictionary of station_id key to a value of whatever the output was set to.
        """
        lister = [(dataset_id, s, from_date, to_date, from_mod_date, to_mod_date, modified_date, quality_code, run_date, remove_height, output, threads) for s in station_ids]

        output = ThreadPool(threads).starmap(self.get_results, lister)

        output2 = dict(zip(station_ids, output))

        return output2



######################################
### Testing

