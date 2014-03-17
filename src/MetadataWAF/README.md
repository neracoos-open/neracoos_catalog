## run_nciso.py 

a python 2.7 utility to run ncISO from the command line and clean up and rename the resulting xml file names.

ncISO is a THREDDS catalog web crawler  which creates ISO-19115-2 xml metdata files for use in web accessible folders. (WAFS)

For usage and to download the ncISO-2.3.jar [go to the ncISO Home page](http://www.ngdc.noaa.gov/eds/tds/)


```
  run_nciso.py -h
  usage: run_nciso.py [-h] [-r] [-dr] [-v] [waf_dir] [tds_url]
  positional arguments:
    waf_dir             Output WAF directory. Default: /var/www/htdocs/WAF
    tds_url             THREDDS url to parse. Default:
                      http://thredds.ucar.edu/thredds/idd/obsData.xml
  optional arguments:
    -h, --help          show this help message and exit
    -r, --rename        Do not run ncISO. Just rename the xml files in the WAF.
    -dr, --dont_rename  Do not rename the xml files in the WAF.
    -v, --verbose       Verbose.

```
