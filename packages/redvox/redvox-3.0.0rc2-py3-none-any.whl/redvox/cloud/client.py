"""
This module contains the RedVox Cloud API client.

This client provides convenient access to RedVox metadata and data. This client manages the tedious business of keeping
an up-to-date authentication token for making authenticated API requests.
"""

import contextlib
import threading
from typing import List, Optional, Tuple

import requests

import redvox.cloud.api as api
import redvox.cloud.auth_api as auth_api
from redvox.cloud.config import RedVoxConfig
import redvox.cloud.errors as cloud_errors
import redvox.common.constants as constants
import redvox.cloud.data_api as data_api
import redvox.cloud.metadata_api as metadata_api
import redvox.cloud.station_stats as station_stats_api


def chunk_time_range(
    start_ts: int, end_ts: int, max_chunk: int
) -> List[Tuple[int, int]]:
    """
    Chunks the given request window into smaller windows.
    :param start_ts: Start of the request window.
    :param end_ts: End of the request window.
    :param max_chunk: Max chunk size.
    :return: A list of window chunks.
    """

    if end_ts <= start_ts:
        raise cloud_errors.CloudApiError("start_ts must be < end_ts")

    if max_chunk <= 0:
        raise cloud_errors.CloudApiError("max_chunk must be > 0")

    chunks: List[Tuple[int, int]] = []

    start: int = start_ts

    while start + max_chunk < end_ts:
        chunks.append((start, start + max_chunk))
        start += max_chunk

    if start < end_ts:
        chunks.append((start, end_ts))

    return chunks


