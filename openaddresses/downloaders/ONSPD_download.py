import datetime
import os
import sys
import traceback
import urllib2
import zipfile

def download(target_path):

    releases = [
        'NOV',
        'AUG',
        'MAY',
        'FEB'
    ]

    year = datetime.datetime.now().year

    file = None
    release_name = None
    while file == None:
        for release in releases:
            url = "https://geoportal.statistics.gov.uk/Docs/PostCodes/ONSPD_{0}_{1}_csv.zip".format(release,year)
            try:
                release_name = "ONSPD_{0}_{1}".format(release,year)
                file = urllib2.urlopen(url)
                break
            except:
                None
        year -= 1

    if not release_name:
        print "Could not find a release"
        sys.exit(1)

    print "Downloading ", release_name

    output_filename = os.path.join(target_path, release_name + "_csv.zip" )
    output = open(output_filename,'wb')
    output.write(file.read())
    output.close()

    with zipfile.ZipFile(output_filename, 'r') as datazip:
        file = datazip.open("Data/{0}_UK.csv".format(release_name))

        write_to = os.path.join(target_path, release_name + ".csv")
        output = open(write_to, 'wb')
        output.write(file.read())
        output.close()

    if os.path.exists(output_filename):
        os.remove(output_filename)