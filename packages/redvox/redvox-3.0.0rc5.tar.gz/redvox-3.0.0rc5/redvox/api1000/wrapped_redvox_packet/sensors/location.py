"""
This module provides tools for working with RedVox API M location data and metadata.
"""

import enum
from typing import List

import redvox.api1000.common.common as common
from redvox.api1000.common.decorators import wrap_enum
from redvox.api1000.common.generic import ProtoBase, ProtoRepeatedMessage
import redvox.api1000.common.generic
import redvox.api1000.common.typing
from redvox.api1000.proto.redvox_api_m_pb2 import RedvoxPacketM


# noinspection Mypy
@wrap_enum(RedvoxPacketM.Sensors.Location.LocationProvider)
class LocationProvider(enum.Enum):
    """
    An enum that represents valid location providers
    """

    UNKNOWN: int = 0
    NONE: int = 1
    USER: int = 2
    GPS: int = 3
    NETWORK: int = 4


# noinspection Mypy
@wrap_enum(RedvoxPacketM.Sensors.Location.BestLocation.LocationScoreMethod)
class LocationScoreMethod(enum.Enum):
    """
    An enum that represents location scoring methods
    """

    UNKNOWN_METHOD: int = 0


class BestTimestamp(
    redvox.api1000.common.generic.ProtoBase[
        RedvoxPacketM.Sensors.Location.BestLocation.BestTimestamp
    ]
):
    """
    This class encapsulates the best timestamps associated with the best location estimates.
    """

    def __init__(
        self, proto: RedvoxPacketM.Sensors.Location.BestLocation.BestTimestamp
    ):
        super().__init__(proto)

    def get_unit(self) -> common.Unit:
        """
        :return: The unit of the timestamps.
        """
        # noinspection Mypy
        # pylint: disable=E1101
        return common.Unit.from_proto(self._proto.unit)

    def set_default_unit(self) -> "BestTimestamp":
        """
        Sets the default timestamp unit.
        :return: A modified instance of self
        """
        # noinspection PyTypeChecker
        return self.set_unit(common.Unit.MICROSECONDS_SINCE_UNIX_EPOCH)

    def set_unit(self, unit: common.Unit) -> "BestTimestamp":
        """
        Sets the unit of the best timestamps.
        :param unit: Unit to set.
        :return: A modified instance of self.
        """
        redvox.api1000.common.typing.check_type(unit, [common.Unit])
        # noinspection Mypy
        self._proto.unit = unit.into_proto()
        return self

    def get_mach(self) -> float:
        """
        :return: The best machine timestamp
        """
        return self._proto.mach

    def set_mach(self, mach: float) -> "BestTimestamp":
        """
        Sets the best machine timestamp.
        :param mach: Timestamp to set.
        :return: A modified instance of self.
        """
        redvox.api1000.common.typing.check_type(mach, [int, float])
        self._proto.mach = mach
        return self

    def get_gps(self) -> float:
        """
        :return: The best GPS timestamp.
        """
        return self._proto.gps

    def set_gps(self, gps: float) -> "BestTimestamp":
        """
        Sets the best GPS provided timestamp
        :param gps: Timestamp to set
        :return: A modified instance of self
        """
        redvox.api1000.common.typing.check_type(gps, [int, float])
        self._proto.gps = gps
        return self


