import os
import pandas as pd
import requests

from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

import zipfile, io
from src.base import Base

class Crawler(Base):
    def __init__(self, api_key):
        super().__init__(api_key=api_key)
        self._get_download_link_url = Crawler.NESTQUANT_API_ENDPOINT + 'metric/%s/download?symbol=%s&resolution=%s&api_key=' + self._api_key
        self._get_lastest_data_url = Crawler.NESTQUANT_API_ENDPOINT + 'metric/%s/download/latest?symbol=%s&resolution=%s&api_key=' + self._api_key
        self._get_metrics_categories_url = Crawler.NESTQUANT_API_ENDPOINT + 'metric/categories'
    
    def _check_location(self, location: str):
        """ Verify the presence of a folder and create it if it is absent. """
        try:
            os.makedirs(location)
        except FileExistsError:
            print(f"Folder '{location}' already exists")
    
    def _get_data_response(
        self,
        metric_id: str,
        symbol: str,
        resolution: str,
        get_historical_data: bool
    ) -> requests.Response:
        """ 
            Retrieve the data response by generating the URL for the query procedure.

            Parameters
            -----------
                metric_id: str,
                    Id of the metric
                symbol: str,
                    data symbol, be careful that the symbol is case sensitive
                resolution: str,
                    Resolution of the data, e.g. 1d, 1h, for FRED data, we don't need to specify 
                    the resolution
                get_historical_data: bool
                    if the value is True, retrieve the historical data in a compressed zip format
                    if the value is False, return the 10 most recent data entries.

            Returns
            ----------
                a Response object
        """
    
        if get_historical_data:
            url = self._get_download_link_url % (metric_id, symbol, resolution)
        else:
            url = self._get_lastest_data_url % (metric_id, symbol, resolution)
        
        return self._get(url)

    def get_all_metrics(self) -> dict:
        return self._get(self._get_metrics_categories_url).json()

    def download_historical_data(
        self,
        metric_id: str,
        resolution: str,
        symbol: str,
        location: str
    ):
        """ 
            Download and extract the historical data, then save it to the specified 'location'.

            Parameters
            -----------
                metric_id: str,
                    Id of the metric
                resolution: str,
                    Resolution of the data, e.g. 1d, 1h, for FRED data, we don't need to specify 
                    the resolution
                symbol: str,
                    data symbol, be careful that the symbol is case sensitive
                location: str
                    the destination where the data should be saved.
        """
        data_response = self._get_data_response(
            metric_id=metric_id, symbol=symbol, resolution=resolution, get_historical_data=True)
        location = os.path.join(location, data_response.headers['content-disposition'].split(';')[1].split('=')[1].split('.')[0])
        self._check_location(location)
        z = zipfile.ZipFile(io.BytesIO(data_response.content))
        z.extractall(location)

    def get_lastest_data(
        self,
        metric_id: str,
        resolution: str,
        symbol: str
    ) -> dict:
        """ 
            Retrieve the lastest data in JSON format.

            Parameters
            -----------
                metric_id: str,
                    ID of the metric
                resolution: str,
                    Resolution of the data, e.g. 1d, 1h, for FRED data, we don't need to specify 
                    the resolution
                symbol: str,
                    data symbol, be careful that the symbol is case sensitive

            Returns
            -----------
                data in dict format
        """
        data_response = self._get_data_response(
            metric_id=metric_id,symbol=symbol, resolution=resolution, get_historical_data=False)
        return pd.read_csv(io.BytesIO(data_response.content))
