import glob
import json
import os
import pandas as pd
import reflex as rx
import re
from typing import Optional


from .plots import MeasurementDevicePlottingState
from ...utils import logger
from ...windchest.windsweep import append_files, change_dataquality_filter
from ...windchest import (
    InputOutput,
    GeneralCatergorisation,
    WindCube_Catergorisation,
    WindCube_Clean,
)


logger = logger.get_logger()
wc_io = InputOutput()
windCube_catergorisation = WindCube_Catergorisation()
windcube_clean = WindCube_Clean()
generalcatergorisation = GeneralCatergorisation()


class MeasurementDeviceDataAlterationState(MeasurementDevicePlottingState):
    # timeseries: Optional[pd.DataFrame] = None
    # metadata_log: Optional[dict] = None
    # metadata_reference: Optional[dict] = None
    # newfiles: Optional[list] = None

    # @rx.var(cache=True)
    # def load_cleaneddata(self):
    #     if self.measurementdevice is not None:
    #         cleaneddata_path = os.path.join(str(self.rawdata_folder), "cleaned_timeseries.csv")
    #         if os.path.exists(cleaneddata_path):
    #             timeseries = wc_io.skip_to(cleaneddata_path)
    #             logger.debug("Cleaned data fetched with skip_to()")
    #             self.timeseries = timeseries
    #         else:
    #             logger.debug("No Cleaned data available")
    #             return None
    #     else:
    #             logger.debug("Measurement device not available in this state")
    #             return None

    # @rx.var(cache=True)
    # def metadata_log(self):
    #     if self.measurementdevice is not None:
    #         metadatalog_path = os.path.join(self.rawdata_folder, "self.metadata_log.json")
    #         if os.path.exists(metadatalog_path):
    #             with open(metadatalog_path, "r") as f:
    #                 self.metadata_log = json.load(f)
    #                 logger.debug("Metadata log fetched")
    #                 self.metadata_log = self.metadata_log
    #         else:
    #             logger.debug("Metadata log not available")
    #             return None
    #     else:
    #             logger.debug("Measurement device not available in this state")
    #             return None

    # @rx.var(cache=True)
    # def load_referencemetadata(self):
    #     if self.measurementdevice is not None:
    #         self.metadata_reference_path = os.path.join(self.rawdata_folder, "self.metadata_reference.json")
    #         if os.path.exists(self.metadata_reference_path):
    #             with open(self.metadata_reference_path, "r") as f:
    #                 logger.debug("Metadata referecnce loaded")
    #                 self.metadata_reference = json.load(f)
    #                 self.metadata_reference = self.metadata_reference
    #         else:
    #             logger.debug("No Metadata referecnce available")
    #             return None
    #     else:
    #             logger.debug("Measurement device not available in this state")
    #             return None

    # @rx.var()
    # def check_for_newfiles(self):
    #     processedfiles_path = os.path.join(self.rawdata_folder, "cleanedfile_paths.json")
    #     allfiles_path = glob.glob(
    #         r"{}".format(self.rawdata_folder + "\**\*.sta"), recursive=True
    #     )
    #     if os.path.exists(processedfiles_path):
    #         new_files = set(allfiles_path) - set(processedfiles_path)
    #         return new_files
    #     else:
    #         return allfiles_path

    # def parse_altitudes(altitudes_str):
    #     return [float(alt) for alt in altitudes_str.split()]

    # def parse_location(location_str):
    #     lat_match = re.search(r"Lat:([0-9.]+)°([NS])", location_str)
    #     lon_match = re.search(r"Long:([0-9.]+)°([EW])", location_str)

    #     if lat_match and lon_match:
    #         latitude = float(lat_match.group(1))
    #         longitude = float(lon_match.group(1))

    #         # Adjust latitude and longitude for the hemisphere
    #         if lat_match.group(2) == "S":
    #             latitude = -latitude
    #         if lon_match.group(2) == "W":
    #             longitude = -longitude

    #         return (latitude, longitude)
    #     else:
    #         return None

    # def check_location_change(location1, location2, threshold=0.000859991822):
    #     lat1, lon1 = location1
    #     lat2, lon2 = location2

    #     lat_diff = abs(lat2 - lat1)
    #     lon_diff = abs(lon2 - lon1)

    #     return lat_diff > threshold or lon_diff > threshold

    # def append_files(self):
    #     print("raw_datafolderis",self.rawdata_folder)
    #     newrawdata_filepaths = self.check_for_newfiles(self.rawdata_folder)
    #     if newrawdata_filepaths:
    #         logger.debug("retrieved new raw data files")
    #         if self.timeseries is not None:
    #             all_timesereis_data = pd.DataFrame()
    #             for file_path in newrawdata_filepaths:
    #                 metadata = wc_io.windcube_meta_data(
    #                     path=rf"{file_path}", search_word="Timestamp"
    #                 )

    #                 daily_timereseries = wc_io.skip_to(
    #                     file_path, search_word="Timestamp", sep="\t"
    #                 )
    #                 daily_timereseries.set_index(
    #                     "Timestamp (end of interval)", inplace=True
    #                 )
    #                 all_timesereis_data = pd.concat(
    #                     [all_timesereis_data, daily_timereseries]
    #                 )
    #                 timestamp = daily_timereseries.index[0]

    #             if metadata == self.metadata_reference:
    #                 self.metadata_reference = metadata

    #             else:
    #                 for key in metadata:
    #                     if (
    #                         key not in self.metadata_reference
    #                         or metadata[key] != self.metadata_reference[key]
    #                     ):
    #                         if key == "PitchAngle (°)":
    #                             # Calculate the percentage difference for PitchAngle and RollAngle
    #                             referencefile_value = float(self.metadata_reference[key])
    #                             current_value = float(metadata[key])
    #                             percentage_difference = (
    #                                 abs(current_value - referencefile_value)
    #                                 / referencefile_value
    #                                 * 100
    #                             )

    #                             if (
    #                                 percentage_difference > 2
    #                             ):  # Check if the percentage difference is greater than 4%
    #                                 self.metadata_log.append(
    #                                     {
    #                                         "Date/Time": timestamp,
    #                                         f"{key}": str(current_value),
    #                                     }
    #                                 )
    #                         elif key == "RollAngle (°)":
    #                             # Calculate the percentage difference for PitchAngle and RollAngle
    #                             referencefile_value = float(self.metadata_reference[key])
    #                             current_value = float(metadata[key])
    #                             percentage_difference = (
    #                                 abs(current_value - referencefile_value)
    #                                 / referencefile_value
    #                                 * 100
    #                             )

    #                             if (
    #                                 percentage_difference > 2
    #                             ):  # Check if the percentage difference is greater than 2%
    #                                 self.metadata_log.append(
    #                                     {
    #                                         "Date/Time": timestamp,
    #                                         f"{key}": str(current_value),
    #                                     }
    #                                 )
    #                         elif key == "GPS Location":

    #                             try:
    #                                 referencefile_location = parse_location(
    #                                     self.metadata_reference[key]
    #                                 )
    #                                 current_location = parse_location(metadata[key])
    #                             except None as e:
    #                                 print(f"Error parsing location: {e}")
    #                                 continue

    #                             # Check for changes in latitude and longitude
    #                             if self.check_location_change(
    #                                 referencefile_location, current_location
    #                             ):
    #                                 self.metadata_log.append(
    #                                     {
    #                                         "Date/Time": timestamp,
    #                                         f"{key}": str(current_location),
    #                                     }
    #                                 )

    #                         elif key == "Altitudes AGL (m)":
    #                             # Convert altitude strings to lists of floats
    #                             referencefile_altitudes = parse_altitudes(
    #                                 self.metadata_reference[key]
    #                             )
    #                             current_altitudes = parse_altitudes(metadata[key])

    #                             if referencefile_altitudes != current_altitudes:
    #                                 self.metadata_log.append(
    #                                     {
    #                                         "Date/Time": timestamp,
    #                                         f"{key}": str(current_altitudes),
    #                                     }
    #                                 )
    #                         else:
    #                             self.metadata_log.append(
    #                                 {
    #                                     "Date/Time": timestamp,
    #                                     f"{key}": metadata[key],
    #                                 }
    #                             )
    #                 self.metadata_reference = metadata
    #             logger.debug("Metadata Checked")
    #             formated_timeseries_data, flag_cols = (
    #                 windCube_catergorisation.windcube_channels_to_wp_format(
    #                     all_timesereis_data
    #                 )
    #             )
    #             logger.debug("New data formatted to WP standard")
    #             cleaned_data = windcube_clean.windcube_data_filter(
    #                 formated_timeseries_data, flag_cols, dataquality_filter
    #             )
    #             logger.debug("New data cleaned")
    #             if timeseries is not None:
    #                 cleaned_data.reset_index(inplace=True)
    #                 timeseries.reset_index(inplace=True)
    #                 cleaned_data = pd.concat([timeseries, cleaned_data])
    #                 cleaned_data_exportpath = os.path.join(
    #                     self.rawdata_folder, "cleaned_timeseries.csv"
    #                 )
    #                 cleaned_data.to_csv(cleaned_data_exportpath)
    #                 logger.debug("New data appended and saved")

    #             self.metadata_reference_exportpath = os.path.join(
    #                 self.rawdata_folder, "self.metadata_reference.json"
    #             )
    #             with open(self.metadata_reference_exportpath, "w") as f:
    #                 json.dump(self.metadata_reference, f, indent=4)

    #             self.metadata_log_exportpath = os.path.join(self.rawdata_folder, "self.metadata_log.json")
    #             with open(self.metadata_log_exportpath, "w") as f:
    #                 json.dump(self.metadata_log, f, indent=4)

    #             allfiles_path = glob.glob(
    #                 r"{}".format(self.rawdata_folder + "\**\*.sta"), recursive=True
    #             )
    #             cleaned_files_path = self.rawdata_folder + "\cleanedfile_paths.json"
    #             with open(cleaned_files_path, "w") as f:
    #                 json.dump(allfiles_path, f)

    #         else:
    #             newrawdata_filepaths = self.check_for_newfiles(self.rawdata_folder)
    #             logger.debug("retrieved new raw data files")
    #             all_timesereis_data = pd.DataFrame()
    #             self.metadata_log = []
    #             first_file_path = newrawdata_filepaths[0]
    #             self.metadata_reference = wc_io.windcube_meta_data(
    #                 path=rf"{first_file_path}", search_word="Timestamp"
    #             )
    #             lidar_data = wc_io.skip_to(
    #                 first_file_path, search_word="Timestamp", sep="\t"
    #             )
    #             lidar_data.set_index("Timestamp (end of interval)", inplace=True)
    #             timestamp = lidar_data.index[0]
    #             for key in self.metadata_reference:
    #                 if key == "GPS Location":
    #                     try:
    #                         referencefile_location = parse_location(self.metadata_reference[key])
    #                     except ValueError as e:
    #                         print(f"Error parsing location: {e}")
    #                         continue
    #                     self.metadata_log.append(
    #                         {
    #                             "Date/Time": timestamp,
    #                             f"{key}": str(referencefile_location),
    #                         }
    #                     )

    #                 elif key == "Altitudes AGL (m)":
    #                     # Convert altitude strings to lists of floats
    #                     referencefile_altitudes = parse_altitudes(self.metadata_reference[key])

    #                     self.metadata_log.append(
    #                         {
    #                             "Date/Time": timestamp,
    #                             f"{key}": str(referencefile_altitudes),
    #                         }
    #                     )
    #                 else:
    #                     self.metadata_log.append(
    #                         {
    #                             "Date/Time": timestamp,
    #                             f"{key}": self.metadata_reference[key],
    #                         }
    #                     )
    #             for file_path in newrawdata_filepaths:
    #                 metadata = wc_io.windcube_meta_data(
    #                     path=rf"{file_path}", search_word="Timestamp"
    #                 )

    #                 daily_timereseries = wc_io.skip_to(
    #                     file_path, search_word="Timestamp", sep="\t"
    #                 )
    #                 daily_timereseries.set_index(
    #                     "Timestamp (end of interval)", inplace=True
    #                 )
    #                 all_timesereis_data = pd.concat(
    #                     [all_timesereis_data, daily_timereseries]
    #                 )
    #                 timestamp = daily_timereseries.index[0]

    #             if metadata == self.metadata_reference:
    #                 self.metadata_reference = metadata

    #             else:
    #                 for key in metadata:
    #                     if (
    #                         key not in self.metadata_reference
    #                         or metadata[key] != self.metadata_reference[key]
    #                     ):
    #                         if key == "PitchAngle (°)":
    #                             # Calculate the percentage difference for PitchAngle and RollAngle
    #                             referencefile_value = float(self.metadata_reference[key])
    #                             current_value = float(metadata[key])
    #                             percentage_difference = (
    #                                 abs(current_value - referencefile_value)
    #                                 / referencefile_value
    #                                 * 100
    #                             )

    #                             if (
    #                                 percentage_difference > 2
    #                             ):  # Check if the percentage difference is greater than 4%
    #                                 self.metadata_log.append(
    #                                     {
    #                                         "Date/Time": timestamp,
    #                                         f"{key}": str(current_value),
    #                                     }
    #                                 )
    #                         elif key == "RollAngle (°)":
    #                             # Calculate the percentage difference for PitchAngle and RollAngle
    #                             referencefile_value = float(self.metadata_reference[key])
    #                             current_value = float(metadata[key])
    #                             percentage_difference = (
    #                                 abs(current_value - referencefile_value)
    #                                 / referencefile_value
    #                                 * 100
    #                             )

    #                             if (
    #                                 percentage_difference > 2
    #                             ):  # Check if the percentage difference is greater than 2%
    #                                 self.metadata_log.append(
    #                                     {
    #                                         "Date/Time": timestamp,
    #                                         f"{key}": str(current_value),
    #                                     }
    #                                 )
    #                         elif key == "GPS Location":

    #                             try:
    #                                 referencefile_location = parse_location(
    #                                     self.metadata_reference[key]
    #                                 )
    #                                 current_location = parse_location(metadata[key])
    #                             except None as e:
    #                                 print(f"Error parsing location: {e}")
    #                                 continue

    #                             # Check for changes in latitude and longitude
    #                             if check_location_change(
    #                                 referencefile_location, current_location
    #                             ):
    #                                 self.metadata_log.append(
    #                                     {
    #                                         "Date/Time": timestamp,
    #                                         f"{key}": str(current_location),
    #                                     }
    #                                 )

    #                         elif key == "Altitudes AGL (m)":
    #                             # Convert altitude strings to lists of floats
    #                             referencefile_altitudes = parse_altitudes(
    #                                 self.metadata_reference[key]
    #                             )
    #                             current_altitudes = parse_altitudes(metadata[key])

    #                             if referencefile_altitudes != current_altitudes:
    #                                 self.metadata_log.append(
    #                                     {
    #                                         "Date/Time": timestamp,
    #                                         f"{key}": str(current_altitudes),
    #                                     }
    #                                 )
    #                         else:
    #                             self.metadata_log.append(
    #                                 {
    #                                     "Date/Time": timestamp,
    #                                     f"{key}": metadata[key],
    #                                 }
    #                             )
    #                 self.metadata_reference = metadata
    #             logger.debug("Metadata Checked")
    #             formated_timeseries_data, flag_cols = (
    #                 windCube_catergorisation.windcube_channels_to_wp_format(
    #                     all_timesereis_data
    #                 )
    #             )
    #             logger.debug("New data formatted to WP standard")
    #             cleaned_data = windcube_clean.windcube_data_filter(
    #                 formated_timeseries_data, flag_cols, dataquality_filter
    #             )
    #             logger.debug("New data cleaned")
    #             cleaned_data_exportpath = os.path.join(
    #                 self.rawdata_folder, "cleaned_timeseries.csv"
    #             )
    #             cleaned_data.to_csv(cleaned_data_exportpath)
    #             logger.debug("New data appended and saved")
    #             self.metadata_reference_exportpath = os.path.join(
    #                 self.rawdata_folder, "self.metadata_reference.json"
    #             )
    #             with open(self.metadata_reference_exportpath, "w") as f:
    #                 json.dump(self.metadata_reference, f, indent=4)

    #             self.metadata_log_exportpath = os.path.join(self.rawdata_folder, "self.metadata_log.json")
    #             with open(self.metadata_log_exportpath, "w") as f:
    #                 json.dump(self.metadata_log, f, indent=4)

    #             allfiles_path = glob.glob(
    #                 r"{}".format(self.rawdata_folder + "\**\*.sta"), recursive=True
    #             )
    #             cleaned_files_path = self.rawdata_folder + "\cleanedfile_paths.json"
    #             with open(cleaned_files_path, "w") as f:
    #                 json.dump(allfiles_path, f)

    def handle_dataqualitysubmit(self, form_data):
        # logger.debug(f"Measurement Device Edit formdata : {form_data}")
        logger.debug(f"dataquality edit form : {form_data}")
        dataquality_filter = form_data["dataquality_filter"]
        self.rawdata_folder = self.rawdata_location.replace('"', "")
        from datetime import datetime

        date_iso_part = datetime.now().isoformat().replace(":", "-")
        change_dataquality_filter(
            self.rawdata_folder, dataquality_filter, date_iso_part
        )
        self.form_data = form_data
        measurementdevice_id = form_data.pop("measurementdevice_id")

        updated_data = {**form_data}
        # updated_data["cleaned_filepath"] = f"cleaned_timeseries_{date_iso_part}.csv"
        self.save_measurementdevice_edits(measurementdevice_id, updated_data)
        self.update_timeseries_plot()
        return self.to_measurementdevice()

    def handle_appenddata(self):

        print("raw_datafolder is ", self.rawdata_folder)
        dataquality_filter = self.dataquality_filter
        append_files(self.rawdata_folder, int(dataquality_filter))
        self.update_timeseries_plot()
        return self.to_measurementdevice()
