__author__ = 'Gabor Tanz'

import requests
from decimal import Decimal
from datetime import datetime, time


def get_bus_routes(number=''):
    method = BUS_PATHS['route_list']
    url = API_URLS['bus'] + method['path']
    params = {method['params']: number}

    response = requests.get(url, params=params).json()
    results = response[RESULTS['result']]
    routes = []
    if len(results) != 0:
        for r in results:
            route = BusRoute(r)
            route.corporation = r[RESULTS['route']['corporation']]
            route.set_first_last(r)
            route.set_first_last_low(r)
            routes.append(route)

    error = Error(response[RESULTS['error']['name']])

    return routes, error


def get_low_bus_routes(number=''):
    method = BUS_PATHS['route_list_low']
    url = API_URLS['bus'] + method['path']
    params = {method['params']: number}

    response = requests.get(url, params=params).json()
    results = response[RESULTS['result']]
    routes = []
    if len(results) != 0:
        for r in results:
            route = BusRoute(r)
            route.corporation = r[RESULTS['route']['corporation']]
            route.set_first_last(r)
            route.set_first_last_low(r)
            routes.append(route)

    error = Error(response[RESULTS['error']['name']])

    return routes, error


def get_night_bus_routes():
    method = BUS_PATHS['route_list_night']
    url = API_URLS['bus'] + method['path']

    response = requests.get(url).json()
    results = response[RESULTS['result']]
    routes = []
    if len(results) != 0:
        for r in results:
            route = BusRoute(r)
            route.subway_stations = r[RESULTS['route']['subway_stations']]
            route.set_first_last_night(r)
            route.set_first_last_low(r)
            routes.append(route)

    error = Error(response[RESULTS['error']['name']])

    return routes, error


def get_airport_bus_routes():
    method = BUS_PATHS['route_list_airport']
    url = API_URLS['bus'] + method['path']

    response = requests.get(url).json()
    results = response[RESULTS['result']]
    routes = []
    if len(results) != 0:
        for r in results:
            routes.append(BusRoute(r))

    error = Error(response[RESULTS['error']['name']])

    return routes, error


def get_route_info(route_id):
    method = BUS_PATHS['route_info']
    url = API_URLS['bus'] + method['path']
    params = {method['params']: route_id}

    response = requests.get(url, params=params).json()
    results = response[RESULTS['result']]
    if len(results) != 1:
        return

    route = BusRoute(results[0])
    error = Error(response[RESULTS['error']['name']])

    return route, error


class Error:
    code = 0
    message = ''

    def __init__(self, json):
        self.code = int(json[RESULTS['error']['code']])
        self.message = json[RESULTS['error']['message']]


class BusRoute:
    id = 0
    name = ''
    length = 0.0
    interval = 0
    type = 0
    start = ''
    end = ''
    corporation = ''
    first = 0
    last = 0
    first_low = 0
    last_low = 0
    subway_stations = []

    def __init__(self, json):
        self.id = int(json[RESULTS['route']['id']])
        self.name = json[RESULTS['route']['name']]
        self.length = Decimal(json[RESULTS['route']['length']])
        self.interval = int(json[RESULTS['route']['interval']])
        self.type = int(json[RESULTS['route']['type']])
        self.start = json[RESULTS['route']['start']]
        self.end = json[RESULTS['route']['end']]

    def set_first_last_low(self, json):
        if json[RESULTS['route']['first_low']] != ' ':
            dt = datetime.strptime(json[RESULTS['route']['first_low']], '%Y%m%d%H%M%S')
            self.first_low = time(dt.hour, dt.minute)
        if json[RESULTS['route']['last_low']] != ' ':
            dt = datetime.strptime(json[RESULTS['route']['last_low']], '%Y%m%d%H%M%S')
            self.last_low = time(dt.hour, dt.minute)

    def set_first_last(self, json):
        if json[RESULTS['route']['first']] != ' ':
            dt = datetime.strptime(json[RESULTS['route']['first']], '%Y%m%d%H%M%S')
            self.first = time(dt.hour, dt.minute)
        if json[RESULTS['route']['last']] != ' ':
            dt = datetime.strptime(json[RESULTS['route']['last']], '%Y%m%d%H%M%S')
            self.last = time(dt.hour, dt.minute)

    def set_first_last_night(self, json):
        if json[RESULTS['route']['first']] != ' ':
            dt = datetime.strptime(json[RESULTS['route']['first']], '%H:%M ')
            self.first = time(dt.hour, dt.minute)
        if json[RESULTS['route']['last']] != ' ':
            dt = datetime.strptime(json[RESULTS['route']['last']], '%H:%M ')
            self.last = time(dt.hour, dt.minute)


RESULTS = {
    'error': {
        'name': 'error',
        'code': 'errorCode',
        'message': 'errorMessage',
    },
    'result': 'resultList',
    'route': {
        'id': 'busRouteId',
        'name': 'busRouteNm',
        'length': 'length',
        'interval': 'term',
        'type': 'routeType',
        'start': 'stStationNm',
        'end': 'edStationNm',
        'corporation': 'corpNm',
        'first': 'firstBusTm',
        'last': 'lastBusTm',
        'first_low': 'firstLowTm',
        'last_low': 'lastLowTm',
        'subway_stations': 'subwayNm',
    },
}

