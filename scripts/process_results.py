"""Process the results of EnergyPlus analysis."""
import os
import pandas as pd
import sqlite3
import json


def sql_query(input_path, input_filename, report_name, table_name, row_name, column_name):

    query = 'SELECT Value from TabularDataWithStrings WHERE ReportName=\'' + report_name + '\''
    query += ' and TableName=\'' + table_name + '\''
    query += ' and ColumnName=\'' + column_name + '\''
    query += ' and RowName=\'' + row_name + '\''
    query += ';'

    con = sqlite3.connect(os.path.join(input_path, input_filename))

    #with con:
    cur = con.cursor()
    val = 0
    sql_ok = 'no'
    try:
        cur.execute('pragma integrity_check')
        data = cur.fetchall()
        for d in data:
            sql_ok = d[0] #, d[1], d[2]
    except:
        pass
    else:
        if sql_ok == 'ok':
            df = pd.read_sql_query(query, con)
            val = float(df.iloc[0]['Value'])
    finally:
        con.close()
    return val


# Inputs
input_path = '..\\raw_results'
output_path='..\\res'

# PROCESS SQL FILES
input_filenames = (f for f in os.listdir(input_path) if f.endswith(".sql"))

min_eui = 0.0
max_eui = 0.0

for input_filename in input_filenames:

    eui = sql_query(input_path, input_filename,
                    'AnnualBuildingUtilityPerformanceSummary',
                    'Site and Source Energy', 'Total Site Energy',
                    'Energy Per Total Building Area')  #MJ/m2

    cooling = sql_query(input_path, input_filename,
                        'AnnualBuildingUtilityPerformanceSummary',
                        'End Uses', 'Cooling', 'Electricity')  #GJ
    cooling += sql_query(input_path, input_filename,
                         'AnnualBuildingUtilityPerformanceSummary',
                         'End Uses', 'Cooling', 'District Cooling')

    heating = sql_query(input_path, input_filename,
                        'AnnualBuildingUtilityPerformanceSummary',
                        'End Uses', 'Heating', 'Electricity')  #GJ
    heating += sql_query(input_path, input_filename,
                         'AnnualBuildingUtilityPerformanceSummary',
                         'End Uses', 'Heating', 'Natural Gas')
    heating += sql_query(input_path, input_filename,
                         'AnnualBuildingUtilityPerformanceSummary',
                         'End Uses', 'Heating', 'District Heating')

    unmet_cooling_hours = sql_query(input_path, input_filename,
                                    'SystemSummary','Time Setpoint Not Met',
                                    'Facility', 'During Occupied Cooling')
    unmet_heating_hours = sql_query(input_path, input_filename,
                                    'SystemSummary', 'Time Setpoint Not Met',
                                    'Facility', 'During Occupied Heating')

    lighting_power_density = sql_query(input_path, input_filename,
                                       'LightingSummary', 'Interior Lighting',
                                       'Interior Lighting Total',
                                       'Lighting Power Density')


    # read daylight factor data
    # Based on my understanding this is totally wrong. For now I set all the values
    # to 0.25 until we get it fixed.
    dlf = 0.25

    # if os.path.exists(os.path.join(input_path, os.path.splitext(input_filename)[0] + '.res')):
    #     rad_data = pd.read_csv(
            # os.path.join(input_path, os.path.splitext(input_filename)[0] + '.res'),
            # sep='\t', lineterminator='\n', header=None, usecols=[0])
    #     series_size = rad_data.size
    #     dlf = float(rad_data[0][rad_data[0]>0.2].count())/series_size
    # else:
    #     rad_data = None
    #     dlf = 0.25


    min_eui = min(eui, min_eui)
    max_eui = max(eui, max_eui)

    case_dict = {
        'eui': eui,
        'cooling': cooling,
        'heating': heating,
        'unmet_cooling_hours': unmet_cooling_hours,
        'unmet_heating_hours': unmet_heating_hours,
        'lighting_power_density': lighting_power_density,
        'daylight_factor': dlf
        #'sensible heat gain summary'
    }

    with open(os.path.join(output_path, input_filename[:-4] + '.json'), 'w') as outfile:
        json.dump(case_dict, outfile)

    # print('')
    # print('EUI: ' + str(eui)
    # print('Min EUI: ' + str(min_eui))
    # print('Max EUI: ' + str(max_eui))
    # print('')
