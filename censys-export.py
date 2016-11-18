import censys.export
import configparser
import urllib.request
import shutil
import sys

config = configparser.ConfigParser()
config.read("keys.ini")
CENSYS_API_ID = (config['SectionOne']['CENSYS_API_ID'])
CENSYS_API_KEY = (config['SectionOne']['CENSYS_API_KEY'])
nrOfResults = 0
path_outputfile = 'outputfiles/censys/censys.json'
asn = -1
valid_asn = False

while not valid_asn:
    asn = input("Enter ASN:")
    if asn.isnumeric():
        asn = int(asn)
        if 0 <= asn <= 4294967295:
            valid_asn = True

c = censys.export.CensysExport(api_id=CENSYS_API_ID, api_secret=CENSYS_API_KEY)

query = "select * from ipv4.20161112 where autonomous_system.asn = 1104" + 'limit 1'
# Start new Job
res = c.new_job(query)
job_id = res["job_id"]

result = c.check_job_loop(job_id)

if result['status'] == 'success':
    for path in result['download_paths']:
        with urllib.request.urlopen(path) as response, open(path_outputfile, 'wb') as out_file:
            shutil.copyfileobj(response, out_file)
            print('Got file from URL: ' + response.geturl())
else:
    print('Censys job failed.' + '\n' + str(result))