class CloudClient:
    """
    The RedVox Cloud API client.
    """

    def __init__(
        self,
        redvox_config: Optional[RedVoxConfig] = RedVoxConfig.find(),
        refresh_token_interval: float = 600.0,
        timeout: Optional[float] = 10.0,
    ):
        """
        Instantiates this client.
        :param redvox_config: The Redvox endpoint configuration.
        :param refresh_token_interval: An optional interval in seconds that the auth token should be refreshed.
        :param timeout: An optional timeout
        """

        if redvox_config is None:
            raise cloud_errors.CloudApiError(
                "A RedVoxConfig was not found in the environment and one wasn't provided"
            )

        if refresh_token_interval <= 0:
            raise cloud_errors.CloudApiError(
                "refresh_token_interval must be strictly > 0"
            )

        if timeout is not None and (timeout <= 0):
            raise cloud_errors.CloudApiError("timeout must be strictly > 0")

        self.redvox_config: RedVoxConfig = redvox_config
        self.refresh_token_interval: float = refresh_token_interval
        self.timeout: Optional[float] = timeout

        self.__session = (
            requests.Session()
        )  # This must be initialized before the auth req!
        try:
            auth_resp: auth_api.AuthResp = self.authenticate_user(
                redvox_config.username, redvox_config.password
            )
        except cloud_errors.ApiConnectionError as ex:
            self.close()
            raise ex

        self.__refresh_timer = None
        if (
            auth_resp.status != 200
            or auth_resp.auth_token is None
            or len(auth_resp.auth_token) == 0
        ):
            self.close()
            raise cloud_errors.AuthenticationError()

        self.auth_token: str = auth_resp.auth_token

        self.__refresh_timer = threading.Timer(
            self.refresh_token_interval, self.__refresh_token
        )
        self.__refresh_timer.start()

    def __refresh_token(self):
        """
        Automatically refreshes this client's auth token in the background once per minute.
        """
        # pylint: disable=W0702
        # noinspection PyBroadException
        try:
            self.auth_token = self.refresh_own_auth_token().auth_token
            self.__refresh_timer = threading.Timer(
                self.refresh_token_interval, self.__refresh_token
            )
            self.__refresh_timer.start()
        except:
            self.close()

    def close(self):
        """
        Terminates this client process by cancelling the refresh token timer.
        """
        # pylint: disable=W0702
        # noinspection PyBroadException
        try:
            if self.__refresh_timer is not None:
                self.__refresh_timer.cancel()
        except:
            pass

        # pylint: disable=W0702
        # noinspection PyBroadException
        try:
            if self.__session is not None:
                self.__session.close()
        except:
            pass

    def health_check(self) -> bool:
        """
        An API call that returns True if the API Cloud server is up and running or False otherwise.
        :return: True if the API Cloud server is up and running or False otherwise.
        """
        return api.health_check(
            self.redvox_config, session=self.__session, timeout=self.timeout
        )

    def authenticate_user(self, username: str, password: str) -> auth_api.AuthResp:
        """
        Attempts to authenticate the given RedVox user.
        :param username: The RedVox username.
        :param password: The RedVox password.
        :return: An authenticate response.
        """
        if len(username) == 0:
            raise cloud_errors.CloudApiError("Username must be provided")

        if len(password) == 0:
            raise cloud_errors.CloudApiError("Password must be provided")

        auth_req: auth_api.AuthReq = auth_api.AuthReq(username, password)
        return auth_api.authenticate_user(
            self.redvox_config, auth_req, session=self.__session, timeout=self.timeout
        )

    def validate_auth_token(
        self, auth_token: str
    ) -> Optional[auth_api.ValidateTokenResp]:
        """
        Validates the provided authentication token with the cloud API.
        :param auth_token: Authentication token to validate.
        :return: An authentication response with token details or None if token in invalid
        """
        if len(auth_token) == 0:
            raise cloud_errors.CloudApiError("auth_token must be provided")

        token_req: auth_api.ValidateTokenReq = auth_api.ValidateTokenReq(auth_token)
        return auth_api.validate_token(
            self.redvox_config, token_req, session=self.__session, timeout=self.timeout
        )

    def validate_own_auth_token(self) -> Optional[auth_api.ValidateTokenResp]:
        """
        Validates the current token held by this client.
        :return: An authentication response with token details or None if token in invalid
        """
        return self.validate_auth_token(self.auth_token)

    def refresh_auth_token(
        self, auth_token: str
    ) -> Optional[auth_api.RefreshTokenResp]:
        """
        Retrieves a new authentication token from a given valid authentication token.
        :param auth_token: The authentication token to verify.
        :return: A new authentication token or None if the provide auth token is not valid.
        """
        if len(auth_token) == 0:
            raise cloud_errors.CloudApiError("auth_token must be provided")

        refresh_token_req: auth_api.RefreshTokenReq = auth_api.RefreshTokenReq(
            auth_token
        )
        return auth_api.refresh_token(
            self.redvox_config,
            refresh_token_req,
            session=self.__session,
            timeout=self.timeout,
        )

    def refresh_own_auth_token(self) -> Optional[auth_api.RefreshTokenResp]:
        """
        Retrieves a new authentication token using the token held by this client as a reference.
        :return: A new authentication token or None if the provide auth token is not valid.
        """
        return self.refresh_auth_token(self.auth_token)

    def request_metadata(
        self,
        start_ts_s: int,
        end_ts_s: int,
        station_ids: List[str],
        metadata_to_include: List[str],
        chunk_by_seconds: int = constants.SECONDS_PER_DAY,
    ) -> Optional[metadata_api.MetadataResp]:
        """
        Requests RedVox packet metadata.
        :param start_ts_s: Start epoch of request window.
        :param end_ts_s: End epoch of request window.
        :param station_ids: A list of station ids.
        :param metadata_to_include: A list of metadata fields to include (see: redvox.cloud.metadata.AvailableMetadata)
        :param chunk_by_seconds: Split up longer requests into chunks of chunk_by_seconds size (default 86400s/1d)
        :return: A metadata result containing the requested metadata or None on error.
        """
        if end_ts_s <= start_ts_s:
            raise cloud_errors.CloudApiError("start_ts_s must be < end_ts_s")

        if len(station_ids) == 0:
            raise cloud_errors.CloudApiError("At least one station_id must be included")

        if len(metadata_to_include) == 0:
            raise cloud_errors.CloudApiError(
                "At least one metadata field must be included"
            )

        if chunk_by_seconds <= 0:
            raise cloud_errors.CloudApiError("chunk_by_seconds must be > 0")

        time_chunks: List[Tuple[int, int]] = chunk_time_range(
            start_ts_s, end_ts_s, chunk_by_seconds
        )
        metadata_resp: metadata_api.MetadataResp = metadata_api.MetadataResp([])

        for start_ts, end_ts in time_chunks:
            metadata_req: metadata_api.MetadataReq = metadata_api.MetadataReq(
                self.auth_token,
                start_ts,
                end_ts,
                station_ids,
                metadata_to_include,
                self.redvox_config.secret_token,
            )

            chunked_resp: Optional[
                metadata_api.MetadataResp
            ] = metadata_api.request_metadata(
                self.redvox_config,
                metadata_req,
                session=self.__session,
                timeout=self.timeout,
            )

            if chunked_resp:
                metadata_resp.metadata.extend(chunked_resp.metadata)

        return metadata_resp

    def request_metadata_m(
        self,
        start_ts_s: int,
        end_ts_s: int,
        station_ids: List[str],
        metadata_to_include: List[str],
        chunk_by_seconds: int = constants.SECONDS_PER_DAY,
    ) -> Optional[metadata_api.MetadataRespM]:
        """
        Requests RedVox packet metadata.
        :param start_ts_s: Start epoch of request window.
        :param end_ts_s: End epoch of request window.
        :param station_ids: A list of station ids.
        :param metadata_to_include: A list of metadata fields to include (see: redvox.cloud.metadata.AvailableMetadata)
        :param chunk_by_seconds: Split up longer requests into chunks of chunk_by_seconds size (default 86400s/1d)
        :return: A metadata result containing the requested metadata or None on error.
        """
        if end_ts_s <= start_ts_s:
            raise cloud_errors.CloudApiError("start_ts_s must be < end_ts_s")

        if len(station_ids) == 0:
            raise cloud_errors.CloudApiError("At least one station_id must be included")

        if len(metadata_to_include) == 0:
            raise cloud_errors.CloudApiError(
                "At least one metadata field must be included"
            )

        if chunk_by_seconds <= 0:
            raise cloud_errors.CloudApiError("chunk_by_seconds must be > 0")

        time_chunks: List[Tuple[int, int]] = chunk_time_range(
            start_ts_s, end_ts_s, chunk_by_seconds
        )
        metadata_resp: metadata_api.MetadataRespM = metadata_api.MetadataRespM([])

        for start_ts, end_ts in time_chunks:
            metadata_req: metadata_api.MetadataReq = metadata_api.MetadataReq(
                self.auth_token,
                start_ts,
                end_ts,
                station_ids,
                metadata_to_include,
                self.redvox_config.secret_token,
            )

            chunked_resp: Optional[
                metadata_api.MetadataRespM
            ] = metadata_api.request_metadata_m(
                self.redvox_config,
                metadata_req,
                session=self.__session,
                timeout=self.timeout,
            )

            if chunked_resp:
                metadata_resp.db_packets.extend(chunked_resp.db_packets)

        return metadata_resp

    def request_timing_metadata(
        self,
        start_ts_s: int,
        end_ts_s: int,
        station_ids: List[str],
        chunk_by_seconds: int = constants.SECONDS_PER_DAY,
    ) -> metadata_api.TimingMetaResponse:
        """
        Requests timing metadata from RedVox packets.
        :param start_ts_s: Start epoch of the request.
        :param end_ts_s: End epoch of the request.
        :param station_ids: A list of station ids.
        :param chunk_by_seconds: Split up longer requests into chunks of chunk_by_seconds size (default 86400s/1d)
        :return: A response containing the requested metadata.
        """
        if end_ts_s <= start_ts_s:
            raise cloud_errors.CloudApiError("start_ts_s must be < end_ts_s")

        if len(station_ids) == 0:
            raise cloud_errors.CloudApiError("At least one station_id must be included")

        if chunk_by_seconds <= 0:
            raise cloud_errors.CloudApiError("chunk_by_seconds must be > 0")

        time_chunks: List[Tuple[int, int]] = chunk_time_range(
            start_ts_s, end_ts_s, chunk_by_seconds
        )
        metadata_resp: metadata_api.TimingMetaResponse = (
            metadata_api.TimingMetaResponse([])
        )

        for start_ts, end_ts in time_chunks:
            timing_req: metadata_api.TimingMetaRequest = metadata_api.TimingMetaRequest(
                self.auth_token,
                start_ts,
                end_ts,
                station_ids,
                self.redvox_config.secret_token,
            )
            chunked_resp: metadata_api.TimingMetaResponse = (
                metadata_api.request_timing_metadata(
                    self.redvox_config,
                    timing_req,
                    session=self.__session,
                    timeout=self.timeout,
                )
            )

            if chunked_resp:
                metadata_resp.items.extend(chunked_resp.items)

        return metadata_resp

    def request_report_data(self, report_id: str) -> Optional[data_api.ReportDataResp]:
        """
        Requests a signed URL for a given report ID.
        :param report_id: The report ID to request data for.
        :return: A response containing a signed URL of the report data.
        """
        if len(report_id) == 0:
            raise cloud_errors.CloudApiError("report_id must be included")

        report_data_req: data_api.ReportDataReq = data_api.ReportDataReq(
            self.auth_token, report_id, self.redvox_config.secret_token
        )
        return data_api.request_report_data(
            self.redvox_config,
            report_data_req,
            session=self.__session,
            timeout=self.timeout,
        )

    def request_station_statuses(
        self,
        start_ts_s: int,
        end_ts_s: int,
        station_ids: List[str],
    ) -> Optional[metadata_api.StationStatusResp]:
        """
        Requests station timing information from the cloud services.
        :param start_ts_s: The start of the request data window.
        :param end_ts_s: The end of the request data window.
        :param station_ids: A list of station IDs.
        :return: A StationStatsResp.
        """
        if end_ts_s <= start_ts_s:
            raise cloud_errors.CloudApiError("start_ts_s must be < end_ts_s")

        station_status_req: metadata_api.StationStatusReq = (
            metadata_api.StationStatusReq(
                self.redvox_config.secret_token,
                self.auth_token,
                start_ts_s,
                end_ts_s,
                station_ids,
            )
        )

        return metadata_api.request_station_statuses(
            self.redvox_config,
            station_status_req,
            session=self.__session,
            timeout=self.timeout,
        )

    def request_data_range(
        self,
        start_ts_s: int,
        end_ts_s: int,
        station_ids: List[str],
        req_type: data_api.DataRangeReqType = data_api.DataRangeReqType.API_900,
    ) -> data_api.DataRangeResp:
        """
        Request signed URLs for RedVox packets.
        :param start_ts_s: The start epoch of the window.
        :param end_ts_s:  The end epoch of the window.
        :param station_ids: A list of station ids.
        :param req_type: The type of data to request.
        :return: A response containing a list of signed URLs for the RedVox packets.
        """
        if end_ts_s <= start_ts_s:
            raise cloud_errors.CloudApiError("start_ts_s must be < end_ts_s")

        if len(station_ids) == 0:
            raise cloud_errors.CloudApiError("At least one station_id must be provided")

        data_range_req: data_api.DataRangeReq = data_api.DataRangeReq(
            self.auth_token,
            start_ts_s,
            end_ts_s,
            station_ids,
            self.redvox_config.secret_token,
        )

        return data_api.request_range_data(
            self.redvox_config,
            data_range_req,
            session=self.__session,
            timeout=self.timeout,
            req_type=req_type,
        )

    def request_station_stats(
        self,
        start_ts_s: int,
        end_ts_s: int,
        station_ids: List[str],
    ) -> Optional[station_stats_api.StationStatsResp]:
        """
        Request signed URLs for RedVox packets.
        :param start_ts_s: The start epoch of the window.
        :param end_ts_s:  The end epoch of the window.
        :param station_ids: A list of station ids.
        :return: A response containing a list of signed URLs for the RedVox packets.
        """
        if end_ts_s <= start_ts_s:
            raise cloud_errors.CloudApiError("start_ts_s must be < end_ts_s")

        if len(station_ids) == 0:
            raise cloud_errors.CloudApiError("At least one station_id must be provided")

        station_stats_req: station_stats_api.StationStatReq = (
            station_stats_api.StationStatReq(
                self.auth_token,
                start_ts_s,
                end_ts_s,
                station_ids,
                self.redvox_config.secret_token,
            )
        )

        return station_stats_api.request_station_stats(
            self.redvox_config, station_stats_req, self.__session, self.timeout
        )


@contextlib.contextmanager
def cloud_client(
    redvox_config: Optional[RedVoxConfig] = RedVoxConfig.find(),
    refresh_token_interval: float = 600.0,
    timeout: float = 10.0,
):
    """
    Function that can be used within a "with" block to automatically handle the closing of open resources.
    Creates and returns a CloudClient that will automatically be closed when exiting the with block or if an error
    occurs.

    See https://docs.python.org/3/library/contextlib.html for more info.

    :param redvox_config: The Redvox endpoint configuration.
    :param refresh_token_interval: An optional token refresh interval
    :param timeout: An optional timeout.
    :return: A CloudClient.
    """
    if redvox_config is None:
        raise cloud_errors.CloudApiError(
            "A RedVoxConfig was not found in the environment and one wasn't provided"
        )

    client: CloudClient = CloudClient(redvox_config, refresh_token_interval, timeout)
    try:
        yield client
    finally:
        if client is not None:
            client.close()
