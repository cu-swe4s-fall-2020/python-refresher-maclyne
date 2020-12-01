rule all:
	input: 'potential_BRAC_county_cases_timeseries.png', \
	       'potential_BRAC_county_cases_timeseries_with_racelabels.png'

rule make_Colorado_coviddata_file:
	input: 'covid-19-data/us-counties.csv'
	output: 'covid-19-data/Colorado-counties.csv'
	shell:
	'''
	python make_statefile_cases.py 'Colorado'
	'''

rule get_BRAC_allcountys_list:
	input: 'BRAC_races_permits.csv' #TODO: need to make this dataset myself
	output: 'BRAC_county_names_involving_permits.txt'
	shell:
	'''
	python BRAC_get_permit_data.py get_county_names_all \
		--file_name {input} \
		> 'BRAC_county_names_involving_permits.txt'
	'''

rule get_county_rates:
	input: 'covid-19-data/Colorado-counties.csv', 'BRAC_county_names_involving_permits.txt'
	output: 'potential_BRAC_county_cases.txt'
	shell:
	'''
	python get_rates.py \
		--state 'Colorado' \
		--coviddata_countys_list cat 'BRAC_county_names_involving_permits.txt' \
		> 'potential_BRAC_county_cases.txt'
	'''

rule make_timeseries:
	input: 'potential_BRAC_county_cases.txt'
	output: 'potential_BRAC_county_cases_timeseries.png'
	shell:
	'''
	python ss_plots/timeseries.py \
		--in_file {input} \
		--out_file {output} \
		--x_label 'Date' \
		--y_label 'Cases Per Capita (per 100,000 populaiton)'
		--height 3 \
		--width 7
	'''

rule get_race_points:
	input: 'potential_BRAC_county_cases.txt', 'BRAC_races_permits.csv'
	output: 'BRAC_countycases_at_races.csv'
	shell:
	'''
	python BRAC_get_permit_data.py BRAC_get_permit_data_with_caserates \
		--BRAC_county_caserates_file 'potential_BRAC_county_cases.txt'
		--BRAC_race_info_file 'BRAC_races_permits.csv'
	'''

rule add_race_markers_to_plot:
	input: 'potential_BRAC_county_cases_timeseries.png', 'BRAC_countycases_at_races.csv'
	output: 'potential_BRAC_county_cases_timeseries_with_racelabels.png'
	shell: #TODO

