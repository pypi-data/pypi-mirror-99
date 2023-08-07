"""
Provides functionality for converting between API versions.
"""

# TODO: Document
# TODO: Test
# TODO: Implement (de)normalization now that dynamic range in known in API M (how does this fork API 900 to API M?)
# TODO: Update any method that sets an enum to accent Union[Enum, int] to fix mypy type errors involving that
# TODO: Breakup conversion into smaller, more testable functions
# TODO: Rework location sensor conversions
# TODO: Add functions for converting compressed audio... in fact, this might make the most sent from converting API 900
# TODO:   into API M data since FLAC requires integers

from typing import List, Optional, Dict

import numpy as np

import redvox.api1000.common.common as common_m
import redvox.api1000.proto.redvox_api_m_pb2 as redvox_api_m_pb2
import redvox.common.date_time_utils as dt_utls
import redvox.api900.reader as reader_900
from redvox.api1000.wrapped_redvox_packet.sensors.sensors import Sensors
from redvox.api1000.wrapped_redvox_packet.sensors.location import LocationProvider
from redvox.api1000.wrapped_redvox_packet.station_information import (
    OsType,
    StationInformation,
    StationMetrics,
)
from redvox.api1000.wrapped_redvox_packet.timing_information import SynchExchange
from redvox.api1000.wrapped_redvox_packet.wrapped_packet import WrappedRedvoxPacketM
import redvox

_NORMALIZATION_CONSTANT: int = 0x7FFFFF
NAN: float = float("nan")


def _normalize_audio_count(count: int, normalize_by: Optional[float] = None) -> float:
    norm: float = normalize_by if normalize_by is not None else _NORMALIZATION_CONSTANT
    return float(count) / float(norm)


def _denormalize_audio_count(norm: float) -> int:
    return int(round(norm * float(_NORMALIZATION_CONSTANT)))


def _migrate_synch_exchanges_900_to_1000(
    synch_exchanges: np.ndarray,
) -> List[SynchExchange]:
    exchanges: List[SynchExchange] = []

    for i in range(0, len(synch_exchanges), 6):
        exchange: SynchExchange = SynchExchange.new()
        exchange.set_a1(float(synch_exchanges[i]))
        exchange.set_a2(float(synch_exchanges[i + 1]))
        exchange.set_a3(float(synch_exchanges[i + 2]))
        exchange.set_b1(float(synch_exchanges[i + 3]))
        exchange.set_b2(float(synch_exchanges[i + 4]))
        exchange.set_b3(float(synch_exchanges[i + 5]))
        exchanges.append(exchange)

    return exchanges


# todo: can set default return to np.nan?
def _find_mach_time_zero(packet: reader_900.WrappedRedvoxPacket) -> int:
    if "machTimeZero" in packet.metadata_as_dict():
        return int(packet.metadata_as_dict()["machTimeZero"])

    location_sensor: Optional[reader_900.LocationSensor] = packet.location_sensor()
    if location_sensor is not None:
        if "machTimeZero" in location_sensor.metadata_as_dict():
            return int(location_sensor.metadata_as_dict()["machTimeZero"])

    return -1


def _packet_length_microseconds_900(packet: reader_900.WrappedRedvoxPacket) -> int:
    microphone_sensor: Optional[
        reader_900.MicrophoneSensor
    ] = packet.microphone_sensor()

    if microphone_sensor is not None:
        sample_rate_hz: float = microphone_sensor.sample_rate_hz()
        total_samples: int = len(microphone_sensor.payload_values())
        length_seconds: float = float(total_samples) / sample_rate_hz
        return round(dt_utls.seconds_to_microseconds(length_seconds))

    return 0


# noinspection PyTypeChecker
# pylint: disable=C0103
def _migrate_os_type_900_to_1000(os: str) -> OsType:
    os_lower: str = os.lower()
    if os_lower == "android":
        return OsType.ANDROID

    if os_lower == "ios":
        return OsType.IOS

    return OsType.UNKNOWN_OS


