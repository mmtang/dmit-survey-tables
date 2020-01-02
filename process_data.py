'''

California State Water Resources Control Board (SWRCB)
Office of Information Management and Analysis (OIMA) 

Michelle Tang (michelle.tang@waterboards.ca.gov)
https://github.com/mmtang

'''

import csv
import os

# separate data into different files
# exclude all "other" columns - can build this out later
info_cols = ['wb_office', 'swrcb_division', 'swrcb_division_other', 'program', 'supervisor', 'suggestions', 'comments', 'submission_time']
interest_cols = ['training_interest', 'collect_data_interest', 'clean_data_interest', 'data_viz_interest', 'stats_interest', 'code_interest', 'ml_interest', 'excel_interest', 'access_interest', 'sql_interest', 'tableau_interest', 'powerbi_interest', 'arcgis_interest', 'python_interest', 'r_interest']
database_cols = ['ceden', 'ciwqs', 'ewrims', 'geotracker', 'smarts', 'water49']
frequency_cols = ['collect_data_freq', 'clean_data_freq', 'data_viz_freq', 'stats_freq', 'code_freq', 'ml_freq']
skill_cols = ['collect_data_skill', 'clean_data_skill', 'data_viz_skill', 'stats_skill', 'code_skill', 'ml_skill', 'excel_skill', 'access_skill', 'sql_skill', 'tableau_skill', 'powerbi_skill', 'arcgis_skill', 'python_skill', 'r_skill']

# location/name of data file
file_path = '1_SurveyResults_10-14-19.csv'

def check_null(val):
    if not val or val == 'NA' or val is None:
        return 'null'
    else: 
        return val

def get_columns(data, cols): 
    target_data = []
    for row in data:
        rec = {}
        rec['id'] = row['id']
        for d in cols:
            rec[d] = row[d]
        target_data.append(rec)
    return target_data


def load_data(file):
    with open(file, 'r', encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile)
        data = []
        # add index/id column
        for i, row in enumerate(reader, 1000):
            row['id'] = i
            data.append(row)
    return data

# arr is an array of the output column names, two values only with the 2nd being the response value. ex: ['subject', 'interest_level']
# column names should be descriptive based on the target file and what data is being written
def unpivot(data, arr, cols):
    unpivoted_data = []
    for row in data:
        for d in cols:
            rec = {}
            rec['id'] = row['id']
            rec[arr[0]] = d
            rec[arr[1]] = check_null(row[d])
            unpivoted_data.append(rec)
    return unpivoted_data

def write_csv(data, file_name):
    subfolder = 'output'
    if not os.path.exists(subfolder):
        os.mkdir(subfolder)
    ext = '.csv'
    sep = ','
    target_name = subfolder + '/' + file_name + ext
    keys = data[0].keys()
    with open(target_name, 'w', newline='') as f:
	    writer = csv.DictWriter(f, keys)
	    writer.writeheader()
	    writer.writerows(data)

if __name__ == '__main__':
    # load
    survey_data = load_data(file_path)
    # transform
    survey_data_trunc = get_columns(survey_data, info_cols)  # we don't need to write the entire dataset, extract a subset
    interest_data = unpivot(survey_data, ['subject', 'interest_level'], interest_cols)
    database_data = unpivot(survey_data, ['database', 'interaction'], database_cols)
    frequency_data = unpivot(survey_data, ['task', 'frequency'], frequency_cols)
    skill_data = unpivot(survey_data, ['subject', 'skill_level'], skill_cols)
    # write
    write_csv(survey_data_trunc, 'survey_data')
    write_csv(interest_data, 'interest_data')
    write_csv(database_data, 'database_data')
    write_csv(frequency_data, 'frequency_data')
    write_csv(skill_data, 'skill_data')
    