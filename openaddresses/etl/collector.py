#
# Open addresses Common ETL Library
# Open addresses Collect Raw Data
#
#
# Version       1.0 (Python) in progress
# Author        John Murray
# Licence       MIT
#
# Purpose       Script to Colect Bulk Open Data feeds
#

import ConfigParser
import urllib
import urllib2
import zipfile
import MySQLdb
import fnmatch
import time

from openaddresses.lib.extractor import LinkExtractor
from openaddresses.etl import Processor

class Collector(Processor):

    def process(self):
        username = self.config.get('database', 'username')
        password = self.config.get('database', 'password')
        hostname = self.config.get('database', 'hostname')
        database = self.config.get('database', 'database')

        self.dbConn = MySQLdb.connect(host=hostname,user=username,passwd=password,db=database)
        self.cursor = dbConn.cursor()

        sources = config.get('sources', 'sources').split(",")

        for s in sources:
            url = config.get(s, 'url')
            filemask = config.get(s, 'filemask')
            filetype = config.get(s, 'filetype')
            if config.has_option(s, 'get'):
                fileget = config.get(s, 'get')
            else:
                fileget = "all"
            self.collectData(url,filemask,filetype,fileget)

        self.dbConn.close()

    def collectData(self,url,filemask,filetype,fileget):

        opener = urllib2.build_opener()
        opener.addheaders = [('User-agent', 'Mozilla/5.0')]

        response = opener.open(url)
        html = response.read()

        parser = LinkExtractor()
        parser.setPattern(url,filemask,filetype)
        parser.feed(html)

        links = parser.links

        files = []
        latest = 0

        for l in links:
            response = urllib2.urlopen(l)
            meta = response.info()
    #       modtime = time.strftime('%Y-%m-%d %H:%M:%S',time.strptime(meta['Last-Modified'],"%a, %d %b %Y %H:%M:%S %Z"))
            modtime = time.strptime(meta['Last-Modified'],"%a, %d %b %Y %H:%M:%S %Z")
            files.append([l,meta['Content-Length'],modtime])
            if modtime > latest:
                latest = modtime

        for f in files:
            file = f[0][f[0].rfind("/")+1:]
            query = "SELECT * FROM `Files` WHERE `fileurl`='"+f[0]+"' AND `size`='"+f[1]+"' AND `modtime`='"+time.strftime('%Y-%m-%d %H:%M:%S',f[2])+"';"
            self.cursor.execute(query)
            if self.cursor.rowcount == 0:
                if fileget == 'all' or (fileget == 'latest' and f[2] >= latest):
                    print "Downloading: "+f[0]
                    print urllib.urlretrieve(f[0], file)
                    query = "INSERT INTO `Files`(`fileurl`, `size`, `modtime`) VALUES ('"+f[0]+"','"+f[1]+"','"+time.strftime('%Y-%m-%d %H:%M:%S',f[2])+"')"
                    self.cursor.execute(query)
                    self.dbConn.commit()
                    if filetype.lower() == 'zip':
                        print "Unzipping: "+file
                        with zipfile.ZipFile(file, "r") as z:
                            z.extractall()
                else:
                    print "Not latest: "+f[0]
            else:
                print "Unchanged: "+f[0]


