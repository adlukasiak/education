# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

import requests
import pandas as pd

# <codecell>

# to get the base url for each year
def get_year_url( year ) :
    if year == 2012:
        url = 'http://www.state.nj.us/education/finance/fp/ufb/download/'
    else:    
        url = 'http://www.state.nj.us/education/finance/fp/ufb/%s/download/' % year
    return url    

# <codecell>

import re

# fishing out the csv file name and the dataset_type from the HTML
# dynamically creates the matrix [year,url,file name,dataset type]
def get_csv_files() :
    csv_files = []
    for year in range(2008,2013) :  # data is available only for 2008-2012, but at one point 2013 will be published.  May want to test the upper range based on current year
        url = get_year_url( year )
        page = requests.get(url).content
        #csv_files[ year ] = re.findall("=\"(.+.CSV)", page)
        links = re.findall(r"<a.*?\s*href=\"(.*?)\".*?>(.*?)</a>", page) #got all the links on the page, but need only CSV
        for link in links: 
            if 'CSV' in link[0]:
                csv_file = link[0]
                dataset_type = link[1]
                csv_files.append( [year, url+csv_file, csv_file, dataset_type] )
    return csv_files

# <codecell>

x = get_csv_files()
print x

# <codecell>

# The real thing here:  getting contents of the cvs files for all of NJ since 2008 to 2012
# each csv file contains headers that are mapped to decription in the layout files.  It's worth linking the two at some point
all_tables = {}
for row in x:
    year = row[0]
    url = row[1]
    dataset_type = row[3]
    dfs=[]
    try:
        df = pd.read_csv(url, skiprows=2)
        df['year'] = year
        dfs.append(df)
    except:
        print '!ERROR on URL ->', url
    all_tables[dataset_type] = pd.concat(dfs)

# <codecell>

# let's see what we got here...
all_tables.keys()  

# <codecell>

# a silly plot to test the data frame
# the enr1 maps to "10/15/06 Actual Enrollment" in the Layout file
all_tables['Advertised Enrollments']['enr1'].plot()

# <codecell>


