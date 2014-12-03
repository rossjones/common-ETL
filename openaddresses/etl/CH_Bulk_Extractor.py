#
# Open addresses Companies House ETL Library
# Open addresses Companies House ETL tool
#
#
# Version       1.0 (Python) in progress
# Author        John Murray
# Licence       MIT
#
# Purpose       Bulk extract of addresses from Companies House Data
#

import csv
import glob
import sys
import json
import datetime
import time
import urllib
import urllib2
import MySQLdb
import collections

from openaddresses.lib.postcode_class import *
from openaddresses.lib.address_lines import *

from openaddresses.etl import Processor

class CHProcessor(Processor):

    def process(self):
        # Read api configuration from config file
        apiurl = self.config.get('api', 'url')
        apitoken = self.config.get('api', 'token')

        # Read database configuration from config file
        username = self.config.get('database', 'username')
        password = self.config.get('database', 'password')
        hostname = self.config.get('database', 'hostname')
        database = self.config.get('database', 'database')

        try:
            self.dbConn = MySQLdb.connect(host=hostname,user=username,passwd=password,db=database)
            self.cursor = self.dbConn.cursor()
            self.address_lines = AddressLines(self.cursor)

            self.town_path = os.path.join(data_folder, 'CompanyTowns.txt')

            with open(town_path, 'wb') as csvout:
                companywriter = csv.writer(csvout, delimiter=',',quotechar='"', quoting=csv.QUOTE_MINIMAL)
                companywriter.writerow(['Postcode', 'Town', 'Sector', 'Aons'])

                for file in glob.glob(os.path.join(data_folder, "Basic*.csv")):
                    self.process_file(file)
        except Exception, e:
            print e

    def storeAddresses(self, out):
        # Error timeout parameters
        max_tries = 100                         # Maximum number of retries
        wait_min = 1                            # First wait time (seconds)
        wait_increment = 5                      # Wait time increment (seconds)

        if len(out['addresses']) > 0:                # Check there is data to write
            data = json.dumps(out, indent=1)
            headers = { 'ACCESS_TOKEN' : apitoken, 'Content-Type': 'application/json' }
            url = apiurl
            req = urllib2.Request(url, data, headers)
            ntries = 0
            while ntries < max_tries:
                try:
                    response = urllib2.urlopen(req)
                    the_page = response.read()
                    time.sleep(2)
                    break
                except urllib2.HTTPError as e:
                    time.sleep(wait_min + wait_increment * ntries)
                    ntries += 1
                    err = e
                    print "Warning - Ingester API HTTP Error encountered - retrying ("+str(ntries)+"): " + str(e.code) + " - " + e.reason
                except urllib2.URLError as e:
                   sys.exit("Fatal error - Ingester API URL Error: " + str(e.code) + " - " + e.reason)
            if ntries >= max_tries:
                sys.exit ("Fatal error - Ingester API HTTP Error max tries reached ("+str(ntries)+")")

    def _fill_address(self, pc):
        # Future code for inference - not active in alpha
        # try:
        #    companywriter.writerow([pc.getPostcode("S"), self.address_lines.getTown(), pc.getSector("S")])
        # except:
        #     print row
        #    sys.exit("Sector failure")
        self.address_lines.getStreet()
        self.address_lines.getAons()
        address = collections.OrderedDict()
        address['address'] = self.address_lines.elements
        address['address']['postcode'] = collections.OrderedDict()
        address['address']['postcode']['name'] = pc.getPostcode("S")
        address['address']['postcode']['geometry'] = collections.OrderedDict()
        address['address']['postcode']['geometry']['type'] = 'Point'
        address['address']['postcode']['geometry']['coordinates'] = [pc.centroid[1], pc.centroid[0]]
        # Next line for future use for inference
        # out['address']['sector'] = pc.getSector("S")
        address['provenance'] = {}
        address['provenance']['executed_at'] = datetime.datetime.today().strftime("%Y-%m-%dT%H:%M:%SZ")
        address['provenance']['url'] = "http://download.companieshouse.gov.uk/en_output.html"
        address['provenance']['filename'] = file
        address['provenance']['record_no'] = str(nrecs)
        return address

    # Process a single file
    def process_file(self, file):
        start_time = time.time()
        print file
        nrecs = 0

        # Load CSV file
        with open(file, 'rb') as csvfile:
            companyreader = csv.DictReader(csvfile, delimiter=',', quotechar='"')
            companyreader.fieldnames = [field.strip() for field in companyreader.fieldnames]

            out = {}                            # Reset output buffer
            out['addresses'] = []

            for row in companyreader:
                nrecs += 1
                if row.get('RegAddress.PostCode'): # Checks for presence and non-empty value
                    pc = Postcode(row['RegAddress.PostCode'], self.cursor)
                    if pc.current != -1:
                        lines = [row['RegAddress.AddressLine1'],
                                 row['RegAddress.AddressLine2'],
                                 row['RegAddress.PostTown'],
                                 row['RegAddress.County']]
                        self.address_lines.setAddress(lines,pc)

                        if self.address_lines.getTown():
                            out['addresses'].append(self._fill_address(pc))

                if (nrecs % 100) == 0:          # Buffer full - send records to API
                    print "Records read: " + str(nrecs)
                    elapsed = time.time() - start_time
                    print str(elapsed) + " secs elapsed"
                    print str((60 * nrecs) / elapsed) + " recs/min"
                    self.storeAddresses(out)         # Write records in buffer to API
                    out = {}                    # Reset output
                    out['addresses'] = []

            print "Records read: " + str(nrecs)
            elapsed = time.time() - start_time
            print str(elapsed) + " secs elapsed"
            print str((60 * nrecs) / elapsed) + " recs/min"
            self.storeAddresses(out)                 # Write remaining records in buffer

