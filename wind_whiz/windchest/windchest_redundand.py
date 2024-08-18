# V0.03

import pandas as pd
import os
import re
import numpy as np
from scipy.stats import linregress

import calendar


class windchest:
    #     #Input Output
    #     def __init__(self,name):
    #         self.name = name

    #     def skip_to(self,path, search_word,nodata_value = 9999,**kwargs):
    #         if os.stat(path).st_size == 0:
    #             raise ValueError("File is empty")

    #         with open(path) as f:
    #             pos = 0
    #             cur_line = f.readline()
    #             while not cur_line.startswith(search_word):
    #                 pos = f.tell()
    #                 cur_line = f.readline()
    #             f.seek(pos)
    #             timeseries_data = pd.read_csv(f, **kwargs)
    #             timeseries_data[timeseries_data==nodata_value]= np.nan
    #             return timeseries_data

    # def meta_data(self,path, search_word,**kwargs):
    #     if os.stat(path).st_size == 0:
    #         raise ValueError("File is empty")
    #     lines_to_read = ""
    #     metadata_dict = {}
    #     with open(path) as f:
    #         lines = f.readlines()
    #         for i, line in enumerate(lines):
    #             if line.startswith(search_word):
    #                 break
    #             else:
    #                 if '=' in line:
    #                     key, value = line.split('=', 1)
    #                     # Remove leading and trailing whitespaces
    #                     key = key.strip()
    #                     value = value.strip()
    #                     metadata_dict[key] = value

    #     return metadata_dict

    # def windcube_meta_data(self,path,search_word,**kwargs):
    #     windcube_meta_data = self.meta_data(path,search_word,**kwargs)
    #     return(windcube_meta_data)

    # def get_time_interval(self,timeseries):
    #     intervals = timeseries.index[1:] - timeseries.index[:-1]
    #     interval_counts = intervals.value_counts()
    #     most_common_interval = interval_counts.idxmax()
    #     interval_in_minutes = most_common_interval.total_seconds() / 60
    #     return interval_in_minutes

    # def get_windspeed_cols(self,timeseries):
    #     #Input timeseries should be in WP format
    #     ws=[]
    #     for col in timeseries:
    #         if ('ws' in col.lower() and 'mean' in col.lower() and 'vws' not in col.lower()) and ('vws' not in col.lower() or 'dispersion' not in col.lower() or 'min' not in col.lower() or 'max' not in col.lower() ):
    #             ws.append(col)
    #     return ws

    # def required_cols(self,timeseries,search_value,num_of_nearest_channels):
    #     heights = self.measurement_height(timeseries)

    #     lower_values = []
    #     higher_values = []

    #     # Iterate through the list to find nearest values
    #     lower_values = sorted([num for num in heights if num < search_value], reverse=True)[:num_of_nearest_channels]

    #     # Find nearest greater numbers
    #     higher_values = sorted([num for num in heights if num > search_value])[:num_of_nearest_channels]

    #     req_heights = lower_values+higher_values
    #     req_cols = []
    #     for height in req_heights:
    #         col_name = f'WS_{height}_mean'
    #         req_cols.append(col_name)
    #     return req_cols

    # def find_nearest_height(self,all_heights, target_height_to_be_sheared):
    #     closest_heights = min(all_heights, key=lambda x: abs(x - target_height_to_be_sheared))
    #     return closest_heights

    # Processing

    # def data_channels(self,measurement_data):

    #     #vitals
    #     wiper_count = []
    #     battery = []
    #     int_temp =[]

    #     #Windspeed associated cols
    #     ws = []
    #     ws_dispersion = []
    #     ws_min=[]
    #     ws_max=[]

    #     #z-wind associated cols
    #     vws = []
    #     vws_dispersion = []

    #     #Wind direction associated cols
    #     wd = []

    #     #cnr associated cols
    #     cnr = []
    #     cnr_min = []
    #     dopp_spect =[]
    #     data_availability = []

    #     #ambient measurements
    #     temp =[]
    #     rh = []
    #     pressure = []

    #     for col in measurement_data:
    #         if ('wind speed (m/s)' in col.lower() ) and ('dispersion' not in col.lower() or 'min' not in col.lower() or 'max' not in col.lower() ):
    #             col_renamed='WS_'+re.findall('\d+', col)[0]+'_mean'
    #             measurement_data = measurement_data.rename(columns={col: col_renamed})
    #             ws.append(col_renamed)
    #         if ('wind speed dispersion (m/s)' in col.lower() ) and ( 'min' not in col.lower() or 'max' not in col.lower() ):
    #             col_renamed='WS_'+re.findall('\d+', col)[0]+'_dispersion'
    #             measurement_data = measurement_data.rename(columns={col: col_renamed})
    #             ws_dispersion.append(col_renamed)
    #         if ('wind speed min (m/s)' in col.lower() ) and ( 'dispersion' not in col.lower() or 'max' not in col.lower() ):
    #             col_renamed='WS_'+re.findall('\d+', col)[0]+'_min'
    #             measurement_data = measurement_data.rename(columns={col: col_renamed})
    #             ws_min.append(col_renamed)
    #         if ('wind speed max (m/s)' in col.lower() ) and ( 'dispersion' not in col.lower() or 'min' not in col.lower() ):
    #             col_renamed='WS_'+re.findall('\d+', col)[0]+'_max'
    #             measurement_data = measurement_data.rename(columns={col: col_renamed})
    #             ws_max.append(col_renamed)

    #         if ('z-wind (m/s)' in col.lower() ) and ( 'dispersion' not in col.lower()):
    #             col_renamed='VWS_'+re.findall('\d+', col)[0]+'_mean'
    #             measurement_data = measurement_data.rename(columns={col: col_renamed})
    #             vws.append(col_renamed)
    #         if ('z-wind dispersion (m/s)' in col.lower() ):
    #             col_renamed='VWS_'+re.findall('\d+', col)[0]+'_dispersion'
    #             measurement_data = measurement_data.rename(columns={col: col_renamed})
    #             vws_dispersion.append(col_renamed)

    #         if ('wind direction (°)' in col.lower() ):
    #             col_renamed='WD_'+re.findall('\d+', col)[0]+'_mean'
    #             measurement_data = measurement_data.rename(columns={col: col_renamed})
    #             wd.append(col_renamed)

    #         if ('cnr (db)' in col.lower() ) and ( 'min' not in col.lower() ):
    #             cnr.append(col)
    #         if ('cnr min (db)' in col.lower() ) :
    #             cnr_min.append(col)
    #         if ('cnr min (db)' in col.lower() ) :
    #             cnr_min.append(col)
    #         if ('dopp spect broad' in col.lower() ) :
    #             dopp_spect.append(col)
    #         if ('data availability (%)' in col.lower() ):
    #             data_availability.append(col)

    #         if ('ext temp (°c)' in col.lower() ):
    #             col_renamed='T_1_mean'
    #             measurement_data = measurement_data.rename(columns={col: col_renamed})
    #             temp.append(col_renamed)
    #         if ('rel humidity (%)' in col.lower() ):
    #             col_renamed='RH_1_mean'
    #             measurement_data = measurement_data.rename(columns={col: col_renamed})
    #             rh.append(col_renamed)
    #         if ('pressure' in col.lower() ):
    #             col_renamed='P_1_mean'
    #             measurement_data = measurement_data.rename(columns={col: col_renamed})
    #             pressure.append(col_renamed)

    #         if ('wiper count' in col.lower() ):
    #             wiper_count.append(col)
    #         if ('vbatt (v)' in col.lower() ):
    #             battery.append(col)
    #         if ('int temp (°c)' in col.lower() ):
    #             int_temp.append(col)

    #     return measurement_data

    # def windcube_data_filter(self,measurement_data,threshold):
    #     heights = self.measurement_height(measurement_data=measurement_data)
    #     for h in heights:
    #         measurement_data.loc[(measurement_data[f'{h}m Data Availability (%)']<threshold ),[f'WS_{h}_mean',f'WD_{h}_mean']] = 9999
    #     return measurement_data

    # def measurement_height(self,measurement_data):

    #     heights = []
    #     ws_cols = self.get_windspeed_cols(measurement_data)
    #     measurement_data = measurement_data[ws_cols]

    #     for col in measurement_data:
    #         matches = re.findall('\d+', col)
    #         if matches:
    #             h = int(matches[0])
    #             if h not in heights:
    #                 heights.append(h)

    #     return heights

    # def lidar_offset(self,lidar_data, offset):

    #     # Applies offset for data channel in Zx lidar , Currently only takes in data channel named according to WP naming convention.
    #     ws = []
    #     for col in lidar_data:
    #         if ('ws' in col.lower()):
    #             height = int(re.findall('\d+', col)[0])
    #             col_renamed=f'WS_{height+offset}_mean'
    #             lidar_data = lidar_data.rename(columns={col: col_renamed})
    #             ws.append(col_renamed)
    #         if ('wd' in col.lower()):
    #             height = int(re.findall('\d+', col)[0])
    #             col_renamed=f'WD_{height+offset}_mean'
    #             lidar_data = lidar_data.rename(columns={col: col_renamed})
    #             ws.append(col_renamed)
    #     return lidar_data

    # def wp_standard_names(self,timeseries):
    #     # Applies offset for data channel in Zx lidar , Currently only takes in data channel named according to WP naming convention.
    #     ws = []
    #     for col in timeseries:
    #         if (('ws' in col.lower()) and ('vws' not in col.lower())):
    #             height = int(re.findall('\d+', col)[0])
    #             col_renamed=f'WS_{height}_mean'
    #             timeseries = timeseries.rename(columns={col: col_renamed})
    #             ws.append(col_renamed)
    #         if ('wd' in col.lower()):
    #             height = int(re.findall('\d+', col)[0])
    #             col_renamed=f'WD_{height}_mean'
    #             timeseries = timeseries.rename(columns={col: col_renamed})
    #             ws.append(col_renamed)
    #     return timeseries

    # def means_of_averagingperiod(self,timeseries,averaging_period):
    #     # Timeseries has to have a DateTimeIndex
    #     timeseries_columns = timeseries.columns
    #     if averaging_period == 'ME':
    #             timeseries_resampled_mean = timeseries.resample(averaging_period).mean()
    #             timeseries_resampled_mean['period'] = timeseries_resampled_mean.index.month
    #             timeseries_resampled_mean_of_means = timeseries_resampled_mean.groupby('period').mean()

    #     else:
    #         averaging_period_integer = int(re.findall('\d+', averaging_period)[0])
    #         timeseries_resampled_mean = timeseries.resample(averaging_period).mean()
    #         timeseries_resampled_mean['day_of_year'] = timeseries_resampled_mean.index.dayofyear
    #         timeseries_resampled_mean['period'] = (timeseries_resampled_mean['day_of_year'] -1) // averaging_period_integer
    #         timeseries_resampled_mean_of_means = timeseries_resampled_mean.groupby('period').mean()

    #     return  timeseries_resampled_mean_of_means[timeseries_columns]

    # def momm(self,timeseries,averaging_period='ME',nodata_value = 9999):
    #     # Timeseries has to have a DateTimeIndex
    #     timeseries[timeseries==nodata_value]= np.nan
    #     if averaging_period != 'ME':
    #         print('Only mean of monthly means available , please use means_of_averagingpeiod of any other averaging period')
    #     time_interval_minutes = self.get_time_interval(timeseries)
    #     timeseries_columns = timeseries.columns
    #     mean_of_means_dict = {}
    #     timeseries['daysinmonth'] = timeseries.index.days_in_month
    #     timeseries['period'] = timeseries.index.month
    #     monthsize_without_completeness_factor = timeseries.groupby('period').agg(**{'monthsize':('daysinmonth','mean')})
    #     for col in timeseries_columns:
    #         mean_of_means_individual_cols = timeseries.groupby('period').agg(**{f'{col}_VDP': (col, 'count'),
    #                                                                             f'{col}': (col, 'mean')})
    #         mean_of_means_individual_cols[f'{col}_completeness_factor'] = ((mean_of_means_individual_cols[f'{col}_VDP']*(time_interval_minutes/(60*24)))/monthsize_without_completeness_factor['monthsize']).clip(upper=1)
    #         mean_of_means_individual_cols[f'{col}_monthsize_with_completeness_factor'] = mean_of_means_individual_cols[f'{col}_completeness_factor']*monthsize_without_completeness_factor['monthsize']

    #         mean_of_means_individual_cols[f'{col}*monthsize_with_cf'] = mean_of_means_individual_cols[f'{col}_monthsize_with_completeness_factor']*mean_of_means_individual_cols[col]

    #         mean_of_means_individual_cols = mean_of_means_individual_cols[[f'{col}*monthsize_with_cf',f'{col}_monthsize_with_completeness_factor']].sum()
    #         momm = mean_of_means_individual_cols[f'{col}*monthsize_with_cf']/mean_of_means_individual_cols[f'{col}_monthsize_with_completeness_factor']
    #         mean_of_means_dict[col]= momm
    #     return mean_of_means_dict

    # Shear

    # def month_hour_shear(self,timeseries,heights_tobe_sheared,num_of_nearest_channels):
    #     timeseries_cols = list(timeseries.columns)
    #     lidar_heights =  self.measurement_height(timeseries)
    #     sheared_heights_timeseries = pd.DataFrame()
    #     timeseries['month_hour'] = timeseries.index.to_series().apply(lambda x: f'{x.strftime("%B")}_{x.hour+1}')
    #     for sheared_height in heights_tobe_sheared :
    #         if sheared_height not in lidar_heights:
    #             req_cols = self.required_cols(timeseries,sheared_height,num_of_nearest_channels)

    #             timeseries_withrequired_heights = pd.concat([timeseries[req_cols],timeseries['month_hour']],axis=1)

    #             month_hour_windspeed = timeseries_withrequired_heights.groupby(['month_hour']).mean()
    #             month_hour_windspeed_log = month_hour_windspeed.apply(np.log)

    #             req_heights =  self.measurement_height(timeseries_withrequired_heights)
    #             req_heights_log = np.log(req_heights)

    #             slopes = []

    #             for index, row in month_hour_windspeed_log.iterrows():
    #                 slope, intercept, r_value, p_value, std_err = linregress(req_heights_log, row)
    #                 slopes.append(slope)
    #             month_hour_windspeed_log['power_law_exponent']= slopes

    #             timeseries_with_powerlawexponent = pd.merge(timeseries_withrequired_heights,month_hour_windspeed_log['power_law_exponent'],left_on='month_hour',right_on='month_hour')
    #             timeseries_with_powerlawexponent.index = timeseries_withrequired_heights.index
    #             nearest_height = self.find_nearest_height(req_heights,sheared_height)
    #             sheared_heights_timeseries[f'WS_{sheared_height}_mean']=timeseries_with_powerlawexponent[f'WS_{nearest_height}_mean']*((sheared_height / nearest_height) ** timeseries_with_powerlawexponent['power_law_exponent'])
    #             timeseries_with_powerlawexponent.drop(columns=['power_law_exponent'],inplace=True)

    #     timeseries = pd.concat([timeseries[timeseries_cols],sheared_heights_timeseries],axis=1)

    #     return timeseries

    # Vena Shear analysis
    def vena_method5(
        self, lidar_with_offset_applied, heights_tobe_sheared, num_of_nearest_channels
    ):
        month_hour_sheared_timeseries = self.month_hour_shear(
            lidar_with_offset_applied, heights_tobe_sheared, num_of_nearest_channels
        )

        ws_cols = self.get_windspeed_cols(month_hour_sheared_timeseries)
        month_hour_sheared_timeseries = month_hour_sheared_timeseries[ws_cols].copy()

        momm = self.momm(month_hour_sheared_timeseries)
        return momm

    def vena_method2(
        self,
        mast_timeseries,
        lidar_with_offset_applied,
        heights_tobe_sheared,
        num_of_nearest_channels,
    ):

        mast_heights = self.measurement_height(mast_timeseries)

        mast_timeseries["month_hour"] = mast_timeseries.index.to_series().apply(
            lambda x: f'{x.strftime("%B")}_{x.hour+1}'
        )
        lidar_with_offset_applied[
            "month_hour"
        ] = lidar_with_offset_applied.index.to_series().apply(
            lambda x: f'{x.strftime("%B")}_{x.hour+1}'
        )
        for sheared_height in heights_tobe_sheared:
            if sheared_height not in mast_heights:
                req_cols = self.required_cols(
                    lidar_with_offset_applied, sheared_height, num_of_nearest_channels
                )
                lidar_timeseries_withrequired_heights = pd.concat(
                    [
                        lidar_with_offset_applied[req_cols],
                        lidar_with_offset_applied["month_hour"],
                    ],
                    axis=1,
                )
                lidar_month_hour_windspeed = (
                    lidar_timeseries_withrequired_heights.groupby(["month_hour"]).mean()
                )
                lidar_month_hour_windspeed_log = lidar_month_hour_windspeed.apply(
                    np.log
                )

                req_heights = self.measurement_height(
                    lidar_timeseries_withrequired_heights
                )
                req_heights_log = np.log(req_heights)

                slopes = []
                for index, row in lidar_month_hour_windspeed_log.iterrows():
                    slope, intercept, r_value, p_value, std_err = linregress(
                        req_heights_log, row
                    )
                    slopes.append(slope)
                lidar_month_hour_windspeed_log["power_law_exponent"] = slopes

                mast_timeseries_with_powerlawexponent = pd.merge(
                    mast_timeseries,
                    lidar_month_hour_windspeed_log["power_law_exponent"],
                    left_on="month_hour",
                    right_on="month_hour",
                )

                mast_timeseries_with_powerlawexponent.index = mast_timeseries.index

                nearest_height = self.find_nearest_height(mast_heights, sheared_height)
                mast_timeseries[
                    f"WS_{sheared_height}_mean"
                ] = mast_timeseries_with_powerlawexponent[
                    f"WS_{nearest_height}_mean"
                ] * (
                    (sheared_height / nearest_height)
                    ** mast_timeseries_with_powerlawexponent["power_law_exponent"]
                )
                mast_timeseries_with_powerlawexponent.drop(
                    columns=["power_law_exponent"], inplace=True
                )
                mast_heights.append(sheared_height)

        ws_cols = self.get_windspeed_cols(mast_timeseries)

        mast_timeseries = mast_timeseries[ws_cols].copy()
        momm = self.momm(mast_timeseries)
        return momm
