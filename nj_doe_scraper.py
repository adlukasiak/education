# -*- coding: utf-8 -*-

import requests
import pandas as pd
import matplotlib.pyplot as plt
import re

# to get the base url for each year


def year_url(year):
    if year == 2012:
        url = 'http://www.state.nj.us/education/finance/fp/ufb/download/'
    else:
        url = 'http://www.state.nj.us/education/finance/fp/ufb/%s/download/' % year
    return url

# fishing out the csv file name and the dataset_type from the HTML
# dynamically creates the matrix [year,url,file name,dataset type]


def csv_files():
    csv_files = []
    for year in range(2008, 2013):  # data is available only for 2008-2012, but at one point 2013 will be published.  May want to test the upper range based on current year
        url = year_url(year)
        page = requests.get(url).content
        # csv_files[ year ] = re.findall("=\"(.+.CSV)", page)
        links = re.findall(r"<a.*?\s*href=\"(.*?)\".*?>(.*?)</a>", page)
                           #got all the links on the page, but need only CSV
        for csv_file, dataset_type in links:
            if 'CSV' in csv_file:
                csv_files.append(
                    (year, url + csv_file, csv_file, dataset_type))
    return csv_files

x = csv_files()
print x

# The real thing here:  getting contents of the cvs files for all of NJ since 2008 to 2012
# each csv file contains headers that are mapped to decription in the
# layout files.  It's worth linking the two at some point
all_tables = {}
for year, url, csv_file, dataset_type in x:
    dfs = []
    try:
        df = pd.read_csv(url, skiprows=2)
        df['year'] = year
        dfs.append(df)
    except:
        print '!ERROR on URL ->', url
    all_tables[dataset_type] = pd.concat(dfs)

# let's see what we got here...
print all_tables.keys()

# a silly plot to test the data frame
# the enr1 maps to "10/15/06 Actual Enrollment" in the Layout file
all_tables['Advertised Enrollments']['ENR1'].plot()
plt.show()  # required for non-IPython notebook environments
