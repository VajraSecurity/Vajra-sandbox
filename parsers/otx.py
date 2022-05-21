#!/usr/bin/env python3
# this script for Sample validation from OTX

import json
from OTXv2 import OTXv2
from OTXv2 import IndicatorTypes
import json
import argparse

otx = OTXv2("OTX-API")
parser = argparse.ArgumentParser(description='OTX CLI script:  @anir0y')
parser.add_argument('-i', '--ip', help='IP eg; 4.4.4.4', required=False)
parser.add_argument(
    '-m', '--md5', help='MD5 Hash of a file eg; 7b42b35832855ab4ff37ae9b8fa9e571', required=False)

args = vars(parser.parse_args())

if args["ip"]:
    print (str(otx.get_indicator_details_full(IndicatorTypes.IPv4, args["ip"])))

if args["md5"]:
    print (str(otx.get_indicator_details_full(IndicatorTypes.FILE_HASH_MD5, args["md5"])))


#todo:
# parse logs with json and fetch only important data