import requests
from typing import List, Generator
from argparse import Namespace

from .exceptions import APIKeyException, RequestException


class APRS(object):

    _api_key: str

    def __init__(self, api_key: str) -> None:
        """Init an APRS.fi client

        Args:
            api_key (str): APRS.fi API key
        """

        self._api_key = api_key

    def _handle_api_request(self, url: str) -> Generator[Namespace, None, None]:

        # Make REST call
        response = requests.get(url, headers={"User-Agent": "pyaprsfi"})

        # Handle errors
        if int(response.status_code / 100) != 2:
            return

        # Parse
        response_json = response.json()

        # Check response errors
        if response_json["result"] != "ok":
            if response_json["code"] == "apikey-wrong":
                raise APIKeyException()
            else:
                raise RequestException()

        # Handle every entry
        for entry in response_json["entries"]:
            yield Namespace(**entry)

    def getLocation(self, callsigns: List[str]) -> Generator[Namespace, None, None]:

        # Build a comma-seperated list of callsigns
        # This also handles lazy programmers
        if type(callsigns) == list:
            comma_calls = ",".join(callsigns)
        else:
            comma_calls = callsigns

        # Process the request
        return self._handle_api_request(f"https://api.aprs.fi/api/get?name={comma_calls}&what=loc&apikey={self._api_key}&format=json")

    def getWeather(self, callsigns: List[str]) -> Generator[Namespace, None, None]:

        # Build a comma-seperated list of callsigns
        # This also handles lazy programmers
        if type(callsigns) == list:
            comma_calls = ",".join(callsigns)
        else:
            comma_calls = callsigns

        # Process the request
        return self._handle_api_request(f"https://api.aprs.fi/api/get?name={comma_calls}&what=wx&apikey={self._api_key}&format=json")

    def getMessages(self, callsigns: List[str]) -> Generator[Namespace, None, None]:

        # Build a comma-seperated list of callsigns
        # This also handles lazy programmers
        if type(callsigns) == list:
            comma_calls = ",".join(callsigns)
        else:
            comma_calls = callsigns

        # Process the request
        return self._handle_api_request(f"https://api.aprs.fi/api/get?dst={comma_calls}&what=msg&apikey={self._api_key}&format=json")