class BestLocation(ProtoBase[RedvoxPacketM.Sensors.Location.BestLocation]):
    """
    Encapsulates the best location estimates
    """

    def __init__(self, proto: RedvoxPacketM.Sensors.Location.BestLocation):
        super().__init__(proto)
        self._latitude_longitude_timestamp: BestTimestamp = BestTimestamp(
            proto.latitude_longitude_timestamp
        )
        self._altitude_timestamp: BestTimestamp = BestTimestamp(
            proto.altitude_timestamp
        )
        self._speed_timestamp: BestTimestamp = BestTimestamp(proto.speed_timestamp)
        self._bearing_timestamp: BestTimestamp = BestTimestamp(proto.bearing_timestamp)

    @staticmethod
    def new() -> "BestLocation":
        """
        :return: A new, empty BestLocation instance
        """
        return BestLocation(RedvoxPacketM.Sensors.Location.BestLocation())

    def get_latitude_longitude_timestamp(self) -> BestTimestamp:
        """
        :return: Best timestamps associated with best latitude and longitude
        """
        return self._latitude_longitude_timestamp

    def set_latitude_longitude_timestamp(
        self, latitude_longitude_timestamp: BestTimestamp
    ) -> "BestLocation":
        """
        Sets the latitude/longitude best timestamp.
        :param latitude_longitude_timestamp: The BestTimestamp to set.
        :return: A modified instance of self.
        """
        common.check_type(latitude_longitude_timestamp, [BestTimestamp])
        self.get_proto().latitude_longitude_timestamp.CopyFrom(
            latitude_longitude_timestamp.get_proto()
        )
        self._latitude_longitude_timestamp = BestTimestamp(
            self.get_proto().latitude_longitude_timestamp
        )
        return self

    def get_altitude_timestamp(self) -> BestTimestamp:
        """
        :return: Best timestamps associated with best altitude
        """
        return self._altitude_timestamp

    def set_altitude_timestamp(
        self, altitude_timestamp: BestTimestamp
    ) -> "BestLocation":
        """
        Sets the altitude timestamp.
        :param altitude_timestamp: The BestTimestamp to set.
        :return: A modified instance of self.
        """
        common.check_type(altitude_timestamp, [BestTimestamp])
        self.get_proto().altitude_timestamp.CopyFrom(altitude_timestamp.get_proto())
        self._altitude_timestamp = BestTimestamp(self.get_proto().altitude_timestamp)
        return self

    def get_speed_timestamp(self) -> BestTimestamp:
        """
        :return: Best timestamps associated with best speed
        """
        return self._speed_timestamp

    def set_speed_timestamp(self, speed_timestamp: BestTimestamp) -> "BestLocation":
        """
        Sets the speed timestamp.
        :param speed_timestamp: The BestTimestamp to set.
        :return: A modified instance of self.
        """
        common.check_type(speed_timestamp, [BestTimestamp])
        self.get_proto().speed_timestamp.CopyFrom(speed_timestamp.get_proto())
        self._speed_timestamp = BestTimestamp(self.get_proto().speed_timestamp)
        return self

    def get_bearing_timestamp(self) -> BestTimestamp:
        """
        :return: Best timestamps associated with best bearing
        """
        return self._bearing_timestamp

    def set_bearing_timestamp(self, bearing_timestamp: BestTimestamp) -> "BestLocation":
        """
        Sets the bearing timestamp.
        :param bearing_timestamp: The BestTimestamp to set.
        :return: A modified instance of self.
        """
        common.check_type(bearing_timestamp, [BestTimestamp])
        self.get_proto().bearing_timestamp.CopyFrom(bearing_timestamp.get_proto())
        self._bearing_timestamp = BestTimestamp(self.get_proto().bearing_timestamp)
        return self

    def get_latitude_longitude_unit(self) -> common.Unit:
        """
        :return: Unit associated with latitude, longitude
        """
        # noinspection Mypy
        # pylint: disable=E1101
        return common.Unit.from_proto(self._proto.latitude_longitude_unit)

    def set_latitude_longitude_unit(self, unit: common.Unit) -> "BestLocation":
        """
        Sets the unit associated with latitude and longitude
        :param unit: Unit to set
        :return: A modified instance of self
        """
        redvox.api1000.common.typing.check_type(unit, [common.Unit])
        # noinspection Mypy
        self._proto.latitude_longitude_unit = unit.into_proto()
        return self

    def get_altitude_unit(self) -> common.Unit:
        """
        :return: Unit associated with altitude
        """
        # noinspection Mypy
        # pylint: disable=E1101
        return common.Unit.from_proto(self._proto.altitude_unit)

    def set_altitude_unit(self, unit: common.Unit) -> "BestLocation":
        """
        Sets the unit associated with altitude
        :param unit: Unit to set
        :return: A modified instance of self
        """
        redvox.api1000.common.typing.check_type(unit, [common.Unit])
        # noinspection Mypy
        self._proto.altitude_unit = unit.into_proto()
        return self

    def get_speed_unit(self) -> common.Unit:
        """
        :return: Unit associated with altitude
        """
        # noinspection Mypy
        # pylint: disable=E1101
        return common.Unit.from_proto(self._proto.speed_unit)

    def set_speed_unit(self, unit: common.Unit) -> "BestLocation":
        """
        Sets the unit associated with speed
        :param unit: Unit to set
        :return: A modified instance of self
        """
        redvox.api1000.common.typing.check_type(unit, [common.Unit])
        # noinspection Mypy
        self._proto.speed_unit = unit.into_proto()
        return self

    def get_bearing_unit(self) -> common.Unit:
        """
        :return: Unit associated with bearing
        """
        # noinspection Mypy
        # pylint: disable=E1101
        return common.Unit.from_proto(self._proto.bearing_unit)

    def set_bearing_unit(self, unit: common.Unit) -> "BestLocation":
        """
        Sets the unit associated with speed
        :param unit: Unit to set
        :return: A modified instance of self
        """
        redvox.api1000.common.typing.check_type(unit, [common.Unit])
        # noinspection Mypy
        self._proto.bearing_unit = unit.into_proto()
        return self

    def get_vertical_accuracy_unit(self) -> common.Unit:
        """
        :return: Unit associated with vertical accuracy
        """
        # noinspection Mypy
        # pylint: disable=E1101
        return common.Unit.from_proto(self._proto.vertical_accuracy_unit)

    def set_vertical_accuracy_unit(self, unit: common.Unit) -> "BestLocation":
        """
        Sets the unit associated with vertical accuracy
        :param unit: Unit to set
        :return: A modified instance of self
        """
        redvox.api1000.common.typing.check_type(unit, [common.Unit])
        # noinspection Mypy
        self._proto.vertical_accuracy_unit = unit.into_proto()
        return self

    def get_horizontal_accuracy_unit(self) -> common.Unit:
        """
        :return: Unit associated with horizontal accuracy
        """
        # noinspection Mypy
        # pylint: disable=E1101
        return common.Unit.from_proto(self._proto.horizontal_accuracy_unit)

    def set_horizontal_accuracy_unit(self, unit: common.Unit) -> "BestLocation":
        """
        Sets the unit associated with horizontal accuracy
        :param unit: Unit to set
        :return: A modified instance of self
        """
        redvox.api1000.common.typing.check_type(unit, [common.Unit])
        # noinspection Mypy
        self._proto.horizontal_accuracy_unit = unit.into_proto()
        return self

    def get_speed_accuracy_unit(self) -> common.Unit:
        """
        :return: Unit associated with speed accuracy
        """
        # noinspection Mypy
        # pylint: disable=E1101
        return common.Unit.from_proto(self._proto.speed_accuracy_unit)

    def set_speed_accuracy_unit(self, unit: common.Unit) -> "BestLocation":
        """
        Sets the unit associated with speed accuracy
        :param unit: Unit to set
        :return: A modified instance of self
        """
        redvox.api1000.common.typing.check_type(unit, [common.Unit])
        # noinspection Mypy
        self._proto.speed_accuracy_unit = unit.into_proto()
        return self

    def get_bearing_accuracy_unit(self) -> common.Unit:
        """
        :return: Unit associated with bearing accuracy
        """
        # noinspection Mypy
        # pylint: disable=E1101
        return common.Unit.from_proto(self._proto.bearing_accuracy_unit)

    def set_bearing_accuracy_unit(self, unit: common.Unit) -> "BestLocation":
        """
        Sets the unit associated with bearing accuracy
        :param unit: Unit to set
        :return: A modified instance of self
        """
        redvox.api1000.common.typing.check_type(unit, [common.Unit])
        # noinspection Mypy
        self._proto.bearing_accuracy_unit = unit.into_proto()
        return self

    def get_latitude(self) -> float:
        """
        :return: The best latitude
        """
        return self._proto.latitude

    def set_latitude(self, latitude: float) -> "BestLocation":
        """
        Sets the best latitude
        :param latitude: Latitude to set
        :return: A modified instance of self
        """
        redvox.api1000.common.typing.check_type(latitude, [int, float])
        self._proto.latitude = latitude
        return self

    def get_longitude(self) -> float:
        """
        :return: The best longitude
        """
        return self._proto.longitude

    def set_longitude(self, longitude: float) -> "BestLocation":
        """
        Sets the best longitude
        :param longitude: Longitude to set
        :return: A modified instance of self
        """
        redvox.api1000.common.typing.check_type(longitude, [int, float])
        self._proto.longitude = longitude
        return self

    def get_altitude(self) -> float:
        """
        :return: The best altitude
        """
        return self._proto.altitude

    def set_altitude(self, altitude: float) -> "BestLocation":
        """
        Sets the best altitude
        :param altitude: Altitude to set
        :return: A modified instance of self
        """
        redvox.api1000.common.typing.check_type(altitude, [int, float])
        self._proto.altitude = altitude
        return self

    def get_speed(self) -> float:
        """
        :return: The best speed
        """
        return self._proto.speed

    def set_speed(self, speed: float) -> "BestLocation":
        """
        Sets the best speed
        :param speed: Speed to set
        :return: A modified instance of self
        """
        redvox.api1000.common.typing.check_type(speed, [int, float])
        self._proto.speed = speed
        return self

    def get_bearing(self) -> float:
        """
        :return: The best bearing
        """
        return self._proto.bearing

    def set_bearing(self, bearing: float) -> "BestLocation":
        """
        Sets the best bearing
        :param bearing: Bearing to set
        :return: A modified instance of self
        """
        redvox.api1000.common.typing.check_type(bearing, [int, float])
        self._proto.bearing = bearing
        return self

    def get_vertical_accuracy(self) -> float:
        """
        :return: The best vertical accuracy
        """
        return self._proto.vertical_accuracy

    def set_vertical_accuracy(self, vertical_accuracy: float) -> "BestLocation":
        """
        Sets the best vertical accuracy.
        :param vertical_accuracy: Accuracy to set
        :return: A modified instance of self
        """
        redvox.api1000.common.typing.check_type(vertical_accuracy, [int, float])
        self._proto.vertical_accuracy = vertical_accuracy
        return self

    def get_horizontal_accuracy(self) -> float:
        """
        :return: The best horizontal accuracy
        """
        return self._proto.horizontal_accuracy

    def set_horizontal_accuracy(self, horizontal_accuracy: float) -> "BestLocation":
        """
        Sets the best horizontal accuracy
        :param horizontal_accuracy: Accuracy to set
        :return: A modified instance of self
        """
        redvox.api1000.common.typing.check_type(horizontal_accuracy, [int, float])
        self._proto.horizontal_accuracy = horizontal_accuracy
        return self

    def get_speed_accuracy(self) -> float:
        """
        :return: The best speed accuracy
        """
        return self._proto.speed_accuracy

    def set_speed_accuracy(self, speed_accuracy: float) -> "BestLocation":
        """
        Sets the best speed accuracy
        :param speed_accuracy: Accuracy to set
        :return: A modified instance of self
        """
        redvox.api1000.common.typing.check_type(speed_accuracy, [int, float])
        self._proto.speed_accuracy = speed_accuracy
        return self

    def get_bearing_accuracy(self) -> float:
        """
        :return: The best bearing accuracy
        """
        return self._proto.bearing_accuracy

    def set_bearing_accuracy(self, bearing_accuracy: float) -> "BestLocation":
        """
        Sets the best bearing accuracy
        :param bearing_accuracy: Accuracy to set
        :return: A modified instance of self
        """
        redvox.api1000.common.typing.check_type(bearing_accuracy, [int, float])
        self._proto.bearing_accuracy = bearing_accuracy
        return self

    def get_score(self) -> float:
        """
        :return: The best location score
        """
        return self._proto.score

    def set_score(self, score: float) -> "BestLocation":
        """
        Sets the best location score
        :param score: Score to set
        :return: A modified instance of self
        """
        redvox.api1000.common.typing.check_type(score, [int, float])
        self._proto.score = score
        return self

    def get_method(self) -> LocationScoreMethod:
        """
        :return: The best location score method
        """
        # noinspection Mypy
        # pylint: disable=E1101
        return LocationScoreMethod.from_proto(self._proto.method)

    def set_method(self, method: LocationScoreMethod) -> "BestLocation":
        """
        Sets the best location score method.
        :param method: Method to set
        :return: A modified instance of self
        """
        redvox.api1000.common.typing.check_type(method, [LocationScoreMethod])
        # noinspection Mypy
        self._proto.method = method.into_proto()
        return self

    def get_location_provider(self) -> LocationProvider:
        """
        :return: The location provide associated with the best location.
        """
        # noinspection Mypy
        # pylint: disable=E1101
        return LocationProvider.from_proto(self._proto.location_provider)

    def set_location_provider(
        self, location_provider: LocationProvider
    ) -> "BestLocation":
        """
        Sets the location provider associated with the best location.
        :param location_provider: Location provider to set.
        :return: A modified instance of self
        """
        redvox.api1000.common.typing.check_type(location_provider, [LocationProvider])
        # noinspection Mypy
        self._proto.location_provider = location_provider.into_proto()
        return self


