class Config(object):
    API_URLS = {
        'bus': 'http://m.bus.go.kr/mBus/bus/',
        'subway': 'http://m.bus.go.kr/mBus/subway/',
        'path': 'http://m.bus.go.kr/mBus/path/'
    }

    BUS_PATHS = {
        'route_info': {
            'path': 'getRouteInfo.bms',
            'params': ['busRouteId'],
        },
        'route_list': {
            'path': 'getBusRouteList.bms',
            'params': ['strSrch'],
        },
        'route_list_low': {
            'path': 'getLowBusRoute.bms',
            'params': ['strSrch'],
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
            'params': ['busRouteId'],
        },
        'route_path_detailed': {
            'path': 'getStaionByRoute.bms',
            'params': ['busRouteId'],
        },
        'route_path_realtime': {
            'path': 'getRttpRouteAndPos.bms',
            'params': ['busRouteId'],
        },
        'route_path_realtime_low': {
            'path': 'getLowRouteAndPos.bms',
            'params': ['busRouteId'],
        },
        'arrival_info_by_route': {
            'path': 'getArrInfoByRouteAll.bms',
            'params': ['busRouteId'],
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
            'params': ['stSrch'],
        },
        'station_by_name_low': {
            'path': 'getLowStationByName.bms',
            'params': ['stSrch'],
        },
        'routes_by_station': {
            'path': 'getRouteByStation.bms',
            'params': ['arsId'],
        },
        'routes_by_station_realtime': {
            'path': 'getStationByUid.bms',
            'params': ['arsId'],
        },
        'routes_by_station_realtime_low': {
            'path': 'getLowStationByUid.bms',
            'params': ['arsId'],
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