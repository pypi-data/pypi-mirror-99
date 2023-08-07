"""
This module provide type-safe data window configuration
"""

from dataclasses import dataclass
from dataclasses_json import dataclass_json
from typing import Optional, List, MutableMapping

import pprint
import toml


# defaults for configuration
DEFAULT_GAP_TIME_S: float = 0.25  # seconds to be considered a gap
DEFAULT_START_PADDING_S: float = 120.0  # time to add before start time when searching
DEFAULT_END_PADDING_S: float = 120.0  # time to add after end time when searching


@dataclass_json()
@dataclass
class DataWindowConfig:
    """
    Properties:
        input_directory: string, directory that contains the files to read data from.  REQUIRED
        structured_layout: bool, if True, the input_directory contains specially named and organized
                            directories of data.  Default True
        station_ids: optional list of strings, list of station ids to filter on.
                        If empty or None, get any ids found in the input directory.  Default None
        extensions: optional list of strings, representing file extensions to filter on.
                        If None, gets as much data as it can in the input directory.  Default None
        api_versions: optional list of ApiVersions, representing api versions to filter on.
                        If None, get as much data as it can in the input directory.  Default None
        start_year: optional int representing the year of the data window start time.  Default None
        start_month: optional int representing the month of the data window start time.  Default None
        start_day: optional int representing the day of the data window start time.  Default None
        start_hour: optional int representing the hour of the data window start time.  Default None
        start_minute: optional int representing the minute of the data window start time.  Default None
        start_second: optional int representing the second of the data window start time.  Default None
        end_year: optional int representing the year of the data window end time.  Default None
        end_month: optional int representing the month of the data window end time.  Default None
        end_day: optional int representing the day of the data window end time.  Default None
        end_hour: optional int representing the hour of the data window end time.  Default None
        end_minute: optional int representing the minute of the data window end time.  Default None
        end_second: optional int representing the second of the data window end time.  Default None
        end_padding_seconds: float representing the amount of seconds to include before the start datetime
                                when filtering data.  Default DEFAULT_START_PADDING_S
        end_padding_seconds: float representing the amount of seconds to include after the end datetime
                                when filtering data.  Default DEFAULT_END_PADDING_S
        gap_time_s: float representing the minimum amount of seconds between data points that would indicate a gap.
                    Default DEFAULT_GAP_TIME_S
        apply_correction: bool, if True, update the timestamps in the data based on best station offset.  Default True
        debug: bool, if True, output additional information when processing data window.  Default False
    """

    input_directory: str
    structured_layout: bool = True
    station_ids: Optional[List[str]] = None
    extensions: Optional[List[str]] = None
    api_versions: Optional[List[str]] = None
    start_year: Optional[int] = None
    start_month: Optional[int] = None
    start_day: Optional[int] = None
    start_hour: Optional[int] = None
    start_minute: Optional[int] = None
    start_second: Optional[int] = None
    end_year: Optional[int] = None
    end_month: Optional[int] = None
    end_day: Optional[int] = None
    end_hour: Optional[int] = None
    end_minute: Optional[int] = None
    end_second: Optional[int] = None
    start_padding_seconds: float = DEFAULT_START_PADDING_S
    end_padding_seconds: float = DEFAULT_END_PADDING_S
    gap_time_seconds: float = DEFAULT_GAP_TIME_S
    apply_correction: bool = True
    debug: bool = False

    @staticmethod
    def from_path(config_path: str) -> "DataWindowConfig":
        try:
            with open(config_path, "r") as config_in:
                config_dict: MutableMapping = toml.load(config_in)
                # noinspection Mypy
                return DataWindowConfig.from_dict(config_dict)
        except Exception as e:
            print(f"Error loading configuration at: {config_path}")
            raise e

    def pretty(self) -> str:
        # noinspection Mypy
        return pprint.pformat(self.to_dict())
