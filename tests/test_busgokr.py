#!/usr/bin/env python3

import unittest

from busgokr import *

class EndpointTests(unittest.TestCase):
    def setUp(self):
        self.startTime = dt.now()

    def tearDown(self):
        t = dt.now() - self.startTime
        print("%s: %s" % (self.id(), t))

    def test_bus_route_search(self):
        routes = bus_route_search(1000)
        self.assertIsInstance(routes, list)
        self.assertIsInstance(routes[0], BusRoute)

        with self.assertRaises(NameNotFound):
            bus_route_search(10000)

    def test_bus_route_info(self):
        route = bus_route_info(122900001)
        self.assertIsInstance(route, BusRoute)

        with self.assertRaises(IDNotFound):
            bus_route_info(9999)

    def test_bus_route_type_search(self):
        routes = bus_route_type_search("01", 1)
        self.assertIsInstance(routes, list)
        self.assertIsInstance(routes[0], BusRoute)

        with self.assertRaises(NameNotFound):
            bus_route_type_search("0", 9)

        with self.assertRaises(NameNotFound):
            bus_route_type_search("999", 1)

    def test_bus_route_coordinates(self):
        coordinates = bus_route_coordinates(122900001)
        self.assertIsInstance(coordinates, list)
        self.assertIsInstance(coordinates[0], Coordinates)

        with self.assertRaises(IDNotFound):
            bus_route_coordinates(999)

    def test_bus_route_waypoints(self):
        waypoints = bus_route_waypoints(122900001)
        self.assertIsInstance(waypoints, list)
        self.assertIsInstance(waypoints[0], BusRouteWaypoint)

        with self.assertRaises(IDNotFound):
            bus_route_waypoints(888)

    def test_bus_route_all_arrival_info(self):
        info = bus_route_all_arrival_info(122900001)
        self.assertIsInstance(info, list)
        self.assertIsInstance(info[0], BusArrivalInfo)

        with self.assertRaises(IDNotFound):
            bus_route_all_arrival_info(999)
    
    def test_bus_stations_position_search(self):
        stations = bus_stations_position_search(127.056737, 37.477838, 100)
        self.assertIsInstance(stations, list)
        self.assertIsInstance(stations[0], BusStation)

        with self.assertRaises(NoStationAtPosition):
            bus_stations_position_search(1, 2, 3)

    def test_bus_route_position_search(self):
        routes = bus_route_position_search(127.056737, 37.477838, 100)
        self.assertIsInstance(routes, list)
        self.assertIsInstance(routes[0], BusRoute)

        with self.assertRaises(NoRouteAtPosition):
            bus_route_position_search(1, 2, 3)

    def test_bus_station_search(self):
        stations = bus_station_search('강남')
        self.assertIsInstance(stations, list)
        self.assertIsInstance(stations[0], BusStation)

        with self.assertRaises(NameNotFound):
            bus_station_search('help')

if __name__ == '__main__':
    unittest.main()
