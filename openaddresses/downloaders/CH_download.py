import urllib2
import zipfile
import os


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
        file = urllib2.urlopen(url)

        target_out =os.path.join(target_folder, filename)
        output = open(target_out,'wb')
        output.write(file.read())
        output.close()
        with zipfile.ZipFile(target_out, 'r') as datazip:
            datazip.extractall()
        os.remove(target_out)
