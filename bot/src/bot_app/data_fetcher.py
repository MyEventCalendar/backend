import json
import urllib3
from .local_settings import API_URL

http = urllib3.PoolManager()


class API_Metods():
    def __init__(self):
        self.__response_data__ = None

    def get_all_events(self):
        response = http.request("GET", f"{API_URL}/events")
        self.__response_data__ = response.data
        return self.__parse_data__()

    def get_actual_events(self):
        response = http.request("GET", f"{API_URL}/events", fields={"actual": "true"})
        self.__response_data__ = response.data
        return self.__parse_data__()

    def delete_event(self, pk):
        response = http.request("DELETE", f"{API_URL}/events/{pk}")
        self.__response_data__ = response.data
        return self.__parse_data__()

    def post_event(self, payload):
        response = http.request("POST", f"{API_URL}/events", fields=payload)
        self.__response_data__ = response.data
        return self.__parse_data__()

    def put_change_event(self, pk, payload):
        response = http.request("PUT", f"{API_URL}/events/{pk}", fields=payload)
        self.__response_data__ = response.data
        return self.__parse_data__()

    def __parse_data__(self):
        return json.loads(self.__response_data__.decode("utf-8"))
