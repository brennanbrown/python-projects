"""NOAA/NWS weather retrieval services."""

from __future__ import annotations

import json
import time
import urllib.request
import xml.etree.ElementTree as ET

USER_AGENT = "python-projects/ci (github.com/brennanbrown)"


def _urlopen_with_retry(
    req: urllib.request.Request, timeout: int, retries: int = 2, backoff: float = 0.5
):
    last_exc: Exception | None = None
    for attempt in range(retries + 1):
        try:
            return urllib.request.urlopen(req, timeout=timeout)
        except Exception as exc:  # noqa: BLE001 - broad catch acceptable for retry wrapper
            last_exc = exc
            if attempt < retries:
                time.sleep(backoff * (2**attempt))
            else:
                raise
    # Unreachable, but keeps type-checkers happy
    if last_exc:
        raise last_exc
    raise RuntimeError("_urlopen_with_retry failed without exception")


def get_noaa_xml_current_obs(station_id: str, timeout: int = 10) -> tuple[dict[str, str], str]:
    """Fetch current observations from legacy NOAA XML endpoint.

    Returns a tuple of (data_dict, icon_url).
    """
    weather_data_tags_dict = {
        "observation_time": "",
        "weather": "",
        "temp_f": "",
        "temp_c": "",
        "dewpoint_f": "",
        "dewpoint_c": "",
        "relative_humidity": "",
        "wind_string": "",
        "visibility_mi": "",
        "pressure_string": "",
        "pressure_in": "",
        "location": "",
    }
    url_general = "https://www.weather.gov/xml/current_obs/{}.xml"
    url = url_general.format(station_id)
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with _urlopen_with_retry(req, timeout=timeout) as resp:
        content = resp.read().decode()

    xml_root = ET.fromstring(content)
    for key in weather_data_tags_dict:
        node = xml_root.find(key)
        weather_data_tags_dict[key] = node.text if node is not None else ""

    icon_url_base = (
        xml_root.find("icon_url_base").text if xml_root.find("icon_url_base") is not None else ""
    )
    icon_url_name = (
        xml_root.find("icon_url_name").text if xml_root.find("icon_url_name") is not None else ""
    )
    icon_url = f"{icon_url_base}{icon_url_name}"
    return weather_data_tags_dict, icon_url


def try_get_nws_v3_latest_observation(station_id: str, timeout: int = 10) -> dict[str, str] | None:
    """Attempt to fetch latest observation via NWS v3 JSON API.

    Returns a normalized dict on success, or None on failure (caller may fallback to XML).
    """
    api_url = f"https://api.weather.gov/stations/{station_id}/observations/latest"
    req = urllib.request.Request(
        api_url,
        headers={
            "User-Agent": USER_AGENT,
            "Accept": "application/ld+json",
        },
    )
    try:
        with _urlopen_with_retry(req, timeout=timeout) as resp:
            data = json.loads(resp.read().decode())
    except Exception:
        return None

    props = data.get("properties", {})

    # Conversions and safe extraction helpers
    def _get_num(dct: dict, key: str) -> float:
        val = (dct.get(key) or {}).get("value") if isinstance(dct, dict) else None
        try:
            return float(val) if val is not None else 0.0
        except Exception:
            return 0.0

    wind_speed_m_s = _get_num(props, "windSpeed")
    wind_dir_deg = _get_num(props, "windDirection")
    vis_m = _get_num(props, "visibility")
    pressure_pa = _get_num(props, "barometricPressure") or _get_num(props, "seaLevelPressure")

    wind_mph = wind_speed_m_s * 2.23693629
    vis_miles = vis_m * 0.000621371 if vis_m else 0.0
    pressure_inhg = pressure_pa * 0.0002953 if pressure_pa else 0.0
    pressure_hpa = pressure_pa / 100.0 if pressure_pa else 0.0

    out: dict[str, str] = {
        "observation_time": props.get("timestamp", ""),
        "weather": (props.get("textDescription") or ""),
        "temp_f": str(
            round(((props.get("temperature", {}) or {}).get("value") or 0) * 9 / 5 + 32, 1)
        ),
        "temp_c": str(round(((props.get("temperature", {}) or {}).get("value") or 0), 1)),
        "dewpoint_f": str(
            round(((props.get("dewpoint", {}) or {}).get("value") or 0) * 9 / 5 + 32, 1)
        ),
        "dewpoint_c": str(round(((props.get("dewpoint", {}) or {}).get("value") or 0), 1)),
        "relative_humidity": str(
            round(((props.get("relativeHumidity", {}) or {}).get("value") or 0), 1)
        ),
        "wind_string": (
            f"{int(round(wind_dir_deg))} degrees at {wind_mph:.1f} MPH" if wind_mph else ""
        ),
        "visibility_mi": f"{vis_miles:.2f}" if vis_miles else "",
        "pressure_string": f"{pressure_hpa:.1f} hPa" if pressure_hpa else "",
        "pressure_in": f"{pressure_inhg:.2f}" if pressure_inhg else "",
        "location": station_id,
    }
    return out


def get_noaa_current_obs(station_id: str, timeout: int = 10) -> tuple[dict[str, str], str]:
    """Prefer NWS v3 JSON; fall back to legacy XML.

    Returns a tuple of (data_dict, icon_url). NWS v3 does not provide an icon URL; in that
    case the icon_url will be an empty string.
    """
    json_obs = try_get_nws_v3_latest_observation(station_id, timeout=timeout)
    if json_obs is not None:
        return json_obs, ""
    return get_noaa_xml_current_obs(station_id, timeout=timeout)
