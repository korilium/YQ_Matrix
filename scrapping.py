
import requests, os

#download zipfile 
url = "https://ec.europa.eu/eurostat/estat-navtree-portlet-prod/BulkDownloadListing?sort=1&downfile=comext/COMEXT_DATA/PRODUCTS/full198801.7z"
filename = os.path.basename(url)
response = requests.get(url, stream=True)

if response.status_code == 200:
    with open(filename, 'wb') as out:
        out.write(response.content)
else:
    print('Request failed: %d' % response.status_code)


#convert to dat file 
import py7zr
with py7zr.SevenZipFile("full198801.7z", 'r') as archive:
    archive.extractall(path="C:/Users/ide/Documents/GitHub/YQ_Matrix")
    
#convert dat file to list to csv to pandas 
with open(r"full198801.dat") as datFile: 
   test = [data.split()[0] for data in datFile]
   
def Convert(string):
    li = list(string.split(","))
    return li

list = [Convert(item) for item in test]

import pandas as pd 
df = pd.DataFrame(list[1:], columns=[list[0]])
final_df = df.drop(['PRODUCT_BEC'], axis=1,)

final_df.to_csv("output.dat", sep = "|")
