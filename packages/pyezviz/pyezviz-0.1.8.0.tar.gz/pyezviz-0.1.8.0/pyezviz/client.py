"""Ezviz API."""
import hashlib
import logging
from random import randint
from uuid import uuid4

import requests
from pyezviz.camera import EzvizCamera
from pyezviz.constants import DefenseModeType, DeviceCatagories

API_ENDPOINT_AUTH = "/doLogin"
API_ENDPOINT_CLOUDDEVICES = "/api/cloud/v2/cloudDevices/getAll"
API_ENDPOINT_PAGELIST = "/v3/userdevices/v1/devices/pagelist"
API_ENDPOINT_DEVICES = "/v3/devices/"
API_ENDPOINT_LOGIN = "/v3/users/login/v5"
API_ENDPOINT_SWITCH_STATUS = "/switchStatus"
API_ENDPOINT_PTZCONTROL = "/ptzControl"
API_ENDPOINT_ALARM_SOUND = "/alarm/sound"
API_ENDPOINT_SET_DEFENCE = "/camera/cameraAction!enableDefence.action"
API_ENDPOINT_DETECTION_SENSIBILITY = "/api/device/configAlgorithm"
API_ENDPOINT_DETECTION_SENSIBILITY_GET = "/api/device/queryAlgorithmConfig"
API_ENDPOINT_ALARMINFO_GET = "/v3/alarms/v2/advanced"
API_ENDPOINT_CHECKLOGIN = "/user/user/userAction!checkLoginInfo.action"
API_ENDPOINT_SET_DEFENCE_SCHEDULE = "/api/device/defence/plan2"
API_ENDPOINT_SWITCH_DEFENCE_MODE = "/v3/userdevices/v1/group/switchDefenceMode"
API_ENDPOINT_SWITCH_SOUND_ALARM = "/sendAlarm"

DEFAULT_TIMEOUT = 25
MAX_RETRIES = 3


class PyEzvizError(Exception):
    """Handle exception."""


