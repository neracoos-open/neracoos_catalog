#! /usr/bin/env python
import os
import sys
import glob
import shutil
import argparse
from subprocess import call
from datetime import datetime
"""
 - Run java ncISO-2.3.jar to harvest and parse a THREDDS Catalog end point.
      (ncISO homepage and jar download: http://www.ngdc.noaa.gov/eds/tds/ )
 -  Use the -waf option to put all files into a single WAF Directory where 3 subdirs are created.
      /iso  xml ISO19115-2 metadata files
      /score  html ACDD Rubric scores
      /nciso  a log file
  @args
  Required but with defaults.
    - waf_dir where to put ncISO the results. WAF relative to the current diretory. ncISO will create it.
    - thredds catalog url (.xml) Default is the NERACOOS TDS.
  Optional
    --verbose
    --rename  Don't run ncISO, just rename files in an existing WAF
    --dont_rename  Don't run rename files in the WAF
  
    There is also a new_name() function to rename the files to simpler form. 

Eric Bridger: ebridger@gmri.org
"""

# RESET THESE
tds_url = 'http://thredds.ucar.edu/thredds/idd/obsData.xml'
waf_dir = '/var/www/htdocs/WAF'

# how many TDS datasets to find. Use 1 for testing 
nciso_num = '1'

###############################################
# Fix up WAF files names created by ncISO based on the TDS catalog
# From: <waf_dir>/iso/thredds_dodsC_UMO_DSG_SOS_A01_Aanderaa_HistoricRealtime_Agg.ncml.xml
# To: A01_Aanderaa_HistoricRealtime_Agg.xml
###############################################
def new_name(fn, part_rm_cnt):

  # save the waf_dir
  dn =  os.path.dirname(fn)
  # fix up the file name
  bn = os.path.basename(fn)
  # remove the .ncml.xml in file Agg.ncml.xml. The ncml is due to the TDS / ncSOS aggrgation caching bug
  bn = bn.replace(".ncml", '')

  parts = bn.split('_')
  # Already renamed these files.
  if parts[0] != 'thredds':
    sys.stderr.write("Already renamed: " + fn + "\n")
    return fn
  # get rid of leading parts
  for _ in range(part_rm_cnt):
    parts.pop(0)
  new_name = dn + '/' +  "_".join( parts )
  return new_name
###############################################

parser = argparse.ArgumentParser()
parser.add_argument("waf_dir", nargs="?", help="Output WAF directory. Default: " + waf_dir, default=waf_dir)
parser.add_argument("tds_url", nargs="?", help="THREDDS url to parse. Default: " + tds_url, default=tds_url)
parser.add_argument("-r", "--rename", action="store_true",  help="Don't run ncISO. Just rename the xml files in the WAF.")
parser.add_argument("-dr", "--dont_rename", action="store_true",  help="Don't rename the xml files in the WAF.")
parser.add_argument("-v", "--verbose", action="store_true",  help="Verbose.")
args = parser.parse_args()

tds_url = args.tds_url
waf_dir = args.waf_dir

if args.verbose:
  print "tds_url:", tds_url
  print "waf_dir: ",  waf_dir
  print "rename: ", args.rename
  print "dont_rename: ",  args.dont_rename

sdt = datetime.now()

if not args.rename:
  if args.verbose:
    print "Starting ncISO-2.3 TDS crawler"

  # with the -waf option a waf_dir is created with 3 subirs. iso/ score/ ncml/
  # num set to 1 for testing
  cmd_list = ['/usr/bin/java', '-Xms1024m', '-Xmx1024m', '-jar', 'ncISO-2.3.jar', '-ts', tds_url, '-num',  nciso_num, '-depth',  '20', '-iso', 'true', '-waf', waf_dir]

  ret = call(cmd_list)
  if ret:
    print "NCISO Error: ", ret
    exit()
    
  if args.verbose:
    print "ncISO Done:", ret
# end if not args.rename only

if not args.dont_rename:
  # Rename the ISO files
  for file in glob.iglob(waf_dir + '/iso/thredds_*.xml'):
    new_file = new_name(file, 5)
    if args.verbose:
      print file                                      
      print "\t", new_file                                      
    shutil.move(file, new_file)

  # Rename the score files
  for file in glob.iglob(waf_dir + '/score/thredds_*.html'):
    new_file = new_name(file, 5)
    if args.verbose:
      print file                                      
      print "\t", new_file                                      
    shutil.move(file, new_file)
# end if dont_rename

edt = datetime.now()

if args.verbose:
  print 'Start: ' + sdt.isoformat()
  print 'End: ' + edt.isoformat()

