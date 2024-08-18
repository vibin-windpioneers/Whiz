import json
import glob
import os
import pandas as pd
import re
from datetime import datetime


from ..io import InputOutput
from ..categorisation import WindCube_Catergorisation, GeneralCatergorisation
from ..wind_scrub import WindCube_Clean

from ...utils import logger


logger = logger.get_logger()


wc_io = InputOutput()
windCube_catergorisation = WindCube_Catergorisation()
windcube_clean = WindCube_Clean()
generalcatergorisation = GeneralCatergorisation()


def parse_altitudes(altitudes_str):
    return [float(alt) for alt in altitudes_str.split()]


def parse_location(location_str):
    lat_match = re.search(r"Lat:([0-9.]+)°([NS])", location_str)
    lon_match = re.search(r"Long:([0-9.]+)°([EW])", location_str)

    if lat_match and lon_match:
        latitude = float(lat_match.group(1))
        longitude = float(lon_match.group(1))

        # Adjust latitude and longitude for the hemisphere
        if lat_match.group(2) == "S":
            latitude = -latitude
        if lon_match.group(2) == "W":
            longitude = -longitude

        return (latitude, longitude)
    else:
        return None


def check_location_change(location1, location2, threshold=0.000859991822):
    lat1, lon1 = location1
    lat2, lon2 = location2

    lat_diff = abs(lat2 - lat1)
    lon_diff = abs(lon2 - lon1)

    return lat_diff > threshold or lon_diff > threshold


def load_cleaneddata(rawdata_folder):
    cleaneddata_path = os.path.join(str(rawdata_folder), "cleaned_timeseries.csv")
    if os.path.exists(cleaneddata_path):
        timeseries = wc_io.skip_to(cleaneddata_path)
        logger.debug("Cleaned data loaded")
        return timeseries
    else:
        logger.debug("No Cleaned data available")
        return None


def check_for_newfiles(rawdata_folder):
    processedfiles_path = os.path.join(rawdata_folder, "cleanedfile_paths.json")
    allfiles_path = glob.glob(
        r"{}".format(rawdata_folder + "\**\*.sta"), recursive=True
    )
    if os.path.exists(processedfiles_path):
        new_files = set(allfiles_path) - set(processedfiles_path)
        return new_files
    else:
        return allfiles_path


def load_metadata_log(rawdata_folder):
    metadatalog_path = os.path.join(rawdata_folder, "metadata_log.json")
    if os.path.exists(metadatalog_path):
        with open(metadatalog_path, "r") as f:
            metadata_log = json.load(f)
            logger.debug("Metadata log loaded")
            return metadata_log
    else:
        logger.debug("No Metadata log available")
        return None


def load_referencemetadata(rawdata_folder):
    metadata_reference_path = os.path.join(rawdata_folder, "metadata_reference.json")
    if os.path.exists(metadata_reference_path):
        with open(metadata_reference_path, "r") as f:
            logger.debug("Metadata referecnce loaded")
            metadata_reference = json.load(f)
            return metadata_reference
    else:
        logger.debug("No Metadata referecnce available")
        return None


def append_files(rawdata_folder, dataquality_filter):
    print("raw_datafolderis", rawdata_folder)
    newrawdata_filepaths = check_for_newfiles(rawdata_folder)
    if newrawdata_filepaths:
        logger.debug("retrieved new raw data files")
        timeseries = load_cleaneddata(rawdata_folder)
        if timeseries is not None:
            metadata_log = load_metadata_log(rawdata_folder)
            metadata_reference = load_referencemetadata(rawdata_folder)
            logger.debug("Metadata referecnce loaded")
            all_timesereis_data = pd.DataFrame()
            for file_path in newrawdata_filepaths:
                metadata = wc_io.windcube_meta_data(
                    path=rf"{file_path}", search_word="Timestamp"
                )

                daily_timereseries = wc_io.skip_to(
                    file_path, search_word="Timestamp", sep="\t"
                )
                daily_timereseries.set_index(
                    "Timestamp (end of interval)", inplace=True
                )
                all_timesereis_data = pd.concat(
                    [all_timesereis_data, daily_timereseries]
                )
                timestamp = daily_timereseries.index[0]

            if metadata == metadata_reference:
                metadata_reference = metadata

            else:
                for key in metadata:
                    if (
                        key not in metadata_reference
                        or metadata[key] != metadata_reference[key]
                    ):
                        if key == "PitchAngle (°)":
                            # Calculate the percentage difference for PitchAngle and RollAngle
                            referencefile_value = float(metadata_reference[key])
                            current_value = float(metadata[key])
                            percentage_difference = (
                                abs(current_value - referencefile_value)
                                / referencefile_value
                                * 100
                            )

                            if (
                                percentage_difference > 2
                            ):  # Check if the percentage difference is greater than 4%
                                metadata_log.append(
                                    {
                                        "Date/Time": timestamp,
                                        f"{key}": str(current_value),
                                    }
                                )
                        elif key == "RollAngle (°)":
                            # Calculate the percentage difference for PitchAngle and RollAngle
                            referencefile_value = float(metadata_reference[key])
                            current_value = float(metadata[key])
                            percentage_difference = (
                                abs(current_value - referencefile_value)
                                / referencefile_value
                                * 100
                            )

                            if (
                                percentage_difference > 2
                            ):  # Check if the percentage difference is greater than 2%
                                metadata_log.append(
                                    {
                                        "Date/Time": timestamp,
                                        f"{key}": str(current_value),
                                    }
                                )
                        elif key == "GPS Location":

                            try:
                                referencefile_location = parse_location(
                                    metadata_reference[key]
                                )
                                current_location = parse_location(metadata[key])
                            except None as e:
                                print(f"Error parsing location: {e}")
                                continue

                            # Check for changes in latitude and longitude
                            if check_location_change(
                                referencefile_location, current_location
                            ):
                                metadata_log.append(
                                    {
                                        "Date/Time": timestamp,
                                        f"{key}": str(current_location),
                                    }
                                )

                        elif key == "Altitudes AGL (m)":
                            # Convert altitude strings to lists of floats
                            referencefile_altitudes = parse_altitudes(
                                metadata_reference[key]
                            )
                            current_altitudes = parse_altitudes(metadata[key])

                            if referencefile_altitudes != current_altitudes:
                                metadata_log.append(
                                    {
                                        "Date/Time": timestamp,
                                        f"{key}": str(current_altitudes),
                                    }
                                )
                        else:
                            metadata_log.append(
                                {
                                    "Date/Time": timestamp,
                                    f"{key}": metadata[key],
                                }
                            )
                metadata_reference = metadata
            logger.debug("Metadata Checked")
            formated_timeseries_data, flag_cols = (
                windCube_catergorisation.windcube_channels_to_wp_format(
                    all_timesereis_data
                )
            )
            logger.debug("New data formatted to WP standard")
            cleaned_data = windcube_clean.windcube_data_filter(
                formated_timeseries_data, flag_cols, dataquality_filter
            )
            logger.debug("New data cleaned")
            if timeseries is not None:
                cleaned_data.reset_index(inplace=True)
                timeseries.reset_index(inplace=True)
                cleaned_data = pd.concat([timeseries, cleaned_data])
                cleaned_data_exportpath = os.path.join(
                    rawdata_folder, "cleaned_timeseries.csv"
                )
                cleaned_data.to_csv(cleaned_data_exportpath)
                logger.debug("New data appended and saved")

            metadata_reference_exportpath = os.path.join(
                rawdata_folder, "metadata_reference.json"
            )
            with open(metadata_reference_exportpath, "w") as f:
                json.dump(metadata_reference, f, indent=4)

            metadata_log_exportpath = os.path.join(rawdata_folder, "metadata_log.json")
            with open(metadata_log_exportpath, "w") as f:
                json.dump(metadata_log, f, indent=4)

            allfiles_path = glob.glob(
                r"{}".format(rawdata_folder + "\**\*.sta"), recursive=True
            )
            cleaned_files_path = rawdata_folder + "\cleanedfile_paths.json"
            with open(cleaned_files_path, "w") as f:
                json.dump(allfiles_path, f)

        else:
            newrawdata_filepaths = check_for_newfiles(rawdata_folder)
            logger.debug("retrieved new raw data files")
            all_timesereis_data = pd.DataFrame()
            metadata_log = []
            first_file_path = newrawdata_filepaths[0]
            metadata_reference = wc_io.windcube_meta_data(
                path=rf"{first_file_path}", search_word="Timestamp"
            )
            lidar_data = wc_io.skip_to(
                first_file_path, search_word="Timestamp", sep="\t"
            )
            lidar_data.set_index("Timestamp (end of interval)", inplace=True)
            timestamp = lidar_data.index[0]
            for key in metadata_reference:
                if key == "GPS Location":
                    try:
                        referencefile_location = parse_location(metadata_reference[key])
                    except ValueError as e:
                        print(f"Error parsing location: {e}")
                        continue
                    metadata_log.append(
                        {
                            "Date/Time": timestamp,
                            f"{key}": str(referencefile_location),
                        }
                    )

                elif key == "Altitudes AGL (m)":
                    # Convert altitude strings to lists of floats
                    referencefile_altitudes = parse_altitudes(metadata_reference[key])

                    metadata_log.append(
                        {
                            "Date/Time": timestamp,
                            f"{key}": str(referencefile_altitudes),
                        }
                    )
                else:
                    metadata_log.append(
                        {
                            "Date/Time": timestamp,
                            f"{key}": metadata_reference[key],
                        }
                    )
            for file_path in newrawdata_filepaths:
                metadata = wc_io.windcube_meta_data(
                    path=rf"{file_path}", search_word="Timestamp"
                )

                daily_timereseries = wc_io.skip_to(
                    file_path, search_word="Timestamp", sep="\t"
                )
                daily_timereseries.set_index(
                    "Timestamp (end of interval)", inplace=True
                )
                all_timesereis_data = pd.concat(
                    [all_timesereis_data, daily_timereseries]
                )
                timestamp = daily_timereseries.index[0]

            if metadata == metadata_reference:
                metadata_reference = metadata

            else:
                for key in metadata:
                    if (
                        key not in metadata_reference
                        or metadata[key] != metadata_reference[key]
                    ):
                        if key == "PitchAngle (°)":
                            # Calculate the percentage difference for PitchAngle and RollAngle
                            referencefile_value = float(metadata_reference[key])
                            current_value = float(metadata[key])
                            percentage_difference = (
                                abs(current_value - referencefile_value)
                                / referencefile_value
                                * 100
                            )

                            if (
                                percentage_difference > 2
                            ):  # Check if the percentage difference is greater than 4%
                                metadata_log.append(
                                    {
                                        "Date/Time": timestamp,
                                        f"{key}": str(current_value),
                                    }
                                )
                        elif key == "RollAngle (°)":
                            # Calculate the percentage difference for PitchAngle and RollAngle
                            referencefile_value = float(metadata_reference[key])
                            current_value = float(metadata[key])
                            percentage_difference = (
                                abs(current_value - referencefile_value)
                                / referencefile_value
                                * 100
                            )

                            if (
                                percentage_difference > 2
                            ):  # Check if the percentage difference is greater than 2%
                                metadata_log.append(
                                    {
                                        "Date/Time": timestamp,
                                        f"{key}": str(current_value),
                                    }
                                )
                        elif key == "GPS Location":

                            try:
                                referencefile_location = parse_location(
                                    metadata_reference[key]
                                )
                                current_location = parse_location(metadata[key])
                            except None as e:
                                print(f"Error parsing location: {e}")
                                continue

                            # Check for changes in latitude and longitude
                            if check_location_change(
                                referencefile_location, current_location
                            ):
                                metadata_log.append(
                                    {
                                        "Date/Time": timestamp,
                                        f"{key}": str(current_location),
                                    }
                                )

                        elif key == "Altitudes AGL (m)":
                            # Convert altitude strings to lists of floats
                            referencefile_altitudes = parse_altitudes(
                                metadata_reference[key]
                            )
                            current_altitudes = parse_altitudes(metadata[key])

                            if referencefile_altitudes != current_altitudes:
                                metadata_log.append(
                                    {
                                        "Date/Time": timestamp,
                                        f"{key}": str(current_altitudes),
                                    }
                                )
                        else:
                            metadata_log.append(
                                {
                                    "Date/Time": timestamp,
                                    f"{key}": metadata[key],
                                }
                            )
                metadata_reference = metadata
            logger.debug("Metadata Checked")
            formated_timeseries_data, flag_cols = (
                windCube_catergorisation.windcube_channels_to_wp_format(
                    all_timesereis_data
                )
            )
            logger.debug("New data formatted to WP standard")
            cleaned_data = windcube_clean.windcube_data_filter(
                formated_timeseries_data, flag_cols, dataquality_filter
            )
            logger.debug("New data cleaned")
            cleaned_data_exportpath = os.path.join(
                rawdata_folder, "cleaned_timeseries.csv"
            )
            cleaned_data.to_csv(cleaned_data_exportpath)
            logger.debug("New data appended and saved")
            metadata_reference_exportpath = os.path.join(
                rawdata_folder, "metadata_reference.json"
            )
            with open(metadata_reference_exportpath, "w") as f:
                json.dump(metadata_reference, f, indent=4)

            metadata_log_exportpath = os.path.join(rawdata_folder, "metadata_log.json")
            with open(metadata_log_exportpath, "w") as f:
                json.dump(metadata_log, f, indent=4)

            allfiles_path = glob.glob(
                r"{}".format(rawdata_folder + "\**\*.sta"), recursive=True
            )
            cleaned_files_path = rawdata_folder + "\cleanedfile_paths.json"
            with open(cleaned_files_path, "w") as f:
                json.dump(allfiles_path, f)


def change_dataquality_filter(rawdata_folder, new_dataquality_filter, suffix):
    timeseries = load_cleaneddata(rawdata_folder)
    logger.debug("Timeseries loaded")
    flag_cols = generalcatergorisation.get_flagcols(timeseries)
    timeseries[flag_cols] = ""
    cleaned_data = windcube_clean.windcube_data_filter(
        timeseries, flag_cols, int(new_dataquality_filter)
    )
    cleaned_data.set_index("Date/Time", inplace=True)
    cleaned_data_exportpath = os.path.join(
        rawdata_folder, f"cleaned_timeseries_{suffix}.csv"
    )
    cleaned_data.to_csv(cleaned_data_exportpath)

    logger.debug("Cleaned datasaved with new dataquality filter")