class Location(redvox.api1000.common.generic.ProtoBase[RedvoxPacketM.Sensors.Location]):
    """
    Encapsulates location data and metadata
    """

    def __init__(self, proto: RedvoxPacketM.Sensors.Location):
        super().__init__(proto)
        self._timestamps: common.TimingPayload = common.TimingPayload(proto.timestamps)
        self._timestamps_gps: common.TimingPayload = common.TimingPayload(
            proto.timestamps_gps
        )
        self._latitude_samples: common.SamplePayload = common.SamplePayload(
            proto.latitude_samples
        )
        self._longitude_samples: common.SamplePayload = common.SamplePayload(
            proto.longitude_samples
        )
        self._altitude_samples: common.SamplePayload = common.SamplePayload(
            proto.altitude_samples
        )
        self._speed_samples: common.SamplePayload = common.SamplePayload(
            proto.speed_samples
        )
        self._bearing_samples: common.SamplePayload = common.SamplePayload(
            proto.bearing_samples
        )
        self._horizontal_accuracy_samples: common.SamplePayload = common.SamplePayload(
            proto.horizontal_accuracy_samples
        )
        self._vertical_accuracy_samples: common.SamplePayload = common.SamplePayload(
            proto.vertical_accuracy_samples
        )
        self._speed_accuracy_samples: common.SamplePayload = common.SamplePayload(
            proto.speed_accuracy_samples
        )
        self._bearing_accuracy_samples: common.SamplePayload = common.SamplePayload(
            proto.bearing_accuracy_samples
        )
        self._last_best_location: BestLocation = BestLocation(proto.last_best_location)
        self._overall_best_location: BestLocation = BestLocation(
            proto.overall_best_location
        )
        # noinspection Mypy
        # pylint: disable=E1101
        self._location_providers: ProtoRepeatedMessage = ProtoRepeatedMessage(
            proto,
            proto.location_providers,
            "location_providers",
            LocationProvider.from_proto,
            LocationProvider.into_proto,
        )

    @staticmethod
    def new() -> "Location":
        """
        :return: A new, empty Location instance
        """
        return Location(RedvoxPacketM.Sensors.Location())

    def get_sensor_description(self) -> str:
        """
        :return: The location sensor description
        """
        return self._proto.sensor_description

    def set_sensor_description(self, sensor_description: str) -> "Location":
        """
        Sets the location sensor's description
        :param sensor_description: Description to set
        :return: A modified instance of self
        """
        redvox.api1000.common.typing.check_type(sensor_description, [str])
        self._proto.sensor_description = sensor_description
        return self

    def get_timestamps(self) -> common.TimingPayload:
        """
        :return: The timing payload (machine timestamps) associated with this sensor's location samples
        """
        return self._timestamps

    def set_timestamps(self, timestamps: common.TimingPayload) -> "Location":
        """
        Sets the timestamps.
        :param timestamps: Timing payload to set.
        :return: A modified instance of self.
        """
        common.check_type(timestamps, [common.TimingPayload])
        self.get_proto().timestamps.CopyFrom(timestamps.get_proto())
        self._timestamps = common.TimingPayload(self.get_proto().timestamps)
        return self

    def get_timestamps_gps(self) -> common.TimingPayload:
        """
        :return: The timing payload (gps timestamps) associated with this sensor's location samples
        """
        return self._timestamps_gps

    def set_timestamps_gps(self, timestamps_gps: common.TimingPayload) -> "Location":
        """
        Sets the GPS timing samples.
        :param timestamps_gps: Payload to set.
        :return: A modified instance of self.
        """
        common.check_type(timestamps_gps, [common.TimingPayload])
        self.get_proto().timestamps_gps.CopyFrom(timestamps_gps.get_proto())
        self._timestamps_gps = common.TimingPayload(self.get_proto().timestamps_gps)
        return self

    def get_latitude_samples(self) -> common.SamplePayload:
        """
        :return: The SamplePayload containing latitude samples and statistics
        """
        return self._latitude_samples

    def set_latitude_samples(
        self, latitude_samples: common.SamplePayload
    ) -> "Location":
        """
        Sets the latitude samples.
        :param latitude_samples: Payload top set.
        :return: A modified instance of self.
        """
        common.check_type(latitude_samples, [common.SamplePayload])
        # noinspection Mypy
        self.get_proto().latitude_samples.CopyFrom(latitude_samples.get_proto())
        self._latitude_samples = common.SamplePayload(self.get_proto().latitude_samples)
        return self

    def get_longitude_samples(self) -> common.SamplePayload:
        """
        :return: The SamplePayload containing longitude samples and statistics
        """
        return self._longitude_samples

    def set_longitude_samples(
        self, longitude_samples: common.SamplePayload
    ) -> "Location":
        """
        Sets the longitude samples.
        :param longitude_samples: Payload to set.
        :return: A modified instance of self.
        """
        common.check_type(longitude_samples, [common.SamplePayload])
        # noinspection Mypy
        self.get_proto().longitude_samples.CopyFrom(longitude_samples.get_proto())
        self._longitude_samples = common.SamplePayload(
            self.get_proto().longitude_samples
        )
        return self

    def get_altitude_samples(self) -> common.SamplePayload:
        """
        :return: The SamplePayload containing altitude samples and statistics
        """
        return self._altitude_samples

    def set_altitude_samples(
        self, altitude_samples: common.SamplePayload
    ) -> "Location":
        """
        Sets the altitude samples.
        :param altitude_samples: Payload to set.
        :return: A modified instance of self.
        """
        common.check_type(altitude_samples, [common.SamplePayload])
        # noinspection Mypy
        self.get_proto().altitude_samples.CopyFrom(altitude_samples.get_proto())
        self._altitude_samples = common.SamplePayload(self.get_proto().altitude_samples)
        return self

    def get_speed_samples(self) -> common.SamplePayload:
        """
        :return: The SamplePayload containing speed samples and statistics
        """
        return self._speed_samples

    def set_speed_samples(self, speed_samples: common.SamplePayload) -> "Location":
        """
        Sets the speed samples.
        :param speed_samples: Payload to set.
        :return: A modified instance of self.
        """
        common.check_type(speed_samples, [common.SamplePayload])
        # noinspection Mypy
        self.get_proto().speed_samples.CopyFrom(speed_samples.get_proto())
        self._speed_samples = common.SamplePayload(self.get_proto().speed_samples)
        return self

    def get_bearing_samples(self) -> common.SamplePayload:
        """
        :return: The SamplePayload containing bearing samples and statistics
        """
        return self._bearing_samples

    def set_bearing_samples(self, bearing_samples: common.SamplePayload) -> "Location":
        """
        Sets the bearing samples.
        :param bearing_samples: Payload to set.
        :return: A modified instance of self.
        """
        common.check_type(bearing_samples, [common.SamplePayload])
        # noinspection Mypy
        self.get_proto().bearing_samples.CopyFrom(bearing_samples.get_proto())
        self._bearing_samples = common.SamplePayload(self.get_proto().bearing_samples)
        return self

    def get_horizontal_accuracy_samples(self) -> common.SamplePayload:
        """
        :return: The SamplePayload containing horizontal accuracy samples and statistics
        """
        return self._horizontal_accuracy_samples

    def set_horizontal_accuracy_samples(
        self, horizontal_accuracy_samples: common.SamplePayload
    ) -> "Location":
        """
        Sets the horizontal accuracy samples.
        :param horizontal_accuracy_samples: Payload to set.
        :return: A modified instance of self.
        """
        common.check_type(horizontal_accuracy_samples, [common.SamplePayload])
        # noinspection Mypy
        self.get_proto().horizontal_accuracy_samples.CopyFrom(
            horizontal_accuracy_samples.get_proto()
        )
        self._horizontal_accuracy_samples = common.SamplePayload(
            self.get_proto().horizontal_accuracy_samples
        )
        return self

    def get_vertical_accuracy_samples(self) -> common.SamplePayload:
        """
        :return: The SamplePayload containing vertical accuracy samples and statistics
        """
        return self._vertical_accuracy_samples

    def set_vertical_accuracy_samples(
        self, vertical_accuracy_samples: common.SamplePayload
    ) -> "Location":
        """
        Sets the vertical accuracy samples.
        :param vertical_accuracy_samples: Payload to set.
        :return: A modified instance of self.
        """
        common.check_type(vertical_accuracy_samples, [common.SamplePayload])
        # noinspection Mypy
        self.get_proto().vertical_accuracy_samples.CopyFrom(
            vertical_accuracy_samples.get_proto()
        )
        self._vertical_accuracy_samples = common.SamplePayload(
            self.get_proto().vertical_accuracy_samples
        )
        return self

    def get_speed_accuracy_samples(self) -> common.SamplePayload:
        """
        :return: The SamplePayload containing speed accuracy samples and statistics
        """
        return self._speed_accuracy_samples

    def set_speed_accuracy_samples(
        self, speed_accuracy_samples: common.SamplePayload
    ) -> "Location":
        """
        Sets the speed accuracy samples.
        :param speed_accuracy_samples: Payload to set.
        :return: A modified instance of self.
        """
        common.check_type(speed_accuracy_samples, [common.SamplePayload])
        # noinspection Mypy
        self.get_proto().speed_accuracy_samples.CopyFrom(
            speed_accuracy_samples.get_proto()
        )
        self._speed_accuracy_samples = common.SamplePayload(
            self.get_proto().speed_accuracy_samples
        )
        return self

    def get_bearing_accuracy_samples(self) -> common.SamplePayload:
        """
        :return: The SamplePayload containing bearing accuracy samples and statistics
        """
        return self._bearing_accuracy_samples

    def set_bearing_accuracy_samples(
        self, bearing_accuracy_samples: common.SamplePayload
    ) -> "Location":
        """
        Sets the samples for the bearing accuracy channel.
        :param bearing_accuracy_samples: Samples to set.
        :return: A modified instance of self.
        """
        common.check_type(bearing_accuracy_samples, [common.SamplePayload])
        # noinspection Mypy
        self.get_proto().bearing_accuracy_samples.CopyFrom(
            bearing_accuracy_samples.get_proto()
        )
        self._bearing_accuracy_samples = common.SamplePayload(
            self.get_proto().bearing_accuracy_samples
        )
        return self

    def get_last_best_location(self) -> BestLocation:
        """
        :return: This returns the most recent BestLocation
        """
        return self._last_best_location

    def set_last_best_location(self, last_best_location: BestLocation) -> "Location":
        """
        Sets the most recent best location.
        :param last_best_location:  The most recent best location to set.
        :return: A modified instance of self.
        """
        common.check_type(last_best_location, [BestLocation])
        self.get_proto().last_best_location.CopyFrom(last_best_location.get_proto())
        self._last_best_location = BestLocation(self.get_proto().last_best_location)
        return self

    def get_overall_best_location(self) -> BestLocation:
        """
        :return: This returns the overall best location since the station last moved
        """
        return self._overall_best_location

    def set_overall_best_location(
        self, overall_best_location: BestLocation
    ) -> "Location":
        """
        Sets the overall best location.
        :param overall_best_location: BestLocation to set.
        :return: A modified instance of self.
        """
        common.check_type(overall_best_location, [BestLocation])
        self.get_proto().overall_best_location.CopyFrom(
            overall_best_location.get_proto()
        )
        self._overall_best_location = BestLocation(
            self.get_proto().overall_best_location
        )
        return self

    def get_location_permissions_granted(self) -> bool:
        """
        :return: Have location permissions been granted?
        """
        return self._proto.location_permissions_granted

    def set_location_permissions_granted(
        self, location_permissions_granted: bool
    ) -> "Location":
        """
        Sets if location permissions have been granted.
        :param location_permissions_granted: Permissions to set
        :return: A modified instance of self
        """
        redvox.api1000.common.typing.check_type(location_permissions_granted, [bool])
        self._proto.location_permissions_granted = location_permissions_granted
        return self

    def get_location_services_requested(self) -> bool:
        """
        :return: Have location services been requested by the user?
        """
        return self._proto.location_services_requested

    def set_location_services_requested(
        self, location_services_requested: bool
    ) -> "Location":
        """
        Sets if location services have been requested.
        :param location_services_requested:
        :return:
        """
        redvox.api1000.common.typing.check_type(location_services_requested, [bool])
        self._proto.location_services_requested = location_services_requested
        return self

    def get_location_services_enabled(self) -> bool:
        """
        :return: If location services are enabled.
        """
        return self._proto.location_services_enabled

    def set_location_services_enabled(
        self, location_services_enabled: bool
    ) -> "Location":
        """
        Sets if location servers are enabled.
        :param location_services_enabled: Set enabled or disabled
        :return: Modified version of self
        """
        redvox.api1000.common.typing.check_type(location_services_enabled, [bool])
        self._proto.location_services_enabled = location_services_enabled
        return self

    def get_location_providers(self) -> ProtoRepeatedMessage:
        """
        :return: A list of location providers associated with each location sample
        """
        return self._location_providers

    def set_location_providers(
        self, location_providers: ProtoRepeatedMessage
    ) -> "Location":
        """
        Sets the location provides.
        :param location_providers: An instance of a ProtoRepeatedMessage containing the location providers.
        :return: A modified instance of self.
        """
        common.check_type(location_providers, [ProtoRepeatedMessage])
        self._location_providers.clear_values()
        self._location_providers.append_values(location_providers.get_values())
        return self

    def is_only_best_values(self) -> bool:
        """
        :return: True if the location does not have data in it and has a last_best_location or overall_best_location
        """
        return self.get_location_providers().get_count() < 1 and (
            self.get_last_best_location() is not None
            or self.get_overall_best_location() is not None
        )


