
import os
import pandas as pd
import sqlite3
import json


input_path=''
input_filenames = ["0101000000.sql", "1000000000.sql"]



def sql_query(input_path, input_filename, report_name, table_name, row_name, column_name):
    sql_query = 'SELECT Value from TabularDataWithStrings WHERE ReportName=\'' + report_name + '\''
    #sql_query += ' and ReportForString=\'' + report_for_string + '\''
    sql_query += ' and TableName=\'' + table_name + '\''
    sql_query += ' and ColumnName=\'' + column_name + '\''
    sql_query += ' and RowName=\'' + row_name + '\''
    sql_query += ';'
    print sql_query

    con = sqlite3.connect(os.path.join(input_path, input_filename))
    df = pd.read_sql_query(sql_query, con)
    con.close()
    
    return float(df.iloc[0]['Value'])


for input_filename in input_filenames:
    case_dict = {}
    eui = sql_query(input_path, input_filename, 'AnnualBuildingUtilityPerformanceSummary','Site and Source Energy','Total Site Energy','Energy Per Total Building Area')
    cooling = sql_query(input_path, input_filename, 'ComponentSizingSummary', 'DistrictCooling', 'DISTRICT COOLING', 'Design Size Nominal Capacity')
    heating = sql_query(input_path, input_filename, 'ComponentSizingSummary','DistrictHeating','DISTRICT HEATING','Design Size Nominal Capacity')
    
    case_dict.update({
            'eui': eui,
            'cooling': cooling,
            'heating': heating
                     })

    with open(os.path.splitext(input_filename)[0] + '.json', 'w') as outfile:
        json.dump(case_dict, outfile)


