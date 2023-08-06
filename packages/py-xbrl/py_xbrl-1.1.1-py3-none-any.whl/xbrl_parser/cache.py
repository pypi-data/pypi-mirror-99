"""
Downloads files and stores them locally.
"""
import time
import re
import os
import requests
import logging
import zipfile

logger = logging.getLogger(__name__)


class HttpCache:
    """
    This class handles a simple disk cache. It will download requested files and store them in folder specified by
    the user. If the file is requested a second time this class will serve the file directly from the file system.
    The path for caching is created out of the url of the file.
    For example, the file with the URL
    "https://www.sec.gov/Archives/edgar/data/320193/000032019318000100/aapl-20180630.xml"
    will be stored in the disk cache in
    „D:/cache/www.sec.gov/Archives/edgar/data/320193/000032019318000100/aapl-20180630.xml“
    where "D:/cache" is the caching directory specified by the user.

    The http cache can also delay requests. This is highly recommended if you download xbrl submissions in batch!

    The SEC also emphasizes that you should try to keep the required server load on the EDGAR system as small as possible!
    https://www.sec.gov/privacy.htm#security

    """

    def __init__(self, cache_dir: str, delay: int = 500):
        """
        :param cache_dir: Root directory of the disk cache (all requested files will be cached in this directory)
        :param delay: How many milliseconds should the cache wait, before requesting another file from the same server
        """
        # check if the cache_dir ends with a /
        if not cache_dir.endswith('/'): cache_dir += '/'
        self.cache_dir: str = cache_dir
        self.delay: int = delay

    def cache_file(self, file_url: str) -> str:
        """
        Caches a file in the http cache.

        @param file_url: absolute url to the file to be cached.
                    i.e: http://xbrl.fasb.org/us-gaap/2017/elts/us-gaap-2017-01-31.xsd
        @return: returns the absolute path to the cached file
        """
        file_path: str = self.url_to_path(file_url)
        # first check if the files
        if os.path.exists(file_path):
            return file_path

        file_dir_path: str = '/'.join(file_path.split('/')[0:-1])
        # try to download the file
        if not os.path.isdir(file_dir_path):
            os.makedirs(file_dir_path)
        query_response = requests.get(file_url)
        logger.info(str(query_response.status_code) + " " + file_url)

        # Set a timeout, so that we do not get blocked by the SEC servers for making to many requests
        time.sleep(self.delay / 1000)

        if not query_response.status_code == 200:
            if query_response.status_code == 404:
                raise Exception("Could not find file on {}".format(file_url, query_response.status_code))
            else:
                raise Exception(
                    "Could not download file from {}. Error code: {}".format(file_url, query_response.status_code))

        with open(file_path, "wb+") as file:
            file.write(query_response.content)
            file.close()

        return file_path

    def purge_file(self, file_url: str) -> bool:
        """
        Removes a file from the cache
        :param file_url: url to the file
            i.e: https://www.sec.gov/Archives/edgar/data/320193/000032019318000100/aapl-20180630.xml
        :return: true if the file was deleted, false if it could not be found
        """
        try:
            os.remove(self.url_to_path(file_url))
        except FileNotFoundError:
            return False
        return True

    def url_to_path(self, url: str) -> str:
        """
        Takes a url and converts it to the ABSOLUTE local cache path
        i.e https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd -> /xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd
        @param url:
        @return:
        """
        return self.cache_dir + re.sub("https?://", "", url)

    def cache_edgar_enclosure(self, enclosure_url: str) -> None:
        """
        The SEC provides zip folders that contain all xbrl related files for a given submission.
        These files are i.e: Instance Document, Extension Taxonomy, Linkbases.
        Due to the fact that the zip compression is very effective on xbrl submissions that naturally contain
        repeating test, it is way more efficient to download the zip folder and extract it.
        So if you want to do the SEC servers and your downloading time a favour, use this method for downloading
        the submission :).
        One way to get the zip enclosure url is through the Structured Disclosure RSS Feeds provided by the SEC:
        https://www.sec.gov/structureddata/rss-feeds-submitted-filings
        :param enclosure_url: url to the zip folder.
        :return:
        """
        if not enclosure_url.endswith('.zip'):
            raise Exception("This is not a valid zip folder")
        # download the zip folder and store it into the default http cache
        enclosure_path = self.cache_file(file_url=enclosure_url)
        submission_dir_path = self.url_to_path('/'.join(enclosure_url.split('/')[:-1]))
        # extract the zip folder
        with zipfile.ZipFile(enclosure_path, "r") as zip_ref:
            zip_ref.extractall(submission_dir_path)
            zip_ref.close()