def validate_location(loc_sensor: Location) -> List[str]:
    """
    Validates the location
    :param loc_sensor: Location to validate
    :return: A list of validation errors
    """
    errors_list = validate_best_location(loc_sensor.get_last_best_location())
    errors_list.extend(validate_best_location(loc_sensor.get_overall_best_location()))

    if loc_sensor.is_only_best_values():
        return errors_list

    errors_list.extend(common.validate_timing_payload(loc_sensor.get_timestamps()))

    errors_list.extend(
        common.validate_sample_payload(loc_sensor.get_latitude_samples(), "Latitude", common.Unit.DECIMAL_DEGREES)
    )

    if any(loc_sensor.get_latitude_samples().get_values() < -90) \
            or any(loc_sensor.get_latitude_samples().get_values() > 90):
        errors_list.append("Location sensor latitude value is beyond valid range")

    errors_list.extend(
        common.validate_sample_payload(loc_sensor.get_longitude_samples(), "Longitude", common.Unit.DECIMAL_DEGREES)
    )

    if any(loc_sensor.get_longitude_samples().get_values() < -180) \
            or any(loc_sensor.get_longitude_samples().get_values() > 180):
        errors_list.append("Location sensor longitude value is beyond valid range")

    if loc_sensor.get_altitude_samples().get_unit() != common.Unit.METERS:
        errors_list.append("Location sensor altitude units are not meters")

    if loc_sensor.get_speed_samples().get_unit() != common.Unit.METERS_PER_SECOND:
        errors_list.append("Location sensor speed units are not meters per second")

    if loc_sensor.get_bearing_samples().get_unit() != common.Unit.DECIMAL_DEGREES:
        errors_list.append("Location sensor bearing units are not decimal degrees")

    if loc_sensor.get_horizontal_accuracy_samples().get_unit() != common.Unit.METERS:
        errors_list.append("Location sensor horizontal accuracy units are not meters")

    if loc_sensor.get_vertical_accuracy_samples().get_unit() != common.Unit.METERS:
        errors_list.append("Location sensor vertical accuracy units are not meters")

    if loc_sensor.get_speed_accuracy_samples().get_unit() != common.Unit.METERS_PER_SECOND:
        errors_list.append(
            "Location sensor speed accuracy units are not meters per second"
        )

    if loc_sensor.get_bearing_accuracy_samples().get_unit() != common.Unit.DECIMAL_DEGREES:
        errors_list.append(
            "Location sensor bearing accuracy units are not decimal degrees"
        )

    return errors_list


