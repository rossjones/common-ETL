from collections import namedtuple

from openaddresses.downloaders.CH_download import download as ch_download
from openaddresses.downloaders.ONSPD_download import download as onspd_download
from openaddresses.downloaders.OS_Locator_download import download as os_download

from openaddresses.etl.CH_Bulk_Extractor import CHProcessor

PACKAGES = {
    'ch':    {'label': 'Companies House',
              'download': ch_download,
              'processor': CHProcessor },
    'onspd': {'label': 'ONSPD',
              'download': onspd_download,
              'processor': None},
    'os':    {'label': 'OS Locator',
              'download': os_download,
              'processor': None}
}