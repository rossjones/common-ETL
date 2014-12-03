import urllib2

def download(target_folder):
    filenames = [
        "OS_Locator2014_2_OPEN_xaa.txt",
        "OS_Locator2014_2_OPEN_xab.txt",
        "OS_Locator2014_2_OPEN_xac.txt",
        "OS_Locator2014_2_OPEN_xad.txt"
    ]

    for filename in filenames:
        print "Downloading {}".format(filename)
        try:
            url = "http://openaddressesuk.org/OS_Locator/" + filename
            file = urllib2.urlopen(url)
            output = open(os.path.join(target_folder, filename),'wb')
            output.write(file.read())
            output.close()
        except Exception, e:
            print "Failed to download", e