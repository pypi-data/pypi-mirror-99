import unittest

import ast
import pandas as pd
import numpy as np
from datetime import datetime, timedelta, timezone

import flirt.reader.empatica
import flirt.simple

import glob


class FillingTestCase(unittest.TestCase):
    def test_filling(self):
        # ibi = flirt.reader.empatica.read_ibi_file_into_df('wearable-data/empatica/IBI.csv')
        # ibi = flirt.get_hrv_features(ibi['ibi'], 180, 1, ['td', 'fd', 'stat'], 0.0)

        # self.assertEqual(8482, len(ibi))
        df = self.main()
        fill = df['hrv_filling']
        print(fill)

    def find_label_timestamps(self, ID, StartingTime):
        df_timestamp = pd.read_csv(glob.glob('/Volumes/mtec_nas_im_snf_headwind/misc/datasets/wesad/' + ID + '/*quest.csv')[0], delimiter=';', header=1).iloc[:2,
                       :].dropna(axis=1)
        print('===================================')
        print('Printing the timestamp for {0}'.format(ID))
        print('===================================')
        print(df_timestamp.head())

        # Start/End of experiment periods
        print('\nStart of the baseline: ' + str(df_timestamp['Base'][0]))
        print('End of the baseline: ' + str(df_timestamp['Base'][1]))
        print('Start of the fun: ' + str(df_timestamp['Fun'][0]))
        print('End of the fun: ' + str(df_timestamp['Fun'][1]))
        print('Start of the stress: ' + str(df_timestamp['TSST'][0]))
        print('End of the stress: ' + str(df_timestamp['TSST'][1]))

        # Get start and end time and assign label into a dict
        lab_dict = {'Base': 0, 'TSST': 1, 'Fun': 2}
        labels_times_dict = {}
        for mode in df_timestamp.columns.tolist():
            print('mode', mode)
            if mode == 'Base' or mode == 'Fun' or mode == 'TSST':
                labels_times_dict[mode] = [
                    StartingTime + timedelta(minutes=int(str(df_timestamp[mode][0]).split(".")[0])) + timedelta(
                        seconds=int(str(df_timestamp[mode][0]).split(".")[1])),
                    StartingTime + timedelta(minutes=int(str(df_timestamp[mode][1]).split(".")[0])) + timedelta(
                        seconds=int(str(df_timestamp[mode][1]).split(".")[1])), lab_dict[mode]]

        return labels_times_dict

    def find_label_start_time(self, ID):
        timestamp = open(glob.glob('/Volumes/mtec_nas_im_snf_headwind/misc/datasets/wesad/' + ID + '/*respiban.txt')[0], "r")
        for i in range(2):
            line = (timestamp.readline())
            line = line.strip()[2:]
            if i == 1:
                dict = ast.literal_eval(line)
                start_time_str = dict['00:07:80:D8:AB:58']['time']
                date_str = dict['00:07:80:D8:AB:58']['date']
                datetime_str = date_str + " " + start_time_str
                # print(datetime_str)
                # date_time_obj= date_time_obj.replace(tzinfo="Europe/Berlin")

                date_time_obj = pd.to_datetime(datetime_str).tz_localize("Europe/Berlin")
                utc_time = date_time_obj.tz_convert(None)

                # print(date_time_obj)
                # start_time = date_time_obj
                # utc_time = start_time - timedelta(hours=2)
        timestamp.close()

        # df_timestamp = pd.read_table(glob2.glob('project_data/WESAD/' + ID + '/*respiban.txt')[0], delim_whitespace=True)#.iloc[:2, :].dropna(axis = 1)
        print('===================================')
        print('Printing the timestamp for {0}'.format(ID))
        print('===================================')
        # print(df_timestamp.head())
        return utc_time

    def get_features_per_subject(self, path, window_length):
        return flirt.simple.get_features_for_empatica_archive(zip_file_path=path,
                                                              window_length=window_length,
                                                              window_step_size=0.25,
                                                              hrv_features=True,
                                                              eda_features=False,
                                                              acc_features=False,
                                                              bvp_features=False,
                                                              temp_features=False,
                                                              debug=True)

    def main(self):
        # os.chdir('/home/fefespinola/ETHZ_Fall_2020/') #local directory where the script is
        df_all = pd.DataFrame(None)
        # relevant_features = pd.DataFrame(None)
        File_Path = glob.glob('/Volumes/mtec_nas_im_snf_headwind/misc/datasets/wesad/**/*_readme.txt', recursive=True)
        window_length = 60  # in seconds
        window_shift = 0.25  # in seconds
        for subject_path in File_Path:
            print(subject_path)
            print(subject_path.split('/')[-2])
            ID = subject_path.split('/')[-2]
            ID = 'S5'
            zip_path = glob.glob('/Volumes/mtec_nas_im_snf_headwind/misc/datasets/wesad/' + ID + '/*_Data.zip')[0]
            print(zip_path)
            features = self.get_features_per_subject(zip_path, window_length)
            features.index.name = 'timedata'
            E4Time = features.index[0]
            print(E4Time)
            StartingTime = self.find_label_start_time(ID)
            print(StartingTime)
            labels_times = self.find_label_timestamps(ID, StartingTime)
            # features.index.tz_localize(tz='UTC')
            relevant_features = features.loc[
                ((features.index.tz_localize(tz=None) + timedelta(seconds=window_length) >= labels_times['Base'][0]) & (
                            features.index.tz_localize(tz=None) <= labels_times['Base'][1]))
                | ((features.index.tz_localize(tz=None) + timedelta(seconds=window_length) >= labels_times['Fun'][
                    0]) & (features.index.tz_localize(tz=None) <= labels_times['Fun'][1]))
                | ((features.index.tz_localize(tz=None) + timedelta(seconds=window_length) >= labels_times['TSST'][
                    0]) & (features.index.tz_localize(tz=None) <= labels_times['TSST'][1]))]

            relevant_features.insert(0, 'ID', ID)
            relevant_features.loc[(relevant_features.index.tz_localize(tz=None) >= labels_times['Base'][0]) &
                                  (relevant_features.index.tz_localize(tz=None) <= labels_times['Base'][1]), 'label'] = \
            labels_times['Base'][2]
            relevant_features.loc[(relevant_features.index.tz_localize(tz=None) >= labels_times['Fun'][0]) &
                                  (relevant_features.index.tz_localize(tz=None) <= labels_times['Fun'][1]), 'label'] = \
            labels_times['Fun'][2]
            relevant_features.loc[(relevant_features.index.tz_localize(tz=None) >= labels_times['TSST'][0]) &
                                  (relevant_features.index.tz_localize(tz=None) <= labels_times['TSST'][1]), 'label'] = \
            labels_times['TSST'][2]

            # concatenate all subjects and add IDs
            df_all = pd.concat((df_all, relevant_features))
            break
        print(df_all)
        return df_all
