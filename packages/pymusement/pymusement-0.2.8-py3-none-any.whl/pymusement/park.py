import datetime

# Required to supress some insecure cert warnings
# Normally, this is bad.
import requests

class Park(object):
    def __init__(self):
        self._rides = []
        self._shows = []
        self._time = datetime.datetime.now()
        self.is_Open = False
        self.Capacity = False
        self.park_hours = ''

    def set_open(self):
        self.is_Open = True
        
    def set_closed(self):
        self.is_Open = False
        
    def rides(self):
        if self._rides == []:
            self._buildPark()
        return self._rides

    def update_time(self):
        return self._time

    def shows(self):
        if self._shows == []:
            self._buildPark()
        return self._shows

    def addRide(self, ride):
        self._rides.append(ride)

    def addShow(self, show):
        self._shows.append(show)

    def setName(self, name):
        self.name = name

    def getName(self):
        raise('This must be implemented')
    
    def get_park_hours():
        raise('This must be implemented')
    
    def _buildPark(self):
        raise('This must be implemented')
