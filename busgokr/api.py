#!/usr/bin/env python3

from datetime import time
from datetime import datetime as dt
from decimal import Decimal
from urllib.parse import quote_plus
import requests

from busgokr import endpoints
from busgokr.exceptions import *


class BusRoute:
    def __init__(self, data):
        self.id = int(data.get('busRouteId'))
        if data.get('firstBusTm'):
            if not data.get('firstBusTm').isspace():
                self.first_bus = dt.strptime(data.get('firstBusTm'), "%Y%m%d%H%M%S")
        if data.get('lastBusTm'):
            if not data.get('lastBusTm').isspace():
                self.last_bus = dt.strptime(data.get('lastBusTm'), "%Y%m%d%H%M%S")
        if data.get('firstLowTm'):
            if not data.get('firstLowTm').isspace():
                self.first_low_bus = dt.strptime(data.get('firstLowTm'), "%Y%m%d%H%M%S")
        if data.get('lastLowTm'):
            if not data.get('lastLowTm').isspace():
                self.last_low_bus = dt.strptime(data.get('lastLowTm'), "%Y%m%d%H%M%S")
        if data.get('routeType'):
            self.route_type = int(data.get('routeType'))
        else:
            self.route_type = None
        self.interval = int(data.get('term'))
        self.name = data.get('busRouteNm')
        self.length = float(data.get('length'))
        self.start_station = data.get('stStationNm')
        self.end_station = data.get('edStationNm')
        self.waypoints = []
        self.corporation = None

    def get_waypoints(self):
        if len(self.waypoints) == 0:
            self.waypoints = get_bus_route_waypoints(self.id)
        return self.waypoints

    def set_corporation(self, data):
        self.corporation = data.get('corpNm')

    def __str__(self):
        return self.name

    def __len__(self):
        return self.length


class Coordinates:
    def __init__(self, data):
        if data.get('gpsX'):
            self.x_gps = Decimal(data.get('gpsX'))
            self.y_gps = Decimal(data.get('gpsY'))
        else:
            self.x_gps = Decimal(data.get('tmX'))
            self.y_gps = Decimal(data.get('tmY'))
        self.x_korea1985 = Decimal(data.get('posX'))
        self.y_korea1985 = Decimal(data.get('posY'))

    def __str__(self):
        return '{0}/{1}'.format(self.x_gps, self.y_gps)


class BusRouteWaypoint:
    def __init__(self, data):
        self.coordinates = Coordinates(data)
        self.station_number = int(data.get('stationNo'))
        self.station_name = data.get('stationNm')
        self.station_id = int(data.get('station'))
        self.direction = data.get('direction')
        self.turnaround_station = int(data.get('trnstnid'))
        self.section_speed = int(data.get('sectSpd'))
        self.station_serial_number = data.get('arsId')  # don't convert to int to keep leading zero
        self.section_id = int(data.get('section'))
        if data.get('transYn') == 'Y':
            self.is_turnaround_station = True
        else:
            self.is_turnaround_station = False
        self.route_type = int(data.get('routeType'))  # redundant if part of busroute
        self.route_name = data.get('busRouteNm')  # redundant if part of busroute
        self.sequence_number = int(data.get('seq'))
        if data.get('lastTm'):
            h, m = [int(x) for x in data.get('lastTm').split(":")]
            self.last_bus = time(h, m)
        if data.get('firstTm'):
            h, m = [int(x) for x in data.get('firstTm').split(":")]
            self.first_bus = time(h, m)
        self.section_distance = int(data.get('fullSectDist'))


class BusArrivalInfo:
    def __init__(self, data):
        self.station_id = int(data.get('stId'))
        self.station_name = data.get('stNm')
        self.station_serial_number = data.get('arsId')
        self.route_id = data.get('busRouteId')
        self.route_name = data.get('rtNm')
        if data.get('firstTm'):
            if not data.get('firstTm').isspace():
                self.first_bus = dt.strptime(data.get('firstTm'), "%Y%m%d%H%M%S")
        if data.get('lastTm'):
            if not data.get('lastTm').isspace():
                self.first_bus = dt.strptime(data.get('lastTm'), "%Y%m%d%H%M%S")
        self.interval = int(data.get('term'))
        self.route_type = int(data.get('routeType'))  # redundant if part of busroute
        if data.get('nextBus') == 'Y':
            self.last_bus_from_station = True
        else:
            self.last_bus_from_station = False
        self.station_order = int(data.get('staOrd'))
        self.direction = data.get('dir')
        self.requested_time = dt.strptime(data.get('mkTm'), "%Y-%m-%d %H:%M:%S.%f")
        self.arriving_vehicle = ArrivingVehicle(data,1)
        self.next_vehicle = ArrivingVehicle(data,2)


class ArrivingVehicle:
    def __init__(self, data, num):
        self.id = int(data.get('vehId{0}'.format(num)))
        self.number = data.get('plainNo{0}'.format(num))
        self.current_section_id = int(data.get('sectOrd{0}'.format(num)))
        self.final_station_name = data.get('stationNm{0}'.format(num))
        self.traveling_minutes = int(data.get('traTime{0}'.format(num)))
        self.traveling_speed = int(data.get('traSpd{0}'.format(num)))
        if data.get('isArrive{0}'.format(num)) == '1':
            self.has_arrived = True
        else:
            self.has_arrived = False
        if data.get('isLast{0}'.format(num)) == '1':
            self.is_last_bus = True
        else:
            self.is_last_bus = False
        self.vehicle_type = int(data.get('busType{0}'.format(num)))
        self.moving_average_correction_factor = data.get('avgCf{0}'.format(num))
        self.exponential_smoothing_correction_factor = data.get('expCf{0}'.format(num))
        # TODO
        # A lot more properties api.bus.go.kr/contents/sub02/getArrInfoByRouteAll.html


