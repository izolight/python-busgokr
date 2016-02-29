#!/usr/env/bin python3

import unittest

from busgokr.api import *


class EndpointTests(unittest.TestCase):
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

    def test_bus_route_waypoints(self):
        waypoints = bus_route_waypoints(122900001)
        self.assertIsInstance(waypoints, list)
        self.assertIsInstance(waypoints[0], BusRouteWaypoint)

        with self.assertRaises(IDNotFound):
            bus_route_waypoints(999)

    def test_bus_route_waypoints_detail(self):
        waypoints = bus_route_waypoints_detail(122900001)
        self.assertIsInstance(waypoints, list)
        self.assertIsInstance(waypoints[0], BusRouteWaypointDetailed)

        with self.assertRaises(IDNotFound):
            bus_route_waypoints_detail(888)
