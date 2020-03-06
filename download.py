
import io
import os
import glob
import pandas as pd
import zipfile
import datetime as dt
from urllib.request import Request
from nsetools import Nse
from abc import ABCMeta, abstractmethod
from condate import mkdate, usable_date, get_date_range, from_date, to_date, DownloadPath


class Downloader(metaclass=ABCMeta):
    def __init__(self, to_date=dt.datetime.now().date(), skip_dates=[]):
        self.url = "https://www.nseindia.com/content/historical/EQUITIES/%s/%s/cm%s%s%sbhav.csv.zip"
        self.filename = "cm%s%s%sbhav.csv"
        self.skip_dates = skip_dates
        self.nse = Nse()
        self.dates = self.generate_dates()


    def generate_dates(self):
        return get_date_range(from_date, to_date, skip_dates=self.skip_dates)
    
    def get_copy_url(self, d):
        day_of_month = d.strftime("%d")
        mon = d.strftime("%b").upper()
        year = d.year
        url = self.url % (year, mon, day_of_month, mon, year)
        return url

    def get_copy_filename(self, d):
        day_of_month = d.strftime("%d")
        mon = d.strftime("%b").upper()
        year = d.year
        filename = self.filename % (day_of_month, mon, year)
        return filename

    def download_one(self, d):
        d = mkdate(d)
        url = self.get_copy_url(d)
        print(url)
        filename = self.get_copy_filename(d)
        response = self.nse.opener.open(Request(url, None, self.nse.headers))
        zip_file_handle = io.BytesIO(response.read())
        zf = zipfile.ZipFile(zip_file_handle)
        return zf.read(filename).decode("utf-8")

    @abstractmethod
    def download(self):
        pass 
    
    @abstractmethod
    def update(self):
        pass 

class Filedownloader(Downloader):
    def __init__(self, directory, *args, **kwargs):
        if (os.path.exists(directory) and os.path.isdir(directory) and os.access(directory, os.W_OK)):
            super().__init__(*args, **kwargs)
            self.directory = directory
        else:
            raise Exception("directory path must be valid and writtable, please check manually")

    def download(self):
        for date in self.dates:
            print("downloading for " + str(date))
            try:
                content = self.download_one(date)
            except Exception as err:
                print("unable to download for the date: %s" %  date.strftime("%Y-%m-%d"))
            else:
                fh = open(self.directory + "/" + date.strftime("%Y-%m-%d") + ".csv", "w")
                fh.write(content)
                fh.close()
    
    def update(self):
        pass 


    def mergecsv(self):
        os.chdir(DownloadPath)
        extension = 'csv'
        all_filenames = [i for i in glob.glob('*.{}'.format(extension))]
        combined_csv = pd.concat([pd.read_csv(f) for f in all_filenames ])
        combined_csv.to_csv( "combined_csv.csv", index=False, encoding='utf-8-sig')
        print("combined csv downloaded successfully...")


if __name__ == '__main__':
    b = Filedownloader(directory=DownloadPath)
    b.download()
    b.mergecsv()