def validate_best_location(best_loc: BestLocation) -> List[str]:
    """
    Validates the best location
    :param best_loc: Best Location to validate
    :return: A list of validation errors
    """
    errors_list = []

    if best_loc.get_latitude_longitude_timestamp().get_unit() != common.Unit.UNKNOWN:
        if best_loc.get_latitude_longitude_timestamp().get_unit() != common.Unit.MICROSECONDS_SINCE_UNIX_EPOCH:
            errors_list.append(
                "Best location latitude and longitude timestamp is not in microseconds since unix epoch"
            )

        if best_loc.get_latitude_longitude_unit() != common.Unit.DECIMAL_DEGREES:
            errors_list.append(
                "Best location latitude and longitude units are not decimal degrees"
            )

        if best_loc.get_latitude() < -90 or best_loc.get_latitude() > 90:
            errors_list.append("Best location latitude value is beyond valid range")

        if best_loc.get_longitude() < -180 or best_loc.get_longitude() > 180:
            errors_list.append("Best location longitude value is beyond valid range")

        if best_loc.get_altitude_timestamp().get_unit() \
                not in [common.Unit.MICROSECONDS_SINCE_UNIX_EPOCH, common.Unit.UNKNOWN]:
            errors_list.append(
                "Best location altitude timestamp is not in microseconds since unix epoch"
            )

        if best_loc.get_altitude_unit() not in [common.Unit.METERS, common.Unit.UNKNOWN]:
            errors_list.append("Best location altitude units are not meters")

        if best_loc.get_speed_timestamp().get_unit() \
                not in [common.Unit.MICROSECONDS_SINCE_UNIX_EPOCH, common.Unit.UNKNOWN]:
            errors_list.append(
                "Best location speed timestamp is not in microseconds since unix epoch"
            )

        if best_loc.get_speed_unit() not in [common.Unit.METERS_PER_SECOND, common.Unit.UNKNOWN]:
            errors_list.append("Best location speed units are not meters per second")

        if best_loc.get_bearing_timestamp().get_unit() \
                not in [common.Unit.MICROSECONDS_SINCE_UNIX_EPOCH, common.Unit.UNKNOWN]:
            errors_list.append(
                "Best location bearing timestamp is not in microseconds since unix epoch"
            )

        if best_loc.get_bearing_unit() not in [common.Unit.DECIMAL_DEGREES, common.Unit.UNKNOWN]:
            errors_list.append("Best location bearing units are not decimal degrees")

        if best_loc.get_horizontal_accuracy_unit() not in [common.Unit.METERS, common.Unit.UNKNOWN]:
            errors_list.append("Best location horizontal accuracy units are not meters")

        if best_loc.get_vertical_accuracy_unit() not in [common.Unit.METERS, common.Unit.UNKNOWN]:
            errors_list.append("Best location vertical accuracy units are not meters")

        if best_loc.get_speed_accuracy_unit() not in [common.Unit.METERS_PER_SECOND, common.Unit.UNKNOWN]:
            errors_list.append(
                "Best location speed accuracy units are not meters per second"
            )

        if best_loc.get_bearing_accuracy_unit() not in [common.Unit.DECIMAL_DEGREES, common.Unit.UNKNOWN]:
            errors_list.append(
                "Best location bearing accuracy units are not decimal degrees"
            )

        if (
            best_loc.get_location_provider()
            not in LocationProvider.__members__.values()
        ):
            errors_list.append("Best location provider is not valid")

    return errors_list
