#!/usr/env/bin python3

class BaseError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return self.value


class MissingParameters(BaseError):
    pass


class ApiError(BaseError):
    pass


class IDNotFound(BaseError):
    pass


class NameNotFound(BaseError):
    pass


class BusRouteNotFound(BaseError):
    pass


class NoStationAtPosition(BaseError):
    pass


class NoRouteAtPosition(BaseError):
    pass
