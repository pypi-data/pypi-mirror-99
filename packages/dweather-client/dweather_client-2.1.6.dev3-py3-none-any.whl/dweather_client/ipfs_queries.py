"""
Queries associated with the ipfs protocol option.
"""

import ipfshttpclient, json, requests, datetime, io, gzip
from dweather_client.ipfs_errors import *
from dweather_client.utils import listify_period
from dweather_client.df_utils import get_station_ids_with_icao
import dweather_client.ipfs_datasets
import pandas as pd
from dweather_client.http_queries import get_heads

def cat_metadata(hash_str, client=None, pin=True):
    """
    Get the metadata file for a given hash.
    Args:
        url (str): the url of the IPFS server
        hash_str (str): the hash of the ipfs dataset
    Returns (example metadata.json):
    
        {
            'date range': [
                '1981/01/01',
                '2019/07/31'
            ],
            'entry delimiter': ',',
            'latitude range': [
                -49.975, 49.975
            ],
            'longitude range': [
                -179.975, 179.975]
            ,
            'name': 'CHIRPS .05 Daily Full Set Uncompressed',
            'period': 'daily',
            'precision': 0.01,
            'resolution': 0.05,
            'unit of measurement': 'mm',
            'year delimiter': '\n'
        }
    """
    session_client = ipfshttpclient.connect() if client is None else client
    try:
        if pin:
            session_client.pin.add(hash_str + "/metadata.json")
        metadata = session_client.cat(hash_str + "/metadata.json")
    finally: 
        if (client is None):
            session_client.close()
    return json.loads(metadata)


def cat_hash_cell(hash_str, coord_str, client=None):
    if (client is None):
        with ipfshttpclient.connect() as client:
            return client.cat(hash_str + '/' + coord_str)
    else:
        return client.cat(hash_str + '/' + coord_str)

def cat_zipped_hash_cell(url, hash_str, coord_str, client=None):
    """
    Read a text file on the ipfs server compressed with gzip.
    Args:
        url (str): the url of the ipfs server
        hash_str (str): the hash of the dataset
        coord_str (str): the text file coordinate name e.g. 45.000_-96.000
    Returns:
        the contents of the file as a string
    """
    if (client is None):
        with ipfshttpclient.connect() as client:
            cell = client.cat(hash_str + '/' + coord_str + ".gz")
            with gzip.GzipFile(fileobj=io.BytesIO(cell)) as zip_data:
                return zip_data.read().decode("utf-8")
    else:
        cell = client.cat(hash_str + '/' + coord_str + ".gz")
        with gzip.GzipFile(fileobj=io.BytesIO(cell)) as zip_data:
            return zip_data.read().decode("utf-8")


def cat_dataset_cell(lat, lon, dataset_revision, client=None):
    """ 
    Retrieve the text of a grid cell data file for a given lat lon and dataset.
    Args:
        lat (float): the latitude of the grid cell, to 3 decimals
        lon (float): the longitude of the grid cell, to 3 decimals
    Returns:
        A tuple (json, str) of the dataset metadata file and the grid cell data text
    Raises: 
        DatasetError: If no matching dataset found on server
        InputOutOfRangeError: If the lat/lon is outside the dataset range in metadata
        CoordinateNotFoundError: If the lat/lon coordinate is not found on server
    """
    all_hashes = get_heads()
    if dataset_revision in all_hashes:
        dataset_hash = all_hashes[dataset_revision]
    else:
        raise DatasetError('{} not found on server'.format(dataset_revision))

    metadata = cat_metadata(dataset_hash, client)
    min_lat, max_lat = sorted(metadata["latitude range"])
    min_lon, max_lon = sorted(metadata["longitude range"])
    if lat < min_lat or lat > max_lat:
        raise InputOutOfRangeError("Latitude {} out of dataset revision range [{:.3f}, {:.3f}] for {}".format(lat, min_lat, max_lat, dataset_revision))
    if  lon < min_lon or lon > max_lon:
        raise InputOutOfRangeError("Longitude {} out of dataset revision range [{:.3f}, {:.3f}] for {}".format(lon, min_lon, max_lon, dataset_revision))
    coord_str = "{:.3f}_{:.3f}".format(lat,lon)
    try:
        if "compression" in metadata and metadata["compression"] == "gzip":
            text_data = cat_zipped_hash_cell(GATEWAY_URL, dataset_hash, coord_str, client=client)
        else:
            text_data = cat_hash_cell(dataset_hash, coord_str, client=client)
        return metadata, text_data
    except requests.exceptions.HTTPError as e:
        raise CoordinateNotFoundError('Coordinate ({}, {}) not found  on ipfs in dataset revision {}'.format(lat, lon, dataset_revision))



