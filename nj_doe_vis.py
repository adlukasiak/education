import requests
import pandas as pd
import matplotlib.pyplot as plt

csv_filename_map = {
	'advertised_enrollments': 'ENROLL',
	'advertised_revenues': 'REV',
	'advertised_appropriations': 'APPROP',
	'advertised_recapitulation_of_balance' : 'RECAP',
	'advertised_per_pupil_post_calculations': 'PUPCST',
	'unusual_revenues_and_appropriations': 'SD5',
	'shared_services': 'SD21',
	'estimated_tax_rate_information': 'SD22',
	'advertised_blended_resource_sbb_statement ': 'SCHAPP',
	'administrative_salaries': 'SD17'
	}

years = ['08', '09', '10', '11', '12']

all_tables = {}  # empty dict

for table_name in csv_filename_map.keys():
	dfs = []
	for year in years:
		url = 'http://www.state.nj.us/education/finance/fp/ufb/20%s/download/%s%s.CSV' % \
			(year, csv_filename_map[table_name], year)

		# quick hack for 2012
		if year == '12':
			url = url.replace('.CSV', '_FINAL.CSV').replace('2012/download', 'download')

		print 'URL ->', url
		try:
			df = pd.read_csv(url, skiprows=2)
			df['year'] = '20'+year
			dfs.append(df)
		except:  # certain data is available only after 2010 (other errors should be handled better)
			print '!ERROR on URL ->', url
	all_tables[table_name] = pd.concat(dfs)
		# requests.get(url)

# Now, let's do an example (albeit meaningless) plot
all_tables['administrative_salaries']['BASE_SAL'].plot()
plt.show()