class EzvizClient:
    """Initialize api client object."""

    def __init__(
        self,
        account,
        password,
        url="apiieu.ezvizlife.com",
        timeout=DEFAULT_TIMEOUT,
    ):
        """Initialize the client object."""
        self.account = account
        self.password = password
        self._session = None
        self._timeout = timeout
        self.api_uri = url

    def _login(self):
        """Login to Ezviz' API."""

        # Fix for old region code usage, should now be url.
        if len(self.api_uri.split(".")) == 1:
            self.api_uri = "apii" + self.api_uri + ".ezvizlife.com"
            print(f"Region code depreciated, please use full url: {self.api_uri}")

        # Break up URI into components and remove api portion.
        host_api_domain = self.api_uri.split(".", 1)[0]
        host_api_domain = host_api_domain.replace("apii", "")
        host_api_domain = host_api_domain.replace("api", "")
        api_domain = "." + self.api_uri.split(".", 1)[1]

        # Ezviz API sends md5 of password.
        temp = hashlib.md5()
        temp.update(self.password.encode("utf-8"))
        md5pass = temp.hexdigest()
        randommath = randint(1000000000000000000, 9999999999999999999)
        payload = {
            "account": self.account,
            "password": md5pass,
            "from": "4e4148ba90184a7cbd81",
            "r": randommath,
            "returnUrl": "plugin",
            "host": self.api_uri,
        }

        try:
            req = self._session.post(
                "https://" + host_api_domain + "auth" + api_domain + API_ENDPOINT_AUTH,
                allow_redirects=False,
                data=payload,
                timeout=self._timeout,
            )

            req.raise_for_status()

        except requests.HTTPError as err:
            raise requests.HTTPError(err)

        try:
            json_result = req.json()

        except ValueError as err:
            raise PyEzvizError("Can't decode login response") from err

        if self._session.cookies.get("REDIRECTCOOKIE", domain=api_domain):
            return self._login_api()

        if json_result["retcode"] == "1001":
            raise PyEzvizError("Incorrect login details or region url")

        if json_result["retcode"] == "1002":
            raise PyEzvizError("Login error: Check your password!")

        if json_result["retcode"] == "1005":
            raise PyEzvizError(
                "Too many failed logins. Open API url in IE and enter Captcha code"
            )

        # Update cookie with JS Session ID.
        try:
            req = self._session.get(
                "https://" + self.api_uri + "/check_plugin.jsp",
                timeout=self._timeout,
            )

            req.raise_for_status()

        except requests.HTTPError as err:
            raise requests.HTTPError(err)

        return True

    def _login_api(self):
        """Login to Ezviz' API."""

        # Ezviz API sends md5 of password
        temp = hashlib.md5()
        temp.update(self.password.encode("utf-8"))
        md5pass = temp.hexdigest()
        payload = {
            "account": self.account,
            "password": md5pass,
            "featureCode": "d9edb711e6563e99d366d1a84602f51f",
        }

        try:
            req = self._session.post(
                "https://" + self.api_uri + API_ENDPOINT_LOGIN,
                allow_redirects=False,
                headers={"clientType": "3"},
                data=payload,
                timeout=self._timeout,
            )

            req.raise_for_status()

        except requests.HTTPError as err:
            raise requests.HTTPError(err)

        json_result = req.json()

        if json_result["meta"]["code"] == 1100:
            self.api_uri = json_result["loginArea"]["apiDomain"]
            print("Region incorrect!")
            print(f"Your region url: {self.api_uri}")
            return self.login()

        return True

    def _api_get_pagelist(self, page_filter=None, json_key=None, max_retries=0):
        """Get data from pagelist API."""

        if max_retries > MAX_RETRIES:
            raise PyEzvizError("Can't gather proper data. Max retries exceeded.")

        if page_filter is None:
            raise PyEzvizError("Trying to call get_pagelist without filter")

        try:
            req = self._session.get(
                "https://" + self.api_uri + API_ENDPOINT_PAGELIST,
                params={"filter": page_filter},
                timeout=self._timeout,
            )

            req.raise_for_status()

        except requests.HTTPError as err:
            if err.response.status_code == 401:
                # session is wrong, need to relogin
                self.login()
                return self._api_get_pagelist(page_filter, json_key, max_retries + 1)

            raise requests.HTTPError(err)

        if not req.text:
            raise PyEzvizError("No data")

        try:
            json_output = req.json()

        except ValueError as err:
            raise PyEzvizError(
                "Impossible to decode response: "
                + str(err)
                + "\nResponse was: "
                + str(req.text)
            ) from err

        if json_output.get("meta").get("code") != 200:
            # session is wrong, need to relogin
            self.login()
            logging.info("Got 401, relogging (max retries: %s)", str(max_retries))
            return self._api_get_pagelist(page_filter, json_key, max_retries + 1)

        if json_key is None:
            json_result = json_output
        else:
            json_result = json_output[json_key]

        if not json_result:
            # session is wrong, need to relogin
            self.login()
            logging.info(
                "Impossible to load the devices, here is the returned response: %s",
                str(req.text),
            )
            return self._api_get_pagelist(page_filter, json_key, max_retries + 1)

        return json_result

    def get_alarminfo(self, serial, max_retries=0):
        """Get data from alarm info API."""
        if max_retries > MAX_RETRIES:
            raise PyEzvizError("Can't gather proper data. Max retries exceeded.")

        try:
            req = self._session.get(
                "https://" + self.api_uri + API_ENDPOINT_ALARMINFO_GET,
                params={
                    "deviceSerials": serial,
                    "queryType": -1,
                    "limit": 1,
                    "stype": 2401,
                },
                timeout=self._timeout,
            )

            req.raise_for_status()

        except requests.HTTPError as err:
            if err.response.status_code == 401:
                # session is wrong, need to relogin
                self.login()
                return self.get_alarminfo(serial, max_retries + 1)

            raise requests.HTTPError(err)

        if req.text == "":
            raise PyEzvizError("No data")

        try:
            json_output = req.json()

        except ValueError as err:
            raise PyEzvizError(
                "Impossible to decode response: "
                + str(err)
                + "\nResponse was: "
                + str(req.text)
            ) from err

        return json_output

    def _switch_status(self, serial, status_type, enable, max_retries=0):
        """Switch status on a device."""
        if max_retries > MAX_RETRIES:
            raise PyEzvizError("Can't gather proper data. Max retries exceeded.")

        try:
            req = self._session.put(
                "https://"
                + self.api_uri
                + API_ENDPOINT_DEVICES
                + serial
                + "/1/1/"
                + str(status_type)
                + API_ENDPOINT_SWITCH_STATUS,
                data={
                    "enable": enable,
                    "serial": serial,
                    "channelNo": "1",
                    "type": status_type,
                },
                timeout=self._timeout,
            )

            req.raise_for_status()

        except requests.HTTPError as err:
            if err.response.status_code == 401:
                # session is wrong, need to relogin
                self.login()
                return self._switch_status(serial, status_type, enable, max_retries + 1)

            raise requests.HTTPError(err)

        try:
            json_output = req.json()

        except ValueError as err:
            raise PyEzvizError(
                "Impossible to decode response: "
                + str(err)
                + "\nResponse was: "
                + str(req.text)
            ) from err

        if json_output.get("meta").get("code") != 200:
            raise PyEzvizError(
                f"Could not set the switch: Got {req.status_code} : {req.text})"
            )

        return True

    def sound_alarm(self, serial, enable=1, max_retries=0):
        """Sound alarm on a device."""
        if max_retries > MAX_RETRIES:
            raise PyEzvizError("Can't gather proper data. Max retries exceeded.")

        try:
            req = self._session.put(
                "https://"
                + self.api_uri
                + API_ENDPOINT_DEVICES
                + serial
                + "/0"
                + API_ENDPOINT_SWITCH_SOUND_ALARM,
                data={
                    "enable": enable,
                },
                timeout=self._timeout,
            )

            req.raise_for_status()

        except requests.HTTPError as err:
            if err.response.status_code == 401:
                # session is wrong, need to relogin
                self.login()
                return self.sound_alarm(serial, enable, max_retries + 1)

            raise requests.HTTPError(err)

        try:
            json_output = req.json()

        except ValueError as err:
            raise PyEzvizError(
                "Impossible to decode response: "
                + str(err)
                + "\nResponse was: "
                + str(req.text)
            ) from err

        if json_output.get("meta").get("code") != 200:
            raise PyEzvizError(
                f"Could not set the alarm sound: Got {req.status_code} : {req.text})"
            )

        return True

    def load_cameras(self):
        """Load and return all cameras objects."""

        devices = self._get_all_device_infos()
        cameras = []
        supported_categories = [
            DeviceCatagories.COMMON_DEVICE_CATEGORY.value,
            DeviceCatagories.CAMERA_DEVICE_CATEGORY.value,
            DeviceCatagories.BATTERY_CAMERA_DEVICE_CATEGORY.value,
            DeviceCatagories.DOORBELL_DEVICE_CATEGORY.value,
            DeviceCatagories.BASE_STATION_DEVICE_CATEGORY.value,
        ]

        for device in devices:
            if (
                devices.get(device).get("deviceInfos").get("deviceCategory")
                in supported_categories
            ):
                # Add support for connected HikVision cameras
                if devices.get(device).get("deviceInfos").get(
                    "deviceCategory"
                ) == DeviceCatagories.COMMON_DEVICE_CATEGORY.value and not devices.get(
                    device
                ).get(
                    "deviceInfos"
                ).get(
                    "hik"
                ):
                    continue

                # Create camera object

                camera = EzvizCamera(self, device, devices.get(device))

                camera.load()
                cameras.append(camera.status())

        return cameras

    def _get_all_device_infos(self):
        """Load all devices and build dict per device serial"""

        devices = self._get_page_list()
        result = {}

        for device in devices["deviceInfos"]:
            result[device["deviceSerial"]] = {}
            result[device["deviceSerial"]]["deviceInfos"] = device
            result[device["deviceSerial"]]["connectionInfos"] = devices.get(
                "connectionInfos"
            ).get(device["deviceSerial"])
            result[device["deviceSerial"]]["p2pInfos"] = devices.get("p2pInfos").get(
                device["deviceSerial"]
            )
            result[device["deviceSerial"]]["alarmNodisturbInfos"] = devices.get(
                "alarmNodisturbInfos"
            ).get(device["deviceSerial"])
            result[device["deviceSerial"]]["kmsInfos"] = devices.get("kmsInfos").get(
                device["deviceSerial"]
            )
            result[device["deviceSerial"]]["timePlanInfos"] = devices.get(
                "timePlanInfos"
            ).get(device["deviceSerial"])
            result[device["deviceSerial"]]["statusInfos"] = devices.get(
                "statusInfos"
            ).get(device["deviceSerial"])
            result[device["deviceSerial"]]["wifiInfos"] = devices.get("wifiInfos").get(
                device["deviceSerial"]
            )
            result[device["deviceSerial"]]["switchStatusInfos"] = devices.get(
                "switchStatusInfos"
            ).get(device["deviceSerial"])
            for item in devices["cameraInfos"]:
                if item["deviceSerial"] == device["deviceSerial"]:
                    result[device["deviceSerial"]]["cameraInfos"] = item
                    result[device["deviceSerial"]]["cloudInfos"] = devices.get(
                        "cloudInfos"
                    ).get(item["cameraId"])

        return result

    def get_all_per_serial_infos(self, serial=None):
        """Load all devices and build dict per device serial"""

        if serial is None:
            raise PyEzvizError("Need serial number for this query")

        devices = self._get_page_list()
        result = {serial: {}}

        for device in devices["deviceInfos"]:
            if device["deviceSerial"] == serial:
                result[device["deviceSerial"]]["deviceInfos"] = device
                result[device["deviceSerial"]]["deviceInfos"] = device
                result[device["deviceSerial"]]["connectionInfos"] = devices.get(
                    "connectionInfos"
                ).get(device["deviceSerial"])
                result[device["deviceSerial"]]["p2pInfos"] = devices.get(
                    "p2pInfos"
                ).get(device["deviceSerial"])
                result[device["deviceSerial"]]["alarmNodisturbInfos"] = devices.get(
                    "alarmNodisturbInfos"
                ).get(device["deviceSerial"])
                result[device["deviceSerial"]]["kmsInfos"] = devices.get(
                    "kmsInfos"
                ).get(device["deviceSerial"])
                result[device["deviceSerial"]]["timePlanInfos"] = devices.get(
                    "timePlanInfos"
                ).get(device["deviceSerial"])
                result[device["deviceSerial"]]["statusInfos"] = devices.get(
                    "statusInfos"
                ).get(device["deviceSerial"])
                result[device["deviceSerial"]]["wifiInfos"] = devices.get(
                    "wifiInfos"
                ).get(device["deviceSerial"])
                result[device["deviceSerial"]]["switchStatusInfos"] = devices.get(
                    "switchStatusInfos"
                ).get(device["deviceSerial"])
                for item in devices["cameraInfos"]:
                    if item["deviceSerial"] == device["deviceSerial"]:
                        result[device["deviceSerial"]]["cameraInfos"] = item
                        result[device["deviceSerial"]]["cloudInfos"] = devices.get(
                            "cloudInfos"
                        ).get(item["cameraId"])

        return result.get(serial)

    def ptz_control(self, command, serial, action, speed=5):
        """PTZ Control by API."""
        if command is None:
            raise PyEzvizError("Trying to call ptzControl without command")
        if action is None:
            raise PyEzvizError("Trying to call ptzControl without action")

        try:
            req = self._session.put(
                "https://"
                + self.api_uri
                + API_ENDPOINT_DEVICES
                + serial
                + API_ENDPOINT_PTZCONTROL,
                data={
                    "command": command,
                    "action": action,
                    "channelNo": "1",
                    "speed": speed,
                    "uuid": str(uuid4()),
                    "serial": serial,
                },
                headers={"clientType": "1"},
                timeout=self._timeout,
            )

            req.raise_for_status()

        except requests.HTTPError as err:
            raise requests.HTTPError(err)

        return req.text

    def login(self):
        """Set http session."""
        if self._session is None:
            self._session = requests.session()
            self._login()

        try:
            req = self._session.get(
                "https://" + self.api_uri + API_ENDPOINT_CHECKLOGIN,
                allow_redirects=False,
                timeout=self._timeout,
            )

            req.raise_for_status()

        except requests.HTTPError as err:
            raise requests.HTTPError(err)

        try:
            response_json = req.json()

        except ValueError:
            return self._login()

        if response_json["success"] != "success":
            self._login()

        return True

    def data_report(self, serial, enable=1, max_retries=0):
        """Enable alarm notifications."""
        if max_retries > MAX_RETRIES:
            raise PyEzvizError("Can't gather proper data. Max retries exceeded.")

        try:
            req = self._session.post(
                "https://" + self.api_uri + API_ENDPOINT_SET_DEFENCE,
                data={
                    "deviceSerial": serial,
                    "defenceType": "Global",
                    "enablePlan": enable,
                    "channelNo": "1",
                },
                timeout=self._timeout,
            )

            req.raise_for_status()

        except requests.HTTPError as err:
            if err.response.status_code == 401:
                # session is wrong, need to relogin
                self.login()
                return self.data_report(serial, enable, max_retries + 1)

            raise requests.HTTPError(err)

        try:
            json_output = req.json()

        except ValueError as err:
            raise PyEzvizError(
                "Impossible to decode response: "
                + str(err)
                + "\nResponse was: "
                + str(req.text)
            ) from err

        if json_output.get("resultCode") != "0":
            raise PyEzvizError(
                f"Could not set alarm notification: Got {req.status_code} : {req.text})"
            )

        return True

    def api_set_defence_schedule(self, serial, schedule, enable, max_retries=0):
        """Set defence schedules."""
        if max_retries > MAX_RETRIES:
            raise PyEzvizError("Can't gather proper data. Max retries exceeded.")

        schedulestring = (
            '{"CN":0,"EL":'
            + str(enable)
            + ',"SS":"'
            + serial
            + '","WP":['
            + schedule
            + "]}]}"
        )
        try:
            req = self._session.post(
                "https://" + self.api_uri + API_ENDPOINT_SET_DEFENCE_SCHEDULE,
                data={
                    "devTimingPlan": schedulestring,
                },
                timeout=self._timeout,
            )

            req.raise_for_status()

        except requests.HTTPError as err:
            if err.response.status_code == 401:
                # session is wrong, need to relogin
                self.login()
                return self.api_set_defence_schedule(
                    serial, schedule, enable, max_retries + 1
                )

            raise requests.HTTPError(err)

        try:
            json_output = req.json()

        except ValueError as err:
            raise PyEzvizError(
                "Impossible to decode response: "
                + str(err)
                + "\nResponse was: "
                + str(req.text)
            ) from err

        if json_output.get("resultCode") != 0:
            raise PyEzvizError(
                f"Could not set the schedule: Got {req.status_code} : {req.text})"
            )

        return True

    def api_set_defence_mode(self, mode: DefenseModeType, max_retries=0):
        """Set defence mode."""
        if max_retries > MAX_RETRIES:
            raise PyEzvizError("Can't gather proper data. Max retries exceeded.")

        try:
            req = self._session.post(
                "https://" + self.api_uri + API_ENDPOINT_SWITCH_DEFENCE_MODE,
                data={
                    "groupId": -1,
                    "mode": mode,
                },
                timeout=self._timeout,
            )

            req.raise_for_status()

        except requests.HTTPError as err:
            if err.response.status_code == 401:
                # session is wrong, need to relogin
                self.login()
                return self.api_set_defence_mode(mode, max_retries + 1)

            raise requests.HTTPError(err)

        try:
            json_output = req.json()

        except ValueError as err:
            raise PyEzvizError(
                "Impossible to decode response: "
                + str(err)
                + "\nResponse was: "
                + str(req.text)
            ) from err

        if json_output.get("meta").get("code") != 200:
            raise PyEzvizError(
                f"Could not set defence mode: Got {req.status_code} : {req.text})"
            )

        return True

    def detection_sensibility(self, serial, sensibility=3, type_value=3, max_retries=0):
        """Set detection sensibility."""
        if max_retries > MAX_RETRIES:
            raise PyEzvizError("Can't gather proper data. Max retries exceeded.")

        if sensibility not in [0, 1, 2, 3, 4, 5, 6] and type_value == 0:
            raise PyEzvizError(
                "Unproper sensibility for type 0 (should be within 1 to 6)."
            )

        try:
            req = self._session.post(
                "https://" + self.api_uri + API_ENDPOINT_DETECTION_SENSIBILITY,
                data={
                    "subSerial": serial,
                    "type": type_value,
                    "channelNo": "1",
                    "value": sensibility,
                },
                timeout=self._timeout,
            )

            req.raise_for_status()

        except requests.HTTPError as err:
            if err.response.status_code == 401:
                # session is wrong, need to re-log-in
                self.login()
                return self.detection_sensibility(
                    serial, sensibility, type_value, max_retries + 1
                )

            raise requests.HTTPError(err)

        try:
            response_json = req.json()

        except ValueError as err:
            raise PyEzvizError("Could not decode response:" + str(err)) from err

        if response_json["resultCode"] and response_json["resultCode"] != "0":
            return "Unknown value"

        return True

    def get_detection_sensibility(self, serial, type_value="0", max_retries=0):
        """Get detection sensibility notifications."""
        if max_retries > MAX_RETRIES:
            raise PyEzvizError("Can't gather proper data. Max retries exceeded.")

        try:
            req = self._session.post(
                "https://" + self.api_uri + API_ENDPOINT_DETECTION_SENSIBILITY_GET,
                data={
                    "subSerial": serial,
                },
                timeout=self._timeout,
            )

            req.raise_for_status()

        except requests.HTTPError as err:
            if err.response.status_code == 401:
                # session is wrong, need to re-log-in.
                self.login()
                return self.get_detection_sensibility(
                    serial, type_value, max_retries + 1
                )

            raise requests.HTTPError(err)

        try:
            response_json = req.json()

        except ValueError as err:
            raise PyEzvizError("Could not decode response:" + str(err)) from err

        if response_json["resultCode"] != "0":
            return "Unknown"

        if response_json["algorithmConfig"]["algorithmList"]:
            for idx in response_json["algorithmConfig"]["algorithmList"]:
                if idx["type"] == type_value:
                    return idx["value"]

        return "Unknown"

    # soundtype: 0 = normal, 1 = intensive, 2 = disabled ... don't ask me why...
    def alarm_sound(self, serial, sound_type, enable=1, max_retries=0):
        """Enable alarm sound by API."""
        if max_retries > MAX_RETRIES:
            raise PyEzvizError("Can't gather proper data. Max retries exceeded.")

        if sound_type not in [0, 1, 2]:
            raise PyEzvizError(
                "Invalid sound_type, should be 0,1,2: " + str(sound_type)
            )

        try:
            req = self._session.put(
                "https://"
                + self.api_uri
                + API_ENDPOINT_DEVICES
                + serial
                + API_ENDPOINT_ALARM_SOUND,
                data={
                    "enable": enable,
                    "soundType": sound_type,
                    "voiceId": "0",
                    "deviceSerial": serial,
                },
                timeout=self._timeout,
            )

            req.raise_for_status()

        except requests.HTTPError as err:
            if err.response.status_code == 401:
                # session is wrong, need to re-log-in
                self.login()
                return self.alarm_sound(serial, sound_type, enable, max_retries + 1)

            raise requests.HTTPError(err)

        return True

    def switch_status(self, serial, status_type, enable=0):
        """Switch status of a device."""
        return self._switch_status(serial, status_type, enable)

    def _get_page_list(self):
        """Get ezviz device info broken down in sections."""
        return self._api_get_pagelist(
            page_filter="CLOUD, TIME_PLAN, CONNECTION, SWITCH,"
            "STATUS, WIFI, NODISTURB, KMS, P2P,"
            "TIME_PLAN, CHANNEL, VTM, DETECTOR,"
            "FEATURE, UPGRADE, VIDEO_QUALITY, QOS",
            json_key=None,
        )

    def get_device(self):
        """Get ezviz devices filter."""
        return self._api_get_pagelist(page_filter="CLOUD", json_key="deviceInfos")

    def get_connection(self):
        """Get ezviz connection infos filter."""
        return self._api_get_pagelist(
            page_filter="CONNECTION", json_key="connectionInfos"
        )

    def _get_status(self):
        """Get ezviz status infos filter."""
        return self._api_get_pagelist(page_filter="STATUS", json_key="statusInfos")

    def get_switch(self):
        """Get ezviz switch infos filter."""
        return self._api_get_pagelist(
            page_filter="SWITCH", json_key="switchStatusInfos"
        )

    def _get_wifi(self):
        """Get ezviz wifi infos filter."""
        return self._api_get_pagelist(page_filter="WIFI", json_key="wifiInfos")

    def _get_nodisturb(self):
        """Get ezviz nodisturb infos filter."""
        return self._api_get_pagelist(
            page_filter="NODISTURB", json_key="alarmNodisturbInfos"
        )

    def _get_p2p(self):
        """Get ezviz P2P infos filter."""
        return self._api_get_pagelist(page_filter="P2P", json_key="p2pInfos")

    def _get_kms(self):
        """Get ezviz KMS infos filter."""
        return self._api_get_pagelist(page_filter="KMS", json_key="kmsInfos")

    def _get_time_plan(self):
        """Get ezviz TIME_PLAN infos filter."""
        return self._api_get_pagelist(page_filter="TIME_PLAN", json_key="timePlanInfos")

    def close_session(self):
        """Close current session."""
        self._session.close()
        self._session = None
