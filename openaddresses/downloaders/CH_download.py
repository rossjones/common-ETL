import os
import zipfile

import requests

def download(target_folder):
    filenames = [
        'BasicCompanyData-2014-11-01-part1_5.zip',
        'BasicCompanyData-2014-11-01-part2_5.zip',
        'BasicCompanyData-2014-11-01-part3_5.zip',
        'BasicCompanyData-2014-11-01-part4_5.zip',
        'BasicCompanyData-2014-11-01-part5_5.zip'
    ]

    for filename in filenames:
        print "Downloading {}".format(filename)
        url = 'http://download.companieshouse.gov.uk/' + filename
        target_out = os.path.join(target_folder, filename)

        # Stream directly to the file in 4k chunks. Lower memory usage
        # and should be faster too.
        req = requests.get(url, stream=True)
        with open(target_out, 'wb') as f:
            for chunk in req.iter_content(chunk_size=4096):
                if chunk:
                    f.write(chunk)
                    f.flush()

        with zipfile.ZipFile(target_out, 'r') as datazip:
            datazip.extractall(target_folder)
        os.remove(target_out)
