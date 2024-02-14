import requests
import yaml
import pandas as pd
from pprint import pprint

########## Task 1 ##########

studiesID = 201

with open('api_key.yml', 'r') as f:
    config = yaml.safe_load(f)

response = requests.get(url=f'https://osdr.nasa.gov/osdr/data/osd/files/{studiesID}?api_key={config["NASA_Key"]}')

# parse json
response_json = response.json()
pprint(response_json)

# create data frame from json
studiesPD = pd.DataFrame(response_json['studies'][f'OSD-{studiesID}']['study_files'])

studiesByOrg = studiesPD.groupby('organization').agg(Num_of_Studies_Per_Organization=('file_name', 'count'))
print('\n\n\nNumber of Studies Per Organization\n')
print(studiesByOrg)

studiesByCat = studiesPD.groupby('category').agg(Num_of_Studies_Per_Categlory=('file_name', 'count'))
print('\n\n\nNumber of Studies Per Category\n')
print(studiesByCat)

studiesBySubCat = studiesPD.groupby('subcategory').agg(Num_of_Studies_Per_Subcateglory=('file_name', 'count'))
print('\n\n\nNumber of Studies Per Subcategory\n')
print(studiesBySubCat)
