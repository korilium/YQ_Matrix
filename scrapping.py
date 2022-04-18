
from nis import maps
import requests, os, py7zr
from datetime import datetime
import pandas as pd 
#download zipfile 

dates = pd.date_range(start="2021-01-01", periods= 12,  freq="M")

months = dates.strftime("%Y%m")

for month in months: 
    url = "https://ec.europa.eu/eurostat/estat-navtree-portlet-prod/BulkDownloadListing?sort=1&downfile=comext/COMEXT_DATA/PRODUCTS/full" + month + ".7z"
    filename = "import/zip/"+os.path.basename(url)
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(filename, 'wb') as out:
            out.write(response.content)
    else:
        print('Request failed: %d' % response.status_code)
        #convert to dat file 
    with py7zr.SevenZipFile("import/zip/full"+month+".7z", 'r') as archive:
        archive.extractall(path="C:/Users/ide/Documents/GitHub/YQ_Matrix-1/import/dat/")
            #convert dat file to list to csv to pandas 
    with open(r"import/dat/full"+month+".dat") as datFile: 
        test = [data.split()[0] for data in datFile]
    def Convert(string):
        li = string.split(",")
        return li
    test1 = [Convert(i) for i in test]
    df = pd.DataFrame(test1[1:], columns=[test1[0]])
    final_df = df.drop(['PRODUCT_BEC'], axis=1,)
    final_df.to_csv("export/nc"+month+".dat", sep = "|")