API_URLS = {
    'bus': 'http://m.bus.go.kr/mBus/bus/',
    'subway': 'http://m.bus.go.kr/mBus/subway/',
    'path': 'http://m.bus.go.kr/mBus/path/'
}

BUS_PATHS = {
    'route_info': {
        'path': 'getRouteInfo.bms',
        'params': 'busRouteId',
    },
    'route_list': {
        'path': 'getBusRouteList.bms',
        'params': 'strSrch',
    },
    'route_list_low': {
        'path': 'getLowBusRoute.bms',
        'params': 'strSrch',
    },
    'route_list_night': {
        'path': 'getNBusRoute.bms',
    },
    'route_list_airport': {
        'path': 'getAirBusRoute.bms',
    },
    'route_list_by_type': {
        'path': 'getRttpRoute.bms',
        'params': ['strSrch', 'stRttp'],
    },
    'route_path': {
        'path': 'getRoutePath.bms',
        'params': 'busRouteId',
    },
    'route_path_detailed': {
        'path': 'getStaionByRoute.bms',
        'params': 'busRouteId',
    },
    'route_path_realtime': {
        'path': 'getRttpRouteAndPos.bms',
        'params': 'busRouteId',
    },
    'route_path_realtime_low': {
        'path': 'getLowRouteAndPos.bms',
        'params': 'busRouteId',
    },
    'arrival_info_by_route': {
        'path': 'getArrInfoByRouteAll.bms',
        'params': 'busRouteId',
    },
    'arrival_info_by_route_and_station': {
        'path': 'getArrInfoByRoute.bms',
        'params': ['busRouteId', 'stId', 'ord'],
    },
    'stations_by_position': {
        'path': 'getStationByPos.bms',
        'params': ['tmX', 'tmY', 'radius'],
    },
    'routes_by_position': {
        'path': 'getNearRouteByPos.bms',
        'params': ['tmX', 'tmY', 'radius'],
    },
    'station_by_name': {
        'path': 'getStationByName.bms',
        'params': 'stSrch',
    },
    'station_by_name_low': {
        'path': 'getLowStationByName.bms',
        'params': 'stSrch',
    },
    'routes_by_station': {
        'path': 'getRouteByStation.bms',
        'params': 'arsId',
    },
    'routes_by_station_realtime': {
        'path': 'getStationByUid.bms',
        'params': 'arsId',
    },
    'routes_by_station_realtime_low': {
        'path': 'getLowStationByUid.bms',
        'params': 'arsId',
    },
    'operating_times_by_station_and_route': {
        'path': 'getBustimeByStation.bms',
        'params': ['arsId', 'busRouteId'],
    },
    'bus_position_by_route': {
        'path': 'getBusPosByRtid.bms',
        'params': ['busRouteId'],
    },
    'bus_position_by_route_low': {
        'path': 'getLowBusPosByRtid.bms',
        'params': ['busRouteId'],
    },
    'bus_position_by_vehicle': {
        'path': 'getBusPosByVehId.bms',
        'params': ['vehId'],
    },
}

PATH_PATHS = {
    'closest_station_by_position': {
        'path': 'getNearStationByPos.bms',
        'params': ['tmX', 'tmY', 'radius'],
    },
    'location_by_name': {
        'path': 'getLocationInfo.bms',
        'params': ['stSrch'],
    },
    'path_by_bus': {
        'path': 'getPathInfoByBus.bms',
        'params': ['startX', 'startY', 'endX', 'endY'],
    },
    'path_by_subway': {
        'path': 'getPathInfoBySubway.bms',
        'params': ['startX', 'startY', 'endX', 'endY'],
    },
    'path_by_bus_and_subway': {
        'path': 'getPathInfoByBusNSub.bms',
        'params': ['startX', 'startY', 'endX', 'endY'],
    },
}

SUBWAY_PATHS = {
    'station_by_route': {
        'path': 'getStatnByRoute.bms',
        'params': ['subwayId'],
    },
    'station_by_name': {
        'path': 'getStatnByNm.bms',
        'params': ['statnNm'],
    },
    'arrival_info_by_route_and_station': {
        'path': 'getArvlByInfo.bms',
        'params': ['subwayId', 'statnId'],
    },
    'station_by_id': {
        'path': 'getStatnById.bms',
        'params': ['subwayId', 'statnId'],
    },
    'timetable_by_station': {
        'path': 'getPlanByStatn.bms',
        'params': ['subwayId', 'statnId', 'tabType'],
    },
    'last_train_by_station': {
        'path': 'getLastcarByStatn.bms',
        'params': ['subwayId', 'statnId'],
    },
    'bus_by_station': {
        'path': 'getBusByStation.bms',
        'params': ['statnId'],
    },
    'station_position_by_id': {
        'path': 'getStatnByIdPos.bms',
        'params': ['subwayId', 'statnId'],
    },
    'entrance_info_by_station': {
        'path': 'getEntrcByInfo.bms',
        'params': ['statnId'],
    },
    'train_info_by_station': {
        'path': 'getStatnTrainInfo.bms',
        'params': ['subwayId', 'statnId'],
    },
}

BUS_TYPES = {
    'airport': 1,
    'village': 2,
    'trunk': 3,
    'branch': 4,
    'circle': 5,
    'express': 6,
    'incheon': 7,
    'gyeongi': 8,
    'public': 0,
}