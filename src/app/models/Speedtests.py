import datetime

from typing import Any, Optional
from redis_om import Field

from app.models.common import BaseModel


class SpeedtestResult(BaseModel):
    type: str = Field(index=True)
    timestamp: datetime.datetime = Field(index=True)
    isp: str = Field(index=True)
    # is it an int, is it a float? What is it?
    packet_loss: Optional[float]
    # ping
    ping_jitter: float = Field(index=True)
    ping_iqm: float = Field(index=True)
    ping_low: float = Field(index=True)
    ping_high: float = Field(index=True)
    # download
    down_mbps: float = Field(index=True)
    down_bandwidth: int = Field(index=True)
    down_bytes: int = Field(index=True)
    down_elapsed: int = Field(index=True)
    down_iqm: float = Field(index=True)
    down_low: float = Field(index=True)
    down_high: float = Field(index=True)
    down_jitter: float = Field(index=True)
    # upload
    up_mbps: float = Field(index=True)
    up_bandwidth: int = Field(index=True)
    up_bytes: int = Field(index=True)
    up_elapsed: int = Field(index=True)
    up_iqm: float = Field(index=True)
    up_low: float = Field(index=True)
    up_high: float = Field(index=True)
    up_jitter: float = Field(index=True)
    # interface
    external_ip: str = Field(index=True)
    internal_ip: str = Field(index=True)
    is_vpn: bool = Field(index=True)
    mac_addr: str = Field(index=True)
    name: str = Field(index=True)
    # result fields
    result_id: str = Field(index=True)
    result_url: str = Field(index=True)
    result_persisted: bool
    # server information
    server_id: str = Field(index=True)
    server_host: str = Field(index=True)
    server_port: int = Field(index=True)
    server_name: str = Field(index=True)
    server_location: str = Field(index=True)
    server_country: str = Field(index=True)
    server_ip: str = Field(index=True)

    # TODO: Correct issue with conversion from dict to redis object instance; SpeedtestResult.find().all() yields [] when known instances exist
    @staticmethod
    def from_dict(obj: Any) -> "SpeedtestResult":
        _type = obj.get("type")
        _timestamp = obj.get("timestamp")
        _isp = obj.get("isp")
        _packet_loss = obj.get("packet_loss")
        # ping
        _ping_jitter = obj.get("ping_jitter")
        _ping_iqm = obj.get("ping_iqm")
        _ping_low = obj.get("ping_low")
        _ping_high = obj.get("ping_high")
        # download
        _down_mbps = obj.get("down_mbps")
        _down_bandwidth = obj.get("down_bandwidth")
        _down_bytes = obj.get("down_bytes")
        _down_elapsed = obj.get("down_elapsed")
        _down_iqm = obj.get("down_iqm")
        _down_low = obj.get("down_low")
        _down_high = obj.get("down_high")
        _down_jitter = obj.get("down_jitter")
        # upload
        _up_mbps = obj.get("up_mbps")
        _up_bandwidth = obj.get("up_bandwidth")
        _up_bytes = obj.get("up_bytes")
        _up_elapsed = obj.get("up_elapsed")
        _up_iqm = obj.get("up_iqm")
        _up_low = obj.get("up_low")
        _up_high = obj.get("up_high")
        _up_jitter = obj.get("up_jitter")
        # interface
        _external_ip = obj.get("interface_external_ip")
        _internal_ip = obj.get("interface_internal_ip")
        _is_vpn = obj.get("interface_is_vpn")
        _mac_addr = obj.get("interface_mac_addr")
        _name = obj.get("interface_name")
        # result fields
        _result_id = obj.get("result_id")
        _result_url = obj.get("result_url")
        _result_persisted = obj.get("result_persisted")
        # server information
        _server_id = obj.get("server_id")
        _server_host = obj.get("server_host")
        _server_port = obj.get("server_port")
        _server_name = obj.get("server_name")
        _server_location = obj.get("server_location")
        _server_country = obj.get("server_country")
        _server_ip = obj.get("server_ip")

        return SpeedtestResult(
            type=_type,
            timestamp=_timestamp,
            isp=_isp,
            packet_loss=_packet_loss,
            # ping,
            ping_jitter=_ping_jitter,
            ping_iqm=_ping_iqm,
            ping_low=_ping_low,
            ping_high=_ping_high,
            # download,
            down_mbps=_down_mbps,
            down_bandwidth=_down_bandwidth,
            down_bytes=_down_bytes,
            down_elapsed=_down_elapsed,
            down_iqm=_down_iqm,
            down_low=_down_low,
            down_high=_down_high,
            down_jitter=_down_jitter,
            # upload,
            up_mbps=_up_mbps,
            up_bandwidth=_up_bandwidth,
            up_bytes=_up_bytes,
            up_elapsed=_up_elapsed,
            up_iqm=_up_iqm,
            up_low=_up_low,
            up_high=_up_high,
            up_jitter=_up_jitter,
            # interface,
            external_ip=_external_ip,
            internal_ip=_internal_ip,
            is_vpn=_is_vpn,
            mac_addr=_mac_addr,
            name=_name,
            # result fields,
            result_id=_result_id,
            result_url=_result_url,
            result_persisted=_result_persisted,
            # server information,
            server_id=_server_id,
            server_host=_server_host,
            server_port=_server_port,
            server_name=_server_name,
            server_location=_server_location,
            server_country=_server_country,
            server_ip=_server_ip,
        )
