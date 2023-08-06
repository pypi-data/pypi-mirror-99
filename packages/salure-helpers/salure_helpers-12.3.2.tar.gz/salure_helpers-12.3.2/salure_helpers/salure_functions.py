import sys
from typing import Union

import pandas as pd
import numpy as np
import os
import time
import requests
import datetime
from salure_helpers.mysql import MySQL
from zipfile import ZipFile


class SalureFunctions:

    """
    Functions in this class are:
    - applymap: ....
    - catch_error: ...
    - scheduler_error_handling: ...
    - convert_empty_columns_type: ...
    - dfdate_to_datetime: ...
    - send_error_to_slack: ...
    - gen_dict_extract: ...
    - detect_changes_between_dataframes: ...
    - generate_mutation_list_from_dataframes: ...
    - archive_old_files: ...
    - df_to_xlsx: ...
    - zip_files: ...
    - intervalmatch_dates: ...
    """

    @staticmethod
    def applymap(key: pd.Series, mapping: dict, default=None):
        """
        This function maps a given column of a dataframe to new values, according to specified mapping.
        Column types float and int are converted to object because those types can't be compared and changed
        ----------
        :param key: input on which you want to apply the rename.
        :param mapping: mapping dict in which to lookup the mapping
        :param default_value: fallback if mapping value is not in mapping dict (only for non Series)
        :return: df with renamed columns
        """
        if type(key) == pd.Series:
            if key.dtype == 'float64' or key.dtype == 'int64':
                key = key.astype('object')
            if len(mapping) == 0:
                return 'Geen mapping gespecificeerd'
            else:
                key.replace(to_replace=mapping, inplace=True)

                return key
        else:
            if key in mapping.keys():
                return mapping[key]
            else:
                return default

    @staticmethod
    def catch_error(e):
        exc_type, exc_obj, exc_tb = sys.exc_info()
        error = str(e)[:400].replace('\'', '').replace('\"', '') + ' | Line: {}'.format(exc_tb.tb_lineno)
        raise Exception(error)

    @staticmethod
    def scheduler_error_handling(e: Exception, task_id, run_id, mysql_con: MySQL, breaking=True, started_at=None):
        """
        This function handles errors that occur in the scheduler. Logs the traceback, updates run statuses and notifies users
        :param e: the Exception that is to be handled
        :param task_id: The scheduler task id
        :param mysql_con: The connection which is used to update the scheduler task status
        :param logger: The logger that is used to write the logging status to
        :param breaking: Determines if the error is breaking or code will continue
        :param started_at: Give the time the task is started
        :return: nothing
        """
        # Format error to a somewhat readable format
        exc_type, exc_obj, exc_tb = sys.exc_info()
        error = str(e)[:400].replace('\'', '').replace('\"', '') + ' | Line: {}'.format(exc_tb.tb_lineno)
        # Get scheduler task details for logging
        task_details = mysql_con.select('task_scheduler', 'queue_name, runfile_path', 'WHERE id = {}'.format(task_id))[0]
        taskname = task_details[0]
        customer = task_details[1].split('/')[-1].split('.')[0]

        if breaking:
            # Set scheduler status to failed
            mysql_con.update('task_scheduler', ['status', 'last_error_message'], ['IDLE', 'Failed'], 'WHERE `id` = {}'.format(task_id))
            # Log to database
            mysql_con.raw_query("INSERT INTO `task_execution_log` VALUES ({}, {}, 'CRITICAL', '{}', {}, '{}')".format(run_id, task_id, datetime.datetime.now(), exc_tb.tb_lineno, error), insert=True)
            mysql_con.raw_query("INSERT INTO `task_scheduler_log` VALUES ({}, {}, 'Failed', '{}', '{}')".format(run_id, task_id, started_at, datetime.datetime.now()),
                insert=True)
            # Notify users on Slack
            SalureFunctions.send_error_to_slack(customer, taskname, 'failed')
            raise Exception(error)
        else:
            mysql_con.raw_query("INSERT INTO `task_execution_log` VALUES ({}, {}, 'CRITICAL', '{}', {}, '{}')".format(run_id, task_id, datetime.datetime.now(), exc_tb.tb_lineno, error), insert=True)
            SalureFunctions.send_error_to_slack(customer, taskname, 'contains an error')

    @staticmethod
    def convert_empty_columns_type(df: pd.DataFrame):
        """
        Converts the type of columns which are complete empty (not even one value filled) to object. This columns are
        sometimes int or float but that's difficult to work with. Therefore, change always to object
        :param df: input dataframe which must be converted
        :return: dataframe with new column types
        """
        for column in df:
            if df[column].isnull().all():
                df[column] = None

        return df

    @staticmethod
    def dfdate_to_datetime(df: pd.DataFrame, dateformat=None):
        """
        This function processes input dataset and tries to convert all columns to datetime. If this throws an error, it skips the column
        ----------
        :param df: input dataframe for which you want to convert datetime columns
        :param dateformat: optionally specify output format for datetimes. If empty, defaults to %y-%m-%d %h:%m:%s
        :return: returns input df but all date columns formatted according to datetime format specified
        """
        df = df.apply(lambda col: pd.to_datetime(col, errors='ignore').dt.tz_localize(None) if col.dtypes == object else col, axis=0)
        if format is not None:
            # optional if you want custom date format. Note that this changes column type from date to string
            df = df.apply(lambda col: col.dt.strftime(dateformat) if col.dtypes == 'datetime64[ns]' else col, axis=0)
            df.replace('NaT', '', inplace=True)

        return df


    @staticmethod
    def send_error_to_slack(customer, taskname, message):
        """
        This function is meant to send scheduler errors to slack
        :param customer: Customername where error occured
        :param taskname: Taskname where error occured
        :return: nothing
        """
        message = requests.get('https://slack.com/api/chat.postMessage',
                               params={'channel': 'C04KBG1T2',
                                       'text': 'The reload task of {taskname} from {customer} {message}. Check the {taskname} log for details'.format(customer=customer,
                                                                                                                                                      taskname=taskname,
                                                                                                                                                      message=message),
                                       'username': 'Task Scheduler',
                                       'token': 'xoxp-4502361743-4844095730-47265352212-271109ebd7'}).content

    @staticmethod
    def gen_dict_extract(key, var):
        """
        Looks up a key in a nested dict until its found.
        :param key: Key to look for
        :param var: input dict (don't set a type for this, since it can be list as well when it recursively calls itself)
        :return: Generator object with a list of elements that are found. Acces with next() to get the first value or for loop to get all elements
        """
        if hasattr(var, 'items'):
            for k, v in var.items():
                if k == key:
                    yield v
                if isinstance(v, dict):
                    for result in SalureFunctions.gen_dict_extract(key, v):
                        yield result
                elif isinstance(v, list):
                    for d in v:
                        for result in SalureFunctions.gen_dict_extract(key, d):
                            yield result

    @staticmethod
    def detect_changes_between_dataframes(df_old: pd.DataFrame, df_actual: pd.DataFrame, check_columns: list, unique_key: str, keep_old_values: Union[str, bool] = False):
        """
        This function reads data from today and yesterday, flags this data according to old and new
        ----------
        :param df_old: A dataframe with the old values
        :param df_actual: A dataframe with the actual value. This one will be compared to the old_df
        :param check_columns: list of column(s) which you want to be used to check for changes in data
        :param unique_key: list of column(s) which you want to be used in order to group data. This should be the unique key which is always the same in data of today and yesterday
        :param keep_old_values: a parameter of type boolean (for backwards compatibility) or string. Optional values are: dict, rows, list.
        Dict gives a column which contains a dict of changed fields and corresponding values, list gives changed fields and changed values in two separate columns in a list, rows keeps the old entrie in a separate df row (flagged with flag_old).
        Default behaviour is False, returning nothing. If any value is given outside dict,rows,list, will also default to False.
        :return: Returns a dataframe with the new colums change_type (deleted, new or edited) and changed_fields (contains all the names of the changed fields)
        """
        # Set default if parameter outside possible options is given
        keep_old_values = keep_old_values if keep_old_values in ['dict', 'rows', 'list'] else False
        # Checking if the types of the columns (both check_columns and unique_key) correspond between df_old and df_new and raising an error if not
        for column in check_columns + [unique_key]:
            # int64 and float64 are an exception: a combination of these two types works fine
            if not (df_old[column].dtype in ['int64', 'float64'] and df_actual[column].dtype in ['int64', 'float64']) \
                    and not df_old[column].dtype == df_actual[column].dtype:
                raise ValueError(f'The types of the column \'{column}\' do not correspond between df_old ('
                                 f'{df_old[column].dtype}) and df_actual ({df_actual[column].dtype}).')
        df_old['flag_old'] = 1
        df_actual['flag_old'] = 0
        df = pd.concat([df_old, df_actual], sort=True).drop_duplicates(subset=check_columns + [unique_key], keep=False)
        df['freq'] = df.groupby(unique_key)[unique_key].transform('count')
        df['change_type'] = np.where(np.logical_and(df.freq == 1, df.flag_old == 0), 'new',
                                     np.where(np.logical_and(df.freq == 1, df.flag_old == 1), 'deleted',
                                              np.where(df.freq >= 2, 'edited',
                                                       'nothing'
                                                       )
                                              )
                                     )
        # Now check which values in which column are changed. Add the names of this columns to the column 'changed_fields'
        df.sort_values(by=[unique_key] + ['flag_old'], inplace=True, ascending=False)
        df.reset_index(inplace=True, drop=True)
        df['changed_fields'] = ''
        # If the unique key is already in the columns which need to be checked, then don't add this double. Otherwise comparison of rows won't work because two values are returned for an index
        if unique_key in check_columns:
            df_changes = df.loc[:, check_columns].fillna('')
        else:
            df_changes = df.loc[:, check_columns + [unique_key]].fillna('')
        for i in df_changes.index.values:
            curr_row: pd.Series = df_changes.iloc[i]
            prev_row = df_changes.iloc[i - 1]
            if curr_row[unique_key] == prev_row[unique_key] and i != 0:
                unique_columns = curr_row != prev_row
                if keep_old_values in ['list', 'dict']:
                    if keep_old_values == 'list':
                        df.loc[i, 'changed_fields'] = str([key for key, value in unique_columns.iteritems() if value is True and key != 'flag_old'])
                        df.loc[i, 'old_values'] = str([prev_row[key] for key, value in unique_columns.iteritems() if value is True and key != 'flag_old'])
                    else:
                        import json
                        df.loc[i, 'changes'] = json.dumps({key: str(prev_row[key]) for key, value in unique_columns.iteritems() if value is True and key != 'flag_old'})
                elif keep_old_values == 'rows' or keep_old_values is False:
                    df.loc[i, 'changed_fields'] = str([key for key, value in unique_columns.iteritems() if value is True and key != 'flag_old'])
        # remove old rows except for when return type is rows
        if keep_old_values != 'rows':
            df = df[(df['flag_old'] == 0) | (df['change_type'] == 'deleted')]
            df.drop(labels=['flag_old', 'freq'], axis='columns', inplace=True, errors='ignore')
        else:
            df['changed_fields'].fillna('', inplace=True)

        return df

    @staticmethod
    def generate_mutation_list_from_dataframes(df: pd.DataFrame, check_columns: list, unique_key: str):
        """
        This function compares the current row with the previous row, if the employeenumbers of these rows are the same.
        ----------
        :param df: Provide df which contains only edited data. Mandatory column in this df: employee_id
        :param check_columns: Provide the columns which you want to check for edited data. Only these columns will be checked
        :return: df with only mutations. This df contains four columns: employee, mutation type, old value and new value. For each mutation type, a new row will be created
        """
        df = df.loc[:, check_columns].fillna('')
        df.reset_index(inplace=True, drop=True)
        changes = pd.DataFrame()
        for i in df.index.values:
            curr_row = df.iloc[i]
            prev_row = df.iloc[i - 1]
            if curr_row[unique_key] == prev_row[unique_key] and i != 0:
                unique_columns = curr_row != prev_row
                new_vals = curr_row.loc[unique_columns]
                old_vals = prev_row.loc[unique_columns]
                for key in old_vals.keys():
                    changes = changes.append({'Employee': curr_row[unique_key], 'Mutation type': key, 'Old Value': old_vals[key], 'New Value': new_vals[key]}, ignore_index=True)

        return changes

    @staticmethod
    def archive_old_files(source_path: str, archive_path: str, comparison_data_path=None, archive_file_age_in_days=90):
        """
        This method moves all files from a source to a specified archive and cleans files from this archive that are older than archive_file_age_in_days
        :param source_path: source where to archive files from
        :param archive_path: archive path
        :param archive_file_age_in_days: all archived files older than this amount of days, will be moved
        :param comparison_data_path: optional comparison data path (standard method for detecting changes). This add extra functionality
        :return:
        """
        for file in os.listdir(archive_path):
            if os.stat(archive_path + file).st_mtime < time.time() - archive_file_age_in_days * 86400:
                os.remove(archive_path + file)
        # If a comparison data path is specified, this functions moves data from source to comparison, and from comparison to archive
        if comparison_data_path is not None:
            for file in os.listdir(comparison_data_path):
                os.rename(comparison_data_path + file, archive_path + str(datetime.datetime.now()) + file)
            for file in os.listdir(source_path):
                os.rename(source_path + file, comparison_data_path + file)
        else:
            for file in os.listdir(source_path):
                os.rename(source_path + file, archive_path + str(datetime.datetime.now().strftime('%d-%m-%Y_%H-%M-%S')) + file)

    @staticmethod
    def df_to_xslx(filepath: str, df: pd.DataFrame, sheetname: str, columns=None):
        """
        This method exports a dataframe to excel. If no columns are specified, then whole DF is exported. Columns will be the the DF columns
        If columns are specified, these will be used as header row. Only DF columns that are in the columns list, will be filled with data, rest is ignored
        :param df: input dataframe with data
        :param sheetname: sheetname to write to
        :param columns: list of columns which are accepted in Excel. DF column name must match one of these to be processed
        :return: void
        """
        writer = pd.ExcelWriter(filepath,
                                engine='xlsxwriter',
                                options={'remove_timezone': True})
        if columns is not None:
            columns = list(columns)
            df_columns = df.columns.values.tolist()

            # Add data to columns
            for df_column in df_columns:
                if df_column in columns:
                    series = df[df_column]
                    print(series.to_excel(writer, sheet_name=sheetname, startcol=columns.index(df_column), index=False, startrow=1, header=False))

            # Add custom headercolumns
            if len(df) > 0:
                worksheet = writer.sheets[sheetname]
                workbook = writer.book
                header_format = workbook.add_format({'bold': True})
                for i in columns:
                    worksheet.write(0, columns.index(i), i, header_format)
        else:
            df.to_excel(writer, sheet_name=sheetname, index=False)

    @staticmethod
    def zip_files(source_folder: str, output_filename: str, keep_original_files=True):
        """
        This method zips all the files in a folder
        :return: nothing
        """
        with ZipFile(output_filename, 'w') as zip:
            for file in os.listdir(source_folder):
                zip.write(source_folder + file, file)
                if not keep_original_files:
                    os.remove(source_folder + file)

    @staticmethod
    def intervalmatch_dates(df: pd.DataFrame, start_date: str, end_date: str, merge_key: str):
        """
        create a new row for each date between a start- and enddate. This new row will take all the values from the original row except that a new column
        wille be added named "date"
        :param df: dataframe with data with at least a startdate, enddate and key column
        :param start_date: the description of the start_date column
        :param end_date: the description of the end_date column
        :param merge_key: the key on which the data with the dates will be joined to the original df. For example a leave_id in leaves
        :return: the same dataframe as the original df but now with a row for each date between start- and enddate
        """
        df_dates_1 = df[[merge_key, start_date]]
        df_dates_1.rename(columns={start_date: 'date'}, inplace=True)
        df_dates_2 = df[[merge_key, end_date]]
        df_dates_2.rename(columns={end_date: 'date'}, inplace=True)
        df_dates = pd.concat([df_dates_1, df_dates_2])
        df_dates.sort_values(by=[merge_key, 'date'], ascending=[True, True], inplace=True)
        df_dates.drop_duplicates(inplace=True)
        df_dates.set_index('date', inplace=True)
        df_dates = df_dates.groupby(merge_key).resample('D').ffill().reset_index(level=0, drop=True).reset_index()
        df = pd.merge(df, df_dates, how='left', on=merge_key)

        return df

    @staticmethod
    def send_message_to_teams(title, message_content, action_name=None, action_url=None):
        """
        This functions sends an automatically generated message to Teams, formatted and with the colour of Salure.
        :param title: title of the error message
        :param message_content: content of the error message
        :param action_name: If a button that is linked to an action is needed, this needs to be filled with the name of this button. Else can be set to None.
        :param action_url: Here the redirect link what the button needs to open has to be filled. If there is no button, this can be set to None.
        :return: returns the status code and the message to see if sending the message to Teams worked.
        """
        group_id = '42d202e0-c990-4284-8fb6-56af44f8a2d8'
        tenant_id = 'd5164171-e477-4b6f-9044-ffcb90dc6a7a'
        webhook_id = '66e4092488cd4fa287f4064acf4c0afd/f5431315-de44-446f-881b-cd052530446b'
        url = f'https://outlook.office.com/webhook/{group_id}@{tenant_id}/IncomingWebhook/{webhook_id}'
        if action_name == None:
            body = {
                "@type": "MessageCard",
                "@context": "http://schema.org/extensions",
                "themeColor": 'F3910F',
                "summary": "Summary",
                "sections": [{
                    "activityTitle": title,
                    "facts": [{
                        "name": "",
                        "value": message_content
                    }],
                    "markdown": False
                }]
            }
        else:
            body = {
                "@type": "MessageCard",
                "@context": "http://schema.org/extensions",
                "themeColor": 'F3910F',
                "summary": "Summary",
                "sections": [{
                    "activityTitle": title,
                    "facts": [{
                        "name": "",
                        "value": message_content
                    }],
                    "markdown": False
                }],
                "potentialAction": [{
                    "@type": "OpenUri",
                    "name": action_name,
                    "targets": [{
                        "os": "default",
                        "uri": action_url
                    }]
                }]
            }
        response = requests.post(url, json=body)
        return response, response.status_code, response.text

    @staticmethod
    def send_error_to_teams(database, task_number, task_title):
        """
        This function makes sure that the content that is send to Teams, using the teams message function, is in a formatted table. This is done using HTML.
        :param database: the name of the database, for example sc_salure.
        :param task_number: the task id of the task that needs to be reported in Teams.
        :param task_title: the name of the specific task that needs to be reported in Teams.
        :return: returns the response of whether the message has been sent successfully. If so, this message contains a formatted table with the information.
        """
        task = f'<table><col width=220><col width=60><col width=400><thead><th>Database</th><th>ID</th><th>Description</th></thead><tbody><tr><td>{database}</td>' \
               f'<td>{task_number}</td><td>{task_title}</td></tr></tbody></table>'
        response = SalureFunctions().send_message_to_teams(title='From Python with love - Failed task in the SC Scheduler', message_content=task, action_name='Open Task Scheduler', action_url='https://salure.salureconnect.com/connectors/task-scheduler')
        return response
