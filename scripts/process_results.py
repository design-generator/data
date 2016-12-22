
import os
import csv
import pandas as pd
import sqlite3
import json


# Inputs
input_path='results'
output_path='C:\\Users\\jmcneill\\Documents\\GitHub\\design-generator-data\\res'

def sql_query(input_path, input_filename, report_name, table_name, row_name, column_name):
    #print(input_filename)
    
    sql_query = 'SELECT Value from TabularDataWithStrings WHERE ReportName=\'' + report_name + '\''
    #sql_query += ' and ReportForString=\'' + report_for_string + '\''
    sql_query += ' and TableName=\'' + table_name + '\''
    sql_query += ' and ColumnName=\'' + column_name + '\''
    sql_query += ' and RowName=\'' + row_name + '\''
    sql_query += ';'
    #print sql_query

    con = sqlite3.connect(os.path.join(input_path, input_filename))

    #with con:
    cur = con.cursor()    
    try:
        cur.execute('pragma integrity_check')
        data = cur.fetchall()
        #print(data)
        for d in data:
            sql_ok = d[0]#, d[1], d[2]
    except:
        sql_ok = 'no'
    
    if sql_ok == 'ok':
        df = pd.read_sql_query(sql_query, con)
        val = float(df.iloc[0]['Value'])
    else:
        val = 0
    con.close()
    
    return val

# PROCESS SQL FILES
input_filenames = []
for file in os.listdir(input_path):
    if file.endswith(".sql"):
        input_filenames.append(file)

#print(input_filenames)
bad_sql_files = []
#['00000010033333300300000.sql', '00000010033333300300001.sql', '00001000000000000000001.sql', '00001000000000000000003.sql', '00001000000000000300000.sql', '00001000000000000300001.sql', '00001000003333300000001.sql', '00001000003333300000003.sql', '00001000003333300300000.sql', '00001000003333300300001.sql', '00001000030000000000000.sql', '00001000030000000000001.sql']

min_eui = 0.0
max_eui = 0.0

for input_filename in input_filenames:
    print(input_filename)
    if not input_filename in bad_sql_files:
    
        case_dict = {}
        eui = sql_query(input_path, input_filename, 'AnnualBuildingUtilityPerformanceSummary','Site and Source Energy','Total Site Energy','Energy Per Total Building Area')  #MJ/m2
        
        
        cooling = sql_query(input_path, input_filename, 'AnnualBuildingUtilityPerformanceSummary', 'End Uses', 'Cooling', 'Electricity')  #GJ
        cooling += sql_query(input_path, input_filename, 'AnnualBuildingUtilityPerformanceSummary','End Uses','Cooling','District Cooling')        
        
        heating = sql_query(input_path, input_filename, 'AnnualBuildingUtilityPerformanceSummary','End Uses','Heating','Electricity')  #GJ
        heating += sql_query(input_path, input_filename, 'AnnualBuildingUtilityPerformanceSummary','End Uses','Heating','Natural Gas')
        heating += sql_query(input_path, input_filename, 'AnnualBuildingUtilityPerformanceSummary','End Uses','Heating','District Heating')
        #print(heating)
        
        unmet_cooling_hours = sql_query(input_path, input_filename, 'SystemSummary','Time Setpoint Not Met','Facility','During Occupied Cooling')
        unmet_heating_hours = sql_query(input_path, input_filename, 'SystemSummary','Time Setpoint Not Met','Facility','During Occupied Heating')
        
        lighting_power_density = sql_query(input_path, input_filename, 'LightingSummary','Interior Lighting','Interior Lighting Total','Lighting Power Density')
        
        
        #print(os.path.exists(os.path.join(input_path, os.path.splitext(input_filename)[0] + '.res')))
        if os.path.exists(os.path.join(input_path, os.path.splitext(input_filename)[0] + '.res')):
            rad_data = pd.read_csv(os.path.join(input_path, os.path.splitext(input_filename)[0] + '.res'), sep='\t', lineterminator='\n', header=None, usecols=[0])
            series_size = rad_data.size
            dlf = float(rad_data[0][rad_data[0]>0.2].count())/series_size
        else:
            rad_data = None
            dlf = 0.25
                
        min_eui = min(eui, min_eui)
        max_eui = max(eui, max_eui)
                
        case_dict.update({
                'eui': eui,
                'cooling': cooling,
                'heating': heating,
                'unmet_cooling_hours': unmet_cooling_hours,
                'unmet_heating_hours': unmet_heating_hours,
                'lighting_power_density': lighting_power_density,
                'daylight_factor': dlf
                #'sensible heat gain summary'
                
                         })

        with open(os.path.join(output_path, os.path.splitext(input_filename)[0] + '.json'), 'w') as outfile:
            json.dump(case_dict, outfile)

        print('')
        print('EUI: ' + str(eui)
        print('Min EUI: ' + str(min_eui))
        print('Max EUI: ' + str(max_eui))
        print('')