# pylint: disable=C0103
def _migrate_os_type_1000_to_900(os: OsType) -> str:
    if os == OsType.ANDROID:
        return "Android"
    elif os == OsType.IOS:
        return "iOS"
    else:
        print(f"API 900 unsupported OsType: {os.name}")
        return os.name


# noinspection DuplicatedCode
def convert_api_900_to_1000(
    wrapped_packet_900: reader_900.WrappedRedvoxPacket,
) -> WrappedRedvoxPacketM:
    """
    Converts a wrapped API 900 packet into a wrapped API M packet.
    :param wrapped_packet_900: API 900 packet to convert.
    :return: A wrapped API M packet.
    """
    wrapped_packet_m: WrappedRedvoxPacketM = WrappedRedvoxPacketM.new()

    # Top-level metadata
    wrapped_packet_m.set_api(1000.0)
    # noinspection PyUnresolvedReferences,Mypy
    wrapped_packet_m.set_sub_api(redvox_api_m_pb2.SUB_API)

    # Station information
    station_information: StationInformation = wrapped_packet_m.get_station_information()
    station_information.set_id(wrapped_packet_900.redvox_id()).set_uuid(
        wrapped_packet_900.uuid()
    ).set_make(wrapped_packet_900.device_make()).set_model(
        wrapped_packet_900.device_model()
    ).set_os(
        _migrate_os_type_900_to_1000(wrapped_packet_900.device_os())
    ).set_os_version(
        wrapped_packet_900.device_os_version()
    ).set_app_version(
        wrapped_packet_900.app_version()
    ).set_is_private(
        wrapped_packet_900.is_private()
    )

    station_information.get_service_urls().set_acquisition_server(
        wrapped_packet_900.acquisition_server()
    ).set_synch_server(
        wrapped_packet_900.time_synchronization_server()
    ).set_auth_server(
        wrapped_packet_900.authentication_server()
    )

    # API 900 does not maintain a copy of its settings. So we will not set anything in AppSettings

    # StationMetrics - We know a couple. We take a slightly more cumbersome approach using the raw protobuf
    # to avoid some conversions between lists and np arrays.
    station_metrics: StationMetrics = station_information.get_station_metrics()
    station_metrics.get_timestamps().append_timestamp(
        wrapped_packet_900.app_file_start_timestamp_machine()
    )
    station_metrics.get_temperature().set_values(
        np.array([wrapped_packet_900.device_temperature_c()]), True
    )
    station_metrics.get_battery().set_values(
        np.array([wrapped_packet_900.battery_level_percent()]), True
    )

    # Timing information
    mach_time_900: int = wrapped_packet_900.app_file_start_timestamp_machine()
    os_time_900: int = (
        wrapped_packet_900.app_file_start_timestamp_epoch_microseconds_utc()
    )
    len_micros: int = _packet_length_microseconds_900(wrapped_packet_900)
    best_latency: Optional[float] = wrapped_packet_900.best_latency()
    best_latency = best_latency if best_latency is not None else NAN
    best_offset: Optional[float] = wrapped_packet_900.best_offset()
    best_offset = best_offset if best_offset is not None else NAN

    wrapped_packet_m.get_timing_information().set_unit(
        common_m.Unit.MICROSECONDS_SINCE_UNIX_EPOCH
    ).set_packet_start_mach_timestamp(mach_time_900).set_packet_start_os_timestamp(
        os_time_900
    ).set_packet_end_mach_timestamp(
        mach_time_900 + len_micros
    ).set_packet_end_os_timestamp(
        os_time_900 + len_micros
    ).set_server_acquisition_arrival_timestamp(
        wrapped_packet_900.server_timestamp_epoch_microseconds_utc()
    ).set_app_start_mach_timestamp(
        _find_mach_time_zero(wrapped_packet_900)
    ).set_best_latency(
        best_latency
    ).set_best_offset(
        best_offset
    )

    time_sensor = wrapped_packet_900.time_synchronization_sensor()
    if time_sensor is not None:
        wrapped_packet_m.get_timing_information().get_synch_exchanges().set_values(
            _migrate_synch_exchanges_900_to_1000(time_sensor.payload_values())
        )

    # Sensors
    sensors_m: Sensors = wrapped_packet_m.get_sensors()
    # Microphone / Audio
    mic_sensor_900: Optional[
        reader_900.MicrophoneSensor
    ] = wrapped_packet_900.microphone_sensor()
    if mic_sensor_900 is not None:
        normalized_audio: np.ndarray = mic_sensor_900.payload_values() / _NORMALIZATION_CONSTANT
        audio_sensor_m = sensors_m.new_audio()
        audio_sensor_m.set_first_sample_timestamp(
            mic_sensor_900.first_sample_timestamp_epoch_microseconds_utc()
        ).set_is_scrambled(wrapped_packet_900.is_scrambled()).set_sample_rate(
            mic_sensor_900.sample_rate_hz()
        ).set_sensor_description(
            mic_sensor_900.sensor_name()
        ).get_samples().set_values(
            normalized_audio, update_value_statistics=True
        )
        audio_sensor_m.get_metadata().set_metadata(mic_sensor_900.metadata_as_dict())

    # Barometer
    barometer_sensor_900: Optional[
        reader_900.BarometerSensor
    ] = wrapped_packet_900.barometer_sensor()
    if barometer_sensor_900 is not None:
        pressure_sensor_m = sensors_m.new_pressure()
        pressure_sensor_m.set_sensor_description(barometer_sensor_900.sensor_name())
        pressure_sensor_m.get_timestamps().set_timestamps(
            barometer_sensor_900.timestamps_microseconds_utc(), True
        )
        pressure_sensor_m.get_samples().set_values(
            barometer_sensor_900.payload_values(), True
        )
        pressure_sensor_m.get_metadata().set_metadata(
            barometer_sensor_900.metadata_as_dict()
        )

    # Location
    # TODO: rework
    location_sensor_900: Optional[
        reader_900.LocationSensor
    ] = wrapped_packet_900.location_sensor()
    if location_sensor_900 is not None:
        location_m = sensors_m.new_location()
        location_m.set_sensor_description(location_sensor_900.sensor_name())
        location_m.get_timestamps().set_timestamps(
            location_sensor_900.timestamps_microseconds_utc(), True
        )
        if location_sensor_900.check_for_preset_lat_lon():
            lat_lon: np.ndarray = location_sensor_900.get_payload_lat_lon()
            location_m.get_latitude_samples().set_values(lat_lon[:1], True)
            location_m.get_longitude_samples().set_values(lat_lon[1:], True)
        else:
            location_m.get_latitude_samples().set_values(
                location_sensor_900.payload_values_latitude(), True
            )
            location_m.get_longitude_samples().set_values(
                location_sensor_900.payload_values_longitude(), True
            )
            location_m.get_altitude_samples().set_values(
                location_sensor_900.payload_values_altitude(), True
            )
            location_m.get_speed_samples().set_values(
                location_sensor_900.payload_values_speed(), True
            )
            location_m.get_horizontal_accuracy_samples().set_values(
                location_sensor_900.payload_values_accuracy(), True
            )

        def _extract_meta_bool(metad: Dict[str, str], key: str) -> bool:
            if key not in metad:
                return False

            return metad[key] == "T"

        loc_meta_900 = location_sensor_900.metadata_as_dict()
        use_location = _extract_meta_bool(loc_meta_900, "useLocation")
        desired_location = _extract_meta_bool(loc_meta_900, "desiredLocation")
        permission_location = _extract_meta_bool(loc_meta_900, "permissionLocation")
        enabled_location = _extract_meta_bool(loc_meta_900, "enabledLocation")

        if desired_location:
            location_m.get_location_providers().set_values([LocationProvider.USER])
        elif enabled_location:
            location_m.get_location_providers().set_values([LocationProvider.GPS])
        elif use_location and desired_location and permission_location:
            location_m.get_location_providers().set_values([LocationProvider.NETWORK])
        else:
            location_m.get_location_providers().set_values([LocationProvider.NONE])

        location_m.set_location_permissions_granted(permission_location)
        location_m.set_location_services_enabled(use_location)
        location_m.set_location_services_requested(desired_location)

        # Once we're done here, we should remove the original metadata
        if "useLocation" in loc_meta_900:
            del loc_meta_900["useLocation"]
        if "desiredLocation" in loc_meta_900:
            del loc_meta_900["desiredLocation"]
        if "permissionLocation" in loc_meta_900:
            del loc_meta_900["permissionLocation"]
        if "enabledLocation" in loc_meta_900:
            del loc_meta_900["enabledLocation"]
        if "machTimeZero" in loc_meta_900:
            del loc_meta_900["machTimeZero"]
        location_m.get_metadata().set_metadata(loc_meta_900)

    # Time Synchronization
    # This was already added to the timing information

    # Accelerometer
    accelerometer_900 = wrapped_packet_900.accelerometer_sensor()
    if accelerometer_900 is not None:
        accelerometer_m = sensors_m.new_accelerometer()
        accelerometer_m.set_sensor_description(accelerometer_900.sensor_name())
        accelerometer_m.get_timestamps().set_timestamps(
            accelerometer_900.timestamps_microseconds_utc(), True
        )
        accelerometer_m.get_x_samples().set_values(
            accelerometer_900.payload_values_x(), True
        )
        accelerometer_m.get_y_samples().set_values(
            accelerometer_900.payload_values_y(), True
        )
        accelerometer_m.get_z_samples().set_values(
            accelerometer_900.payload_values_z(), True
        )
        accelerometer_m.get_metadata().set_metadata(
            accelerometer_900.metadata_as_dict()
        )

    # Magnetometer
    magnetometer_900 = wrapped_packet_900.magnetometer_sensor()
    if magnetometer_900 is not None:
        magnetometer_m = sensors_m.new_magnetometer()
        magnetometer_m.set_sensor_description(magnetometer_900.sensor_name())
        magnetometer_m.get_timestamps().set_timestamps(
            magnetometer_900.timestamps_microseconds_utc(), True
        )
        magnetometer_m.get_x_samples().set_values(
            magnetometer_900.payload_values_x(), True
        )
        magnetometer_m.get_y_samples().set_values(
            magnetometer_900.payload_values_y(), True
        )
        magnetometer_m.get_z_samples().set_values(
            magnetometer_900.payload_values_z(), True
        )
        magnetometer_m.get_metadata().set_metadata(magnetometer_900.metadata_as_dict())

    # Gyroscope
    gyroscope_900 = wrapped_packet_900.gyroscope_sensor()
    if gyroscope_900 is not None:
        gyroscope_m = sensors_m.new_gyroscope()
        gyroscope_m.set_sensor_description(gyroscope_900.sensor_name())
        gyroscope_m.get_timestamps().set_timestamps(
            gyroscope_900.timestamps_microseconds_utc(), True
        )
        gyroscope_m.get_x_samples().set_values(gyroscope_900.payload_values_x(), True)
        gyroscope_m.get_y_samples().set_values(gyroscope_900.payload_values_y(), True)
        gyroscope_m.get_z_samples().set_values(gyroscope_900.payload_values_z(), True)
        gyroscope_m.get_metadata().set_metadata(gyroscope_900.metadata_as_dict())

    # Light
    light_900 = wrapped_packet_900.light_sensor()
    if light_900 is not None:
        light_m = sensors_m.new_light()
        light_m.set_sensor_description(light_900.sensor_name())
        light_m.get_timestamps().set_timestamps(
            light_900.timestamps_microseconds_utc(), True
        )
        light_m.get_samples().set_values(light_900.payload_values(), True)
        light_m.get_metadata().set_metadata(light_900.metadata_as_dict())

    # Image
    # TODO: Implement

    # Proximity
    proximity_900 = wrapped_packet_900.infrared_sensor()
    if proximity_900 is not None:
        proximity_m = sensors_m.new_proximity()
        proximity_m.set_sensor_description(proximity_900.sensor_name())
        proximity_m.get_timestamps().set_timestamps(
            proximity_900.timestamps_microseconds_utc(), True
        )
        proximity_m.get_samples().set_values(proximity_900.payload_values(), True)
        proximity_m.get_metadata().set_metadata(proximity_900.metadata_as_dict())

    # Removed any other API 900 top-level metadata now that its been used
    meta = wrapped_packet_900.metadata_as_dict()
    if "machTimeZero" in meta:
        del meta["machTimeZero"]
    if "bestOffset" in meta:
        del meta["bestOffset"]
    if "bestLatency" in meta:
        del meta["bestLatency"]
    wrapped_packet_m.get_metadata().append_metadata(
        "migrated_from_api_900", f"v{redvox.VERSION}"
    )

    return wrapped_packet_m


def convert_api_1000_to_900(
    wrapped_packet_m: WrappedRedvoxPacketM,
) -> reader_900.WrappedRedvoxPacket:
    """
    Converts an API M wrapped packet into an API 900 wrapped packet.
    :param wrapped_packet_m: Packet to convert.
    :return: An API 900 wrapped packet.
    """
    # TODO detect and warn about all the fields that are being dropped due to conversion!
    wrapped_packet_900: reader_900.WrappedRedvoxPacket = (
        reader_900.WrappedRedvoxPacket()
    )

    station_information_m = wrapped_packet_m.get_station_information()
    sensors_m = wrapped_packet_m.get_sensors()
    audio_m = sensors_m.get_audio()

    wrapped_packet_900.set_api(900)
    wrapped_packet_900.set_uuid(station_information_m.get_uuid())
    wrapped_packet_900.set_redvox_id(station_information_m.get_id())
    wrapped_packet_900.set_authenticated_email(station_information_m.get_auth_id())
    wrapped_packet_900.set_authentication_token(
        "n/a"
    )  # Different auth protocols are used, can't convert between
    wrapped_packet_900.set_firebase_token("n/a")  # No longer in API M packet
    wrapped_packet_900.set_is_backfilled(False)  # No longer useful metric in API M
    wrapped_packet_900.set_is_private(station_information_m.get_is_private())
    wrapped_packet_900.set_is_scrambled(audio_m.get_is_scrambled())
    wrapped_packet_900.set_device_make(station_information_m.get_make())
    wrapped_packet_900.set_device_model(station_information_m.get_model())
    wrapped_packet_900.set_device_os(
        _migrate_os_type_1000_to_900(station_information_m.get_os())
    )
    wrapped_packet_900.set_device_os_version(station_information_m.get_os_version())
    wrapped_packet_900.set_app_version(station_information_m.get_app_version())

    battery_metrics = station_information_m.get_station_metrics().get_battery()
    battery_percent: float = (
        battery_metrics.get_values()[-1]
        if battery_metrics.get_values_count() > 0
        else 0.0
    )
    wrapped_packet_900.set_battery_level_percent(battery_percent)
    temp_metrics = station_information_m.get_station_metrics().get_temperature()
    device_temp: float = (
        temp_metrics.get_values()[-1] if temp_metrics.get_values_count() > 0 else 0.0
    )
    wrapped_packet_900.set_device_temperature_c(device_temp)

    server_info_m = wrapped_packet_m.get_station_information().get_service_urls()
    wrapped_packet_900.set_acquisition_server(server_info_m.get_acquisition_server())
    wrapped_packet_900.set_time_synchronization_server(server_info_m.get_synch_server())
    wrapped_packet_900.set_authentication_server(server_info_m.get_auth_server())

    timing_info_m = wrapped_packet_m.get_timing_information()
    wrapped_packet_900.set_app_file_start_timestamp_epoch_microseconds_utc(
        round(timing_info_m.get_packet_start_os_timestamp())
    )
    wrapped_packet_900.set_app_file_start_timestamp_machine(
        round(timing_info_m.get_packet_start_mach_timestamp())
    )
    wrapped_packet_900.set_server_timestamp_epoch_microseconds_utc(
        round(timing_info_m.get_server_acquisition_arrival_timestamp())
    )

    # Top-level metadata
    wrapped_packet_900.add_metadata(
        "machTimeZero", str(timing_info_m.get_app_start_mach_timestamp())
    )
    wrapped_packet_900.add_metadata(
        "bestLatency", str(timing_info_m.get_best_latency())
    )
    wrapped_packet_900.add_metadata("bestOffset", str(timing_info_m.get_best_offset()))
    wrapped_packet_900.add_metadata("migrated_from_api_1000", f"v{redvox.VERSION}")

    # Sensors
    if audio_m is not None:
        denorm_audio = list(
            map(_denormalize_audio_count, audio_m.get_samples().get_values())
        )
        mic_900 = reader_900.MicrophoneSensor()
        mic_900.set_sample_rate_hz(audio_m.get_sample_rate())
        mic_900.set_first_sample_timestamp_epoch_microseconds_utc(
            round(audio_m.get_first_sample_timestamp())
        )
        mic_900.set_sensor_name(audio_m.get_sensor_description())
        mic_900.set_metadata_as_dict(audio_m.get_metadata().get_metadata())
        mic_900.set_payload_values(denorm_audio)
        wrapped_packet_900.set_microphone_sensor(mic_900)

    pressure_m = sensors_m.get_pressure()
    if pressure_m is not None:
        barometer_900 = reader_900.BarometerSensor()
        barometer_900.set_sensor_name(pressure_m.get_sensor_description())
        barometer_900.set_metadata_as_dict(pressure_m.get_metadata().get_metadata())
        barometer_900.set_timestamps_microseconds_utc(
            pressure_m.get_timestamps().get_timestamps().astype(np.int64)
        )
        barometer_900.set_payload_values(pressure_m.get_samples().get_values())
        wrapped_packet_900.set_barometer_sensor(barometer_900)

    location_m = sensors_m.get_location()
    if location_m is not None:
        location_900 = reader_900.LocationSensor()
        location_900.set_sensor_name(location_m.get_sensor_description())
        location_900.set_timestamps_microseconds_utc(
            location_m.get_timestamps().get_timestamps().astype(np.int64)
        )
        location_900.set_payload_values(
            location_m.get_latitude_samples().get_values(),
            location_m.get_longitude_samples().get_values(),
            location_m.get_altitude_samples().get_values(),
            location_m.get_speed_samples().get_values(),
            location_m.get_horizontal_accuracy_samples().get_values(),
        )
        wrapped_packet_900.set_location_sensor(location_900)
        metadata = location_m.get_metadata().get_metadata()
        metadata["useLocation"] = (
            "T" if location_m.get_location_services_enabled() else "F"
        )
        metadata["desiredLocation"] = (
            "T" if location_m.get_location_services_requested() else "F"
        )
        metadata["permissionLocation"] = (
            "T" if location_m.get_location_permissions_granted() else "F"
        )
        metadata["enabledLocation"] = (
            "T"
            if LocationProvider.GPS in location_m.get_location_providers().get_values()
            else "FD"
        )
        location_900.set_metadata_as_dict(metadata)

    # Synch exchanges
    synch_exchanges_m = timing_info_m.get_synch_exchanges()
    if synch_exchanges_m.get_count() > 0:
        synch_900 = reader_900.TimeSynchronizationSensor()
        values: List[int] = []

        for exchange in synch_exchanges_m.get_values():
            values.extend(
                [
                    round(exchange.get_a1()),
                    round(exchange.get_a2()),
                    round(exchange.get_a3()),
                    round(exchange.get_b1()),
                    round(exchange.get_b2()),
                    round(exchange.get_b3()),
                ]
            )

        synch_900.set_payload_values(values)
        wrapped_packet_900.set_time_synchronization_sensor(synch_900)

    accel_m = sensors_m.get_accelerometer()
    if accel_m is not None:
        accel_900 = reader_900.AccelerometerSensor()
        accel_900.set_sensor_name(accel_m.get_sensor_description())
        accel_900.set_timestamps_microseconds_utc(
            accel_m.get_timestamps().get_timestamps().astype(np.int64)
        )
        accel_900.set_metadata_as_dict(accel_m.get_metadata().get_metadata())
        accel_900.set_payload_values(
            accel_m.get_x_samples().get_values(),
            accel_m.get_y_samples().get_values(),
            accel_m.get_z_samples().get_values(),
        )
        wrapped_packet_900.set_accelerometer_sensor(accel_900)

    magnetometer_m = sensors_m.get_magnetometer()
    if magnetometer_m is not None:
        magnetometer_900 = reader_900.MagnetometerSensor()
        magnetometer_900.set_sensor_name(magnetometer_m.get_sensor_description())
        magnetometer_900.set_timestamps_microseconds_utc(
            magnetometer_m.get_timestamps().get_timestamps().astype(np.int64)
        )
        magnetometer_900.set_metadata_as_dict(
            magnetometer_m.get_metadata().get_metadata()
        )
        magnetometer_900.set_payload_values(
            magnetometer_m.get_x_samples().get_values(),
            magnetometer_m.get_y_samples().get_values(),
            magnetometer_m.get_z_samples().get_values(),
        )
        wrapped_packet_900.set_magnetometer_sensor(magnetometer_900)

    gyroscope_m = sensors_m.get_gyroscope()
    if gyroscope_m is not None:
        gyroscope_900 = reader_900.GyroscopeSensor()
        gyroscope_900.set_sensor_name(gyroscope_m.get_sensor_description())
        gyroscope_900.set_timestamps_microseconds_utc(
            gyroscope_m.get_timestamps().get_timestamps().astype(np.int64)
        )
        gyroscope_900.set_metadata_as_dict(gyroscope_m.get_metadata().get_metadata())
        gyroscope_900.set_payload_values(
            gyroscope_m.get_x_samples().get_values(),
            gyroscope_m.get_y_samples().get_values(),
            gyroscope_m.get_z_samples().get_values(),
        )
        wrapped_packet_900.set_gyroscope_sensor(gyroscope_900)

    # Light
    light_m = sensors_m.get_light()
    if light_m is not None:
        light_900 = reader_900.LightSensor()
        light_900.set_sensor_name(light_m.get_sensor_description())
        light_900.set_metadata_as_dict(light_m.get_metadata().get_metadata())
        light_900.set_timestamps_microseconds_utc(
            light_m.get_timestamps().get_timestamps().astype(np.int64)
        )
        light_900.set_payload_values(light_m.get_samples().get_values())
        wrapped_packet_900.set_light_sensor(light_900)

    # Image, skip for now

    # Infrared / proximity
    proximity_m = sensors_m.get_proximity()
    if proximity_m is not None:
        proximity_900 = reader_900.InfraredSensor()
        proximity_900.set_sensor_name(proximity_m.get_sensor_description())
        proximity_900.set_metadata_as_dict(proximity_m.get_metadata().get_metadata())
        proximity_900.set_timestamps_microseconds_utc(
            proximity_m.get_timestamps().get_timestamps().astype(np.int64)
        )
        proximity_900.set_payload_values(proximity_m.get_samples().get_values())
        wrapped_packet_900.set_infrared_sensor(proximity_900)

    return wrapped_packet_900