class BusStation:
    def __init__(self, data):
        self.coordinates = Coordinates(data)
        if data.get('stationId'):
            self.id = int(data.get('stationId'))
        else:
            self.id = int(data.get('stId'))
        if data.get('stationNm'):
            self.name = data.get('stationNm')
        else:
            self.name = data.get('stNm')
        self.serial_number = data.get('arsId')
        if data.get('stationTp'):
            self.station_type = int(data.get('stationTp'))
        else:
            self.station_type = None
        self.distance = None
    
    def set_distance_to_coordinates(self, x, y, data):
        if not self.distance:
            self.distance = {}
        self.distance[(x, y)] = int(data.get('dist'))


def get_bus_route(route_id=None, name=None):
    errors = []
    if not (route_id or name):
        raise MissingParameters("Either id or name are required for route retrieval, none provided.")
    if route_id:
        try:
            return bus_route_info(route_id)
        except IDNotFound as e:
            errors.append(e.value)
    if name:
        try:
            routes = bus_route_search(name)
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
            return bus_route_type_search(name, route_type)
        except NameNotFound as e:
            errors.append(e.value)
    try:
        return bus_route_search(name)
    except NameNotFound as e:
        errors.append(e.value)
    raise BusRouteNotFound(' ,'.join(errors))


def get_bus_route_waypoints(route_id=None):
    errors = []
    if not route_id:
        raise MissingParameters("Id is required for waypoint retrieval, none provided.")
    try:
        return bus_route_waypoints(route_id)
    except IDNotFound as e:
        errors.append(e.value)
    raise BusRouteNotFound(' ,'.join(errors))


# Bus.go.kr endpoints
def bus_route_info(route_id):
    url = endpoints.bus_route_by_id.format(route_id)
    q = _query_endpoint(url)
    if q:
        b = BusRoute(q[0])
        b.set_corporation(q[0])
        return b
    else:
        raise IDNotFound('No busroute with id {0} found.'.format(route_id))


def bus_route_search(name):
    url = endpoints.bus_route_search.format(name)
    q = _query_endpoint(url)
    if q:
        routes = []
        for r in q:
            b = BusRoute(r)
            b.set_corporation(r)
            routes.append(b)
        return routes
    else:
        raise NameNotFound('No busroutes with name {0} found.'.format(name))


def bus_route_type_search(name, route_type):
    url = endpoints.bus_routes_by_type.format(name, route_type)
    q = _query_endpoint(url)
    if q:
        routes = []
        for r in q:
            b = BusRoute(r)
            b.set_corporation(r)
            routes.append(b)
        return routes
    else:
        raise NameNotFound('No busroutes with name {0} and type {1} found.'.format(name, route_type))


def bus_route_coordinates(route_id):
    url = endpoints.route_path_by_id.format(route_id)
    q = _query_endpoint(url)
    if q:
        coordinates = []
        for c in q:
            coordinates.append(Coordinates(c))
        return coordinates
    else:
        raise IDNotFound('No busroute with id {0} found.'.format(route_id))


def bus_route_waypoints(route_id):
    url = endpoints.route_path_detailed_by_id.format(route_id)
    q = _query_endpoint(url)
    if q:
        waypoints = []
        for w in q:
            waypoints.append(BusRouteWaypoint(w))
        return waypoints
    else:
        raise IDNotFound('No busroute with id {0} found.'.format(route_id))


def bus_route_all_arrival_info(route_id):
    url = endpoints.bus_arrival_info_by_route.format(route_id)
    q = _query_endpoint(url)
    if q:
        arrival_info = []
        for a in q:
            arrival_info.append(BusArrivalInfo(a))
        return arrival_info
    else:
        raise IDNotFound('No busroute with id {0} found.'.format(route_id))


def bus_stations_position_search(x, y, radius):
    url = endpoints.bus_stations_by_position.format(x, y, radius)
    q = _query_endpoint(url)
    if q:
        stations = []
        for b in q:
            bs = BusStation(b)
            bs.set_distance_to_coordinates(x, y, b)
            stations.append(bs)
        return stations
    else:
        raise NoStationAtPosition('No bus station within {0} of {1}/{2} found.'.format(radius, x, y))    


def bus_route_position_search(x, y, radius):
    url = endpoints.routes_by_position.format(x, y, radius)
    q = _query_endpoint(url)
    if q:
        routes = []
        for r in q:
            routes.append(BusRoute(r))
        return routes
    else:
        raise NoRouteAtPosition('No bus route within {0} of {1}/{2} found.'.format(radius, x, y))


def bus_station_search(name):
    url = endpoints.bus_stations_by_name.format(quote_plus(quote_plus(name)))  # needs to be urlencoded 2 times
    q = _query_endpoint(url)
    if q:
        stations = []
        for b in q:
            stations.append(BusStation(b))
        return stations
    else:
        raise NameNotFound('No bus station with Name: {0} found.'.format(name))


def bus_routes_by_station(serial):
    url = endpoints.routes_by_bus_station.format(serial)
    q = _query_endpoint(url)
    if q:
        routes = []
        for r in q:
            routes.append(BusRoute(r))
        return routes
    else:
        raise BusRouteNotFound('No bus routes at serial: {0} found.'.format(serial))


def _query_endpoint(url):
    try:
        resp = requests.get(url)
        data = resp.json()        
        resp.close()
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
