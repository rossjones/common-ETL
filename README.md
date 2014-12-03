common-ETL
==========
This repository is about Open Addresses' "common ETL" and "Companies House ETL" modules. Read about them [here](http://openaddressesuk.org/docs), find detail in [this repository's wiki](https://github.com/OpenAddressesUK/common-ETL/wiki), or learn about Open Addresses in general [here](http://openaddressesuk.org). 

## Installation

You will need python-virtualenv installed ```pip install python-virtualenv``` but [virtualenv_wrapper](https://virtualenvwrapper.readthedocs.org/en/latest/) is preferable.

```bash

virtualenv . --no-site-packages
. bin/activate
#or if you have virtualenvwrapper
mkvirtualenv openaddresses


git clone https://github.com/rossjones/common-ETL.git
cd common-ETL
python setup.py develop

# Make changes to config file ....
# TODO: Document and specify to etl command

# List all the known packages
etl list
# Download the CH data
etl download ch
# Process the ch data
etl process ch 

```


##Licence
This code is open source under the MIT license. See the LICENSE.md file for full details.
