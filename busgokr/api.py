#!/usr/bin/env python3

from datetime import datetime

import requests

from busgokr import endpoints
from busgokr.exceptions import *


class BusRoute:
    def __init__(self, data):
        self.id = data.get('busRouteId')
        self.corporation = data.get('corpNm')
        if not data.get('firstBusTm').isspace():
            self.first_bus = datetime.strptime(data.get('firstBusTm'), "%Y%m%d%H%M%S")
        if not data.get('lastBusTm').isspace():
            self.last_bus = datetime.strptime(data.get('lastBusTm'), "%Y%m%d%H%M%S")
        if not data.get('firstLowTm').isspace():
            self.first_low_bus = datetime.strptime(data.get('firstLowTm'), "%Y%m%d%H%M%S")
        if not data.get('lastLowTm').isspace():
            self.last_low_bus = datetime.strptime(data.get('lastLowTm'), "%Y%m%d%H%M%S")
        self.route_type = data.get('routeType')
        self.interval = data.get('term')
        self.name = data.get('busRouteNm')
        self.length = data.get('length')
        self.start_station = data.get('stStationNm')
        self.end_station = data.get('edStationNm')

    def __str__(self):
        return self.name

    def __len__(self):
        return self.length


def get_bus_route(route_id=None, name=None):
    errors = []
    if not (route_id or name):
        raise MissingParameters("Either id or name are required for route retrieval, none provided.")
    if route_id:
        try:
            return route_info(route_id)
        except IDNotFound as e:
            errors.append(e.value)
    if name:
        try:
            routes = search_route(name)
            if len(routes) == 1:
                return routes[0]
            else:
                return routes
        except NameNotFound as e:
            errors.append(e.value)
    raise BusRouteNotFound(' ,'.join(errors))


def get_bus_route_list(name='', route_type=None):
    errors = []
    if route_type and len(name) > 0:
        try:
            return search_route_type(name, route_type)
        except NameNotFound as e:
            errors.append(e.value)
    try:
        return search_route(name)
    except NameNotFound as e:
        errors.append(e.value)
    raise BusRouteNotFound(' ,'.join(errors))


def route_info(route_id):
    url = endpoints.bus_route_by_id.format(route_id)
    q = _query_endpoint(url)
    if q:
        return BusRoute(q[0])
    else:
        raise IDNotFound('No busroute with id {0} found.'.format(route_id))


def search_route(name):
    url = endpoints.bus_route_search.format(name)
    q = _query_endpoint(url)
    if q:
        routes = []
        for r in q:
            routes.append(BusRoute(r))
        return routes
    else:
        raise NameNotFound('No busroutes with name {0} found.'.format(name))


def search_route_type(name, route_type):
    url = endpoints.bus_routes_by_type.format(name, route_type)
    q = _query_endpoint(url)
    if q:
        routes = []
        for r in q:
            routes.append(BusRoute(r))
        return routes
    else:
        raise NameNotFound('No busroutes with name {0} and type {1} found.'.format(name, route_type))


def _query_endpoint(url):
    try:
        data = requests.get(url).json()
    except requests.HTTPError as e:
        raise e
    except requests.URLRequired as e:
        raise e

    if data['error']['errorCode'] == '0000':
        if 'resultList' in data.keys():
            if data['resultList']:
                return data['resultList']
            else:
                return None
        else:
            return None
    else:
        raise ApiError(data['error'])


def get_route_waypoints(route_id):
    method = BUS_PATHS['route_waypoints']
    url = API_URLS['bus'] + method['path']
    params = {method['params']: route_id}

    response = requests.get(url, params=params).json()
    error = Error(response[RESULTS['error']['name']])
    if error.code != 0:
        return error

    results = response[RESULTS['result']]
    waypoints = []
    if len(results) != 0:
        for r in results:
            longitude = r[RESULTS['waypoints']['longitude']]
            latitude = r[RESULTS['waypoints']['latitude']]
            waypoint = {'longitude': longitude, 'latitude': latitude}
            waypoints.append(waypoint)

    return waypoints


class Error:
    code = 0
    message = ''

    def __init__(self, json):
        self.code = int(json[RESULTS['error']['code']])
        self.message = json[RESULTS['error']['message']]


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
    'waypoints': {
        'longitude': 'gpsX',
        'latitude': 'gpsY',
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
    'route_waypoints': {
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