def cat_rainfall_dict(lat, lon, dataset_revision, return_metadata=False, client=None):
    """ 
    Build a dict of rainfall data for a given grid cell.
    Args:
        lat (float): the latitude of the grid cell, to 3 decimals
        lon (float): the longitude of the grid cell, to 3 decimals
    Returns:
        a dict ({datetime.date: float}) of datetime dates and the corresponding rainfall in mm for that date
    Raises:
        DatasetError: If no matching dataset found on server
        InputOutOfRangeError: If the lat/lon is outside the dataset range in metadata
        CoordinateNotFoundError: If the lat/lon coordinate is not found on server
        DataMalformedError: If the grid cell file can't be parsed as rainfall data
    """
    metadata, rainfall_text = cat_dataset_cell(lat, lon, dataset_revision, client=client)
    dataset_start_date = datetime.datetime.strptime(metadata['date range'][0], "%Y/%m/%d").date()
    dataset_end_date = datetime.datetime.strptime(metadata['date range'][1], "%Y/%m/%d").date()
    timedelta = dataset_end_date - dataset_start_date
    days_in_record = timedelta.days + 1 # we have both the start and end date in the dataset so its the difference + 1
    try:
        rainfall_text = rainfall_text.decode()
    except:
        pass
    day_strs = rainfall_text.replace(',', ' ').split()
    if (len(day_strs) != days_in_record):
        raise DataMalformedError ("Number of days in data file does not match the provided metadata")
    rainfall_dict = {}
    for i in range(days_in_record):
        if day_strs[i] == metadata["missing value"]:
            rainfall_dict[dataset_start_date + datetime.timedelta(days=i)] = None
        else:
            rainfall_dict[dataset_start_date + datetime.timedelta(days=i)] = float(day_strs[i])
    if return_metadata:
        return metadata, rainfall_dict
    else:
        return rainfall_dict
  

def cat_rev_rainfall_dict(lat, lon, dataset, desired_end_date, latest_rev):
    """
    Build a dictionary of rainfall data. Include as much of the most accurate, final data as possible. Start by buidling from the most accurate data,
    then keep appending data from more recent/less accurate versions of the dataset until we run out or reach the end date.

    This will not throw an error if there are no revisions with data available, it will simply return what is available.
    Args:
        lat (float): the grid cell latitude
        lon (float): the grid cell longitude
        dataset (str): the name of the dataset, e.g., "chirps_05-daily" on hashes.json
        desired_end_date (datetime.date): the last day of data needed.
        latest_rev (str): the least accurate revision of the dataset that is considered final
    Returns:
        tuple:
            a dict ({datetime.date: float}) of datetime dates and the corresponding rainfall in mm for that date
            bool is_final: if all data up to desired end date is final, this will be true
    """
    all_rainfall = {}
    is_final = True
    with ipfshttpclient.connect() as client:
        # Build the rainfall from the most accurate revision of the dataset to the least
        for dataset_revision in dweather_client.ipfs_datasets.datasets[dataset]:
            additional_rainfall = cat_rainfall_dict(lat, lon, dataset_revision, client=client)
            all_dates = list(all_rainfall) + list(additional_rainfall)
            all_rainfall = {date: all_rainfall[date] if date in all_rainfall else additional_rainfall[date] for date in all_dates}
            # stop when we have the desired end date in the dataset
            if desired_end_date in all_rainfall:
                return all_rainfall, is_final
            # data is no longer final after we pass the specified version
            if dataset_revision == latest_rev:
                is_final = False

    # If we don't reach the desired dataset, return all data.
    return all_rainfall, is_final


def cat_temperature_dict(lat, lon, dataset_revision, return_metadata=False, client=None):
    """
    Build a dict of temperature data for a given grid cell.
    Args:
        lat (float): the latitude of the grid cell, to 3 decimals
        lon (float): the longitude of the grid cell, to 3 decimals
    Returns:
        tuple (highs, lows) of dicts
        highs: dict ({datetime.date: float}) of datetime dates and the corresponding high temperature in degress F
        lows: dict ({datetime.date: float}) of datetime dates and the corresponding low temperature in degress F
    Raises:
        DatasetError: If no matching dataset_revision found on server
        InputOutOfRangeError: If the lat/lon is outside the dataset_revision range in metadata
        CoordinateNotFoundError: If the lat/lon coordinate is not found on server
        DataMalformedError: If the grid cell file can't be parsed as temperature data
    """
    metadata, temp_text = cat_dataset_cell(lat, lon, dataset_revision, client=client)
    dataset_start_date = datetime.datetime.strptime(metadata['date range'][0], "%Y/%m/%d").date()
    dataset_end_date = datetime.datetime.strptime(metadata['date range'][1], "%Y/%m/%d").date()
    timedelta = dataset_end_date - dataset_start_date
    days_in_record = timedelta.days + 1 # we have both the start and end date in the dataset_revision so its the difference + 1
    try:
        temp_text = temp_text.decode()
    except:
        pass
    day_strs = temp_text.replace(',', ' ').split()
    if (len(day_strs) != days_in_record):
        raise DataMalformedError ("Number of days in data file does not match the provided metadata")
    highs = {}
    lows = {}
    for i in range(days_in_record):
        low, high = map(float, day_strs[i].split('/'))
        date_iter = dataset_start_date + datetime.timedelta(days=i)
        highs[date_iter] = high
        lows[date_iter] = low
    if return_metadata:
        return metadata, highs, lows
    else:
        return highs, lows


def cat_rev_temperature_dict(lat, lon, dataset, desired_end_date, latest_rev):
    """
    Build a dictionary of rainfall data. Include as much final data as possible. If the desired end date
    is not in the final dataset, append as much prelim as possible.
    Args:
        lat (float): the latitude of the grid cell, to 3 decimals
        lon (float): the longitude of the grid cell, to 3 decimals
        dataset (str): the dataset name as on hashes.json
        desired_end_date (datetime.date): don't include prelim data after this point if not needed
        latest_rev (str): The least accurate revision that is still considered 'final'
    returns:
        tuple (highs, lows) of dicts and a bool
        highs: dict ({datetime.date: float}) of datetime dates and the corresponding high temperature in degress F
        lows: dict ({datetime.date: float}) of datetime dates and the corresponding low temperature in degress F
        is_final: True if all data is from final dataset, false if prelim included
    """
    highs = {}
    lows = {}
    is_final = True

    with ipfshttpclient.connect() as client:
        # Build the data from the most accurate version of the dataset to the least
        for dataset_revision in dweather_client.ipfs_datasets.datasets[dataset]:
            additional_highs, additional_lows = cat_temperature_dict(lat, lon, dataset_revision, client=client)
            all_dates = list(highs) + list(additional_highs)    
            highs = {date: highs[date] if date in highs else additional_highs[date] for date in all_dates}
            lows = {date: lows[date] if date in lows else additional_lows[date] for date in all_dates}
            # Stop early if we have the end date
            if desired_end_date in highs:
                return highs, lows, is_final

            # data is no longer final after we pass the specified version
            if dataset_revision == latest_rev:
                is_final = False

    # If we don't reach the desired dataset, return all data.
    return highs, lows, is_final


def pin_all_stations(client=None, station_dataset="ghcnd-imputed-daily"):
    """ Sync all stations locally."""
    heads = get_heads()
    dataset_hash = heads[station_dataset]
    session_client = ipfshttpclient.connect() if client is None else client
    try:
        session_client.pin.add(dataset_hash)
    finally:
        if (client is None):
            session_client.close()

def cat_station_df(station_id, station_dataset="ghcnd-imputed-daily", client=None, pin=True, force_hash=None):
    """ Cat a given station's raw data as a pandas dataframe. """
    df = pd.read_csv(io.StringIO(\
        cat_station_csv(
            station_id,
            station_dataset=station_dataset,
            client=client, 
            pin=pin,
            force_hash=force_hash
        )
    ))
    return df.set_index(pd.DatetimeIndex(df['DATE']))

def cat_station_csv(station_id, station_dataset="ghcnd-imputed-daily", client=None, pin=True, force_hash=None):
    """
    Retrieve the contents of a station data csv file.
    Args:
        station_id (str): the id of the weather station
        station_dataset(str): on of ["ghcnd", "ghcnd-imputed-daily"]
    returns:
        the contents of the station csv file as a string
    """
    if (force_hash is None):
        all_hashes = get_heads()
        dataset_hash = all_hashes[station_dataset]
    else:
        dataset_hash = force_hash
    csv_hash = dataset_hash + '/' + station_id + ".csv.gz"
    session_client = ipfshttpclient.connect() if client is None else client
    try:
        if pin:
            session_client.pin.add(csv_hash)
        csv = session_client.cat(csv_hash)
        with gzip.GzipFile(fileobj=io.BytesIO(csv)) as zip_data:
            return zip_data.read().decode("utf-8")
    finally:
        if (client is None):
            session_client.close()

def cat_icao_stations(station_dataset="ghcnd-imputed-daily", pin=True, force_hash=None):
    """
    For every station that has an icao code, load it into a dataframe and
    return them all as a list.
    """
    station_ids = get_station_ids_with_icao()
    return cat_station_df_list(station_ids, station_dataset=station_dataset, pin=pin, force_hash=force_hash)

def cat_n_closest_station_dfs(lat, lon, n, station_dataset="ghcnd-imputed-daily", pin=True, force_hash=None):
    """
    Load the closest n stations to a given point into a list of dataframes.
    """
    if (force_hash is None):
        metadata = cat_metadata(get_heads()[station_dataset])
    else:
        metadata = cat_metadata(force_hash)
    station_ids = get_n_closest_station_ids(lat, lon, metadata, n)
    return cat_station_df_list(station_ids, station_dataset=station_dataset, pin=pin, force_hash=force_hash)

def cat_station_df_list(station_ids, station_dataset="ghcnd-imputed-daily", pin=True, force_hash=None):
    batch_hash = force_hash
    if (force_hash is None):
        batch_hash = get_heads()[station_dataset]
    metadata = cat_metadata(batch_hash, pin=pin)
    station_content = []
    with ipfshttpclient.connect() as client:
        for station_id in station_ids:
            logging.info("(%i of %i): Loading station %s from %s into DataFrame%s" % ( \
                station_ids.index(station_id) + 1,
                len(station_ids),
                station_id, 
                "dWeather head" if force_hash is None else "forced hash",
                " and pinning to ipfs datastore" if pin else ""
            ))
            try:
                station_content.append(cat_station_df( \
                    station_id,
                    station_dataset=station_dataset,
                    client=client,
                    pin=pin,
                    force_hash=batch_hash
            ))
            except ipfshttpclient.exceptions.ErrorResponse:
                logging.warning("Station %s not found" % station_id)
                
    return station_content 


def cat_icao_stations(client=None, pin=True):
    """ Get a list of station dataframes for all stations that have an icao"""
    dfs = []
    session_client = ipfshttpclient.connect() if client is None else client
    try:
        for station_id in get_station_ids_with_icao():
            try:
                print(station_id)
                dfs.append(cat_station_csv(station_id, client=client, pin=pin))
            except Exception as e:
                print(e)
                continue
    finally:
        if (client is None):
            session_client.close()
    return dfs
