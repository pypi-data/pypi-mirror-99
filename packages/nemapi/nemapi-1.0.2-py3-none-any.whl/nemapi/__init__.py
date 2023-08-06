"""nemapi - Access to public National Electricity Market data through nemAPI."""

__version__ = '1.0.2'
__author__ = 'Jonathon Emerick <jonathon.emerick@uq.net.au>'

from xml.etree import ElementTree
import datetime as dt
import requests
import pandas as pd
import json
import pytz

from nemapi import URLs

global timezone
timezone = pytz.timezone('Australia/Brisbane')

class nemapi:
    def __init__(self, response_format="json"):
        self.format = response_format
        self.url = URLs.URLs(response_format=response_format)

        self.table_name = ""

    def __to_format(self, table_name, response):
        """Takes in json and converts data to pandas dataframe
        """
        if self.format == "json":
            try:
                data = json.loads(response.text)
                dataframe = pd.json_normalize(data[table_name])
                dataframe.set_index('settlementdate', inplace=True)
                return dataframe
            except:
                return "Outside of date range for table, please use an appropriate range."
        else:
            return "Not a JSON format response from API"
    
    def __get_data(self, url):
        # self.__create_auth()
        return self.__to_format(self.table_name, requests.get(url))

    def get_dispatch_price(self, intervals):
        """Returns data from dispatch_price table from AEMO MMS data model.

        Inputs
            intervals: allows the user to define a trailing number of dispatch intervals.
        
        Output
            dispatch_price: Dataframe of dispatch prices indexed on the column settlementdate.
            Columns currently included: settlementdate, regionid, rrp.
            ** Note - users are limited to 10,000 rows at a time.
        """
        self.table_name = 'dispatch_price'
        return self.__get_data(self.url.dispatch_price_url(str(intervals)))

    def get_dispatch_regionsum(self, intervals):
        """Returns data from dispatch_regionsum table from AEMO MMS data model.

        Inputs
            intervals: allows the user to define a trailing number of dispatch intervals.
        
        Output
            dispatch_regionsum: Dataframe of dispatch regionsum indexed on the column settlementdate.
            Columns currently included: settlementdate, regionid, totaldemand, availablegeneration, totalintermittentgeneration, demand_and_nonschedgen, uigf.
            ** Note - users are limited to 10,000 rows at a time.
        """
        self.table_name = 'dispatch_regionsum'
        return self.__get_data(self.url.dispatch_regionsum_url(str(intervals)))

    def get_dispatch_interconnectorres(self, intervals):
        """Returns data from dispatch_interconnectorres table from AEMO MMS data model.

        Inputs
            intervals: allows the user to define a trailing number of dispatch intervals.
        
        Output
            dispatch_interconnectorres: Dataframe of dispatch interconnector's indexed on the column settlementdate.
            Columns currently included: settlementdate, interconnectorid, mwflow, exportlimit, importlimit, exportgenconid, importgenconid.
            ** Note - users are limited to 10,000 rows at a time.
        """
        self.table_name = 'dispatch_interconnectorres'
        return self.__get_data(self.url.dispatch_interconnectorres_url(str(intervals)))

    def get_dispatch_price_historical(self, start_date, end_date, regionid='ALL'):
        """Returns data from dispatch_price table from AEMO MMS data model.

        Inputs
            start_date: Must be in ISOFORMAT "YYYY-MM-DD HH:MM:SS" as string
            end_date: Must be in ISOFORMAT "YYYY-MM-DD HH:MM:SS" as string
            regionid: allows the user to define a regionid within the NEM. 
                    QLD1, NSW1, VIC1, SA1, TAS1. 
                    Default as ALL.
        
        Output
            dispatch_price: Dataframe of dispatch prices indexed on the column settlementdate.
            Columns currently included: settlementdate, regionid, rrp.
            ** Note - users are limited to 10,000 rows at a time.
        """
        self.table_name = 'dispatch_price'
        start_date = timezone.localize(dt.datetime.fromisoformat(start_date)).timestamp()
        end_date = timezone.localize(dt.datetime.fromisoformat(end_date)).timestamp()
        return self.__get_data(self.url.dispatch_price_historical_url(start_date, end_date, regionid))
    
    def get_dispatch_regionsum_historical(self, start_date, end_date, regionid='ALL'):
        """Returns data from dispatch_regionsum table from AEMO MMS data model.

        Inputs
            start_date: Must be in ISOFORMAT "YYYY-MM-DD HH:MM:SS" as string
            end_date: Must be in ISOFORMAT "YYYY-MM-DD HH:MM:SS" as string
            regionid: allows the user to define a regionid within the NEM. 
                    QLD1, NSW1, VIC1, SA1, TAS1.
                    Default as ALL.
        
        Output
            dispatch_regionsum: Dataframe of dispatch regionsum indexed on the column settlementdate.
           Columns currently included: settlementdate, regionid, totaldemand, availablegeneration, totalintermittentgeneration, demand_and_nonschedgen, uigf.
            ** Note - users are limited to 10,000 rows at a time.
        """
        self.table_name = 'dispatch_regionsum'
        start_date = timezone.localize(dt.datetime.fromisoformat(start_date)).timestamp()
        end_date = timezone.localize(dt.datetime.fromisoformat(end_date)).timestamp()
        return self.__get_data(self.url.dispatch_regionsum_historical_url(start_date, end_date, regionid))
    
    def get_dispatch_interconnectorres_historical(self, start_date, end_date, connectorid='ALL'):
        """Returns data from dispatch_price table from AEMO MMS data model.

        Inputs
            start_date: Must be in ISOFORMAT "YYYY-MM-DD HH:MM:SS" as string
            end_date: Must be in ISOFORMAT "YYYY-MM-DD HH:MM:SS" as string
            connectorid: allows the user to define a connectorid within the NEM. 
                    N-Q-MNSP1, NSW1-QLD1, T-V-MNSP1, V-S-MNSP1, V-SA, VIC1-NSW1.
                    Default as ALL.
        
        Output
            dispatch_interconnectorres: Dataframe of dispatch interconnector's indexed on the column settlementdate.
            settlementdate, interconnectorid, mwflow, exportlimit, importlimit, exportgenconid, importgenconid.
            ** Note - users are limited to 10,000 rows at a time.
        """
        self.table_name = 'dispatch_interconnectorres'
        start_date = timezone.localize(dt.datetime.fromisoformat(start_date)).timestamp()
        end_date = timezone.localize(dt.datetime.fromisoformat(end_date)).timestamp()
        return self.__get_data(self.url.dispatch_interconnectorres_historical_url(start_date, end_date, connectorid))

    def get_trading_price(self, intervals):
        """Returns data from trading_price table from AEMO MMS data model.

        Inputs
            intervals: allows the user to define a trailing number of trading intervals.
        
        Output
            trading_price: Dataframe of trading prices indexed on the column settlementdate.
            Columns currently included: settlementdate, regionid, rrp.
            ** Note - users are limited to 10,000 rows at a time.
        """
        self.table_name = 'trading_price'
        return self.__get_data(self.url.trading_price_url(str(intervals)))

    def get_trading_regionsum(self, intervals):
        """Returns data from trading_regionsum table from AEMO MMS data model.

        Inputs
            intervals: allows the user to define a trailing number of trading intervals.
        
        Output
            trading_regionsum: Dataframe of trading regionsum indexed on the column settlementdate.
            Columns currently included: settlementdate, regionid, totaldemand, availablegeneration, totalintermittentgeneration, demand_and_nonschedgen, uigf.
            ** Note - users are limited to 10,000 rows at a time.
        """
        self.table_name = 'trading_regionsum'
        return self.__get_data(self.url.trading_regionsum_url(str(intervals)))

    def get_trading_interconnectorres(self, intervals):
        """Returns data from trading_interconnectorres table from AEMO MMS data model.

        Inputs
            intervals: allows the user to define a trailing number of trading intervals.
        
        Output
            trading_interconnectorres: Dataframe of trading interconnector's indexed on the column settlementdate.
            Columns currently included: settlementdate, interconnectorid, mwflow, exportlimit, importlimit, exportgenconid, importgenconid.
            ** Note - users are limited to 10,000 rows at a time.
        """
        self.table_name = 'trading_interconnectorres'
        return self.__get_data(self.url.trading_interconnectorres_url(str(intervals)))

    def get_trading_price_historical(self, start_date, end_date, regionid='ALL'):
        """Returns data from trading_price table from AEMO MMS data model.

        Inputs
            start_date: Must be in ISOFORMAT "YYYY-MM-DD HH:MM:SS" as string
            end_date: Must be in ISOFORMAT "YYYY-MM-DD HH:MM:SS" as string
            regionid: allows the user to define a regionid within the NEM. 
                    QLD1, NSW1, VIC1, SA1, TAS1. 
                    Default as ALL.
        
        Output
            trading_price: Dataframe of trading prices indexed on the column settlementdate.
            Columns currently included: settlementdate, regionid, rrp.
            ** Note - users are limited to 10,000 rows at a time.
        """
        self.table_name = 'trading_price'
        start_date = timezone.localize(dt.datetime.fromisoformat(start_date)).timestamp()
        end_date = timezone.localize(dt.datetime.fromisoformat(end_date)).timestamp()
        return self.__get_data(self.url.trading_price_historical_url(start_date, end_date, regionid))
    
    def get_trading_regionsum_historical(self, start_date, end_date, regionid='ALL'):
        """Returns data from trading_regionsum table from AEMO MMS data model.

        Inputs
            start_date: Must be in ISOFORMAT "YYYY-MM-DD HH:MM:SS" as string
            end_date: Must be in ISOFORMAT "YYYY-MM-DD HH:MM:SS" as string
            regionid: allows the user to define a regionid within the NEM. 
                    QLD1, NSW1, VIC1, SA1, TAS1.
                    Default as ALL.
        
        Output
            trading_regionsum: Dataframe of trading regionsum indexed on the column settlementdate.
           Columns currently included: settlementdate, regionid, totaldemand, availablegeneration, totalintermittentgeneration, demand_and_nonschedgen, uigf.
            ** Note - users are limited to 10,000 rows at a time.
        """
        self.table_name = 'trading_regionsum'
        start_date = timezone.localize(dt.datetime.fromisoformat(start_date)).timestamp()
        end_date = timezone.localize(dt.datetime.fromisoformat(end_date)).timestamp()
        return self.__get_data(self.url.trading_regionsum_historical_url(start_date, end_date, regionid))
    
    def get_trading_interconnectorres_historical(self, start_date, end_date, connectorid='ALL'):
        """Returns data from trading_price table from AEMO MMS data model.

        Inputs
            start_date: Must be in ISOFORMAT "YYYY-MM-DD HH:MM:SS" as string
            end_date: Must be in ISOFORMAT "YYYY-MM-DD HH:MM:SS" as string
            connectorid: allows the user to define a connectorid within the NEM. 
                    N-Q-MNSP1, NSW1-QLD1, T-V-MNSP1, V-S-MNSP1, V-SA, VIC1-NSW1.
                    Default as ALL.
        
        Output
            trading_interconnectorres: Dataframe of trading interconnector's indexed on the column settlementdate.
            settlementdate, interconnectorid, mwflow, meteredmwflow, mwlosses.
            ** Note - users are limited to 10,000 rows at a time.
        """
        self.table_name = 'trading_interconnectorres'
        start_date = timezone.localize(dt.datetime.fromisoformat(start_date)).timestamp()
        end_date = timezone.localize(dt.datetime.fromisoformat(end_date)).timestamp()
        return self.__get_data(self.url.trading_interconnectorres_historical_url(start_date, end_date, connectorid))