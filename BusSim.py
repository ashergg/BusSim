import numpy as np
from numpy.random import randint
import warnings


class Station():
    """
        A class for bus stations
        
        Station objets do not update each time step, rather give the bus
        object that gets to its location the number of the passengers that
        are waiting to board the bus.
        
    """
    def __init__(self, location, rate):
        self.location = location
        self.rate = rate
        self.passengers = 0
        self.lastBus = 0
        self.occupied = False
    def busStop(self, currentTime):
        self.occupied = True
        timefromlast = currentTime - self.lastBus
        passengers = np.random.poisson(timefromlast*self.rate/60)
        return passengers
    def busLeave(self, currentTime):
        self.lastBus = currentTime
        self.occupied = False
    def getLocation(self):
        return [self.location, 0]


class Bus():
    def __init__(self, route, baseStopTime=3, boardingRate=0.5):
        self.route = route
        self.baseStopTime = baseStopTime
        self.boardingRate = boardingRate
        self.location = 0
        self.occupancy = 0
        self.wait = 0
        self.currentStation = None
        if len(self.route.getStations()) == 0:
            warnings.warn('Warning: Created a bus without any stops!')
            self.nextStop = None
        else:
            self.nextStop = self.route.getStations()[0]
        self.nextStopIndex = 0
    def makestep(self, currentTime):
        if self.wait > 1:
            self.wait -= 1
        elif self.wait == 1:
            self.currentStation.busLeave(currentTime)
            self.wait = 0
            self.currentStation = None
            if not self.nextStop:
                self.route.remove_bus(self)
        else:
            self.location += 1
            if self.location == self.nextStop.location:
                self.currentStation = self.nextStop
                passengers = self.currentStation.busStop(currentTime)
                self.wait = self.baseStopTime + int(passengers*self.boardingRate)
                self.occupancy += passengers
                try:
                    self.nextStop = self.route.getStations()[self.nextStopIndex + 1]
                except:
                    self.nextStop = None
                self.nextStopIndex += 1
    def getLocation(self):
        return [self.location, 0]


class Route():
    def __init__(self, busRate=10):
        self.busRate = busRate
        self.buses = []
        self.stations = []
    def setStations(self, count=20, interval=90, minrate=1, maxrate=6):
        self.stations = [Station((i+1)*interval, randint(minrate, maxrate)) for i in range(count)]
    def getStations(self):
        return self.stations
    def makeStep(self, currentTime):
        if currentTime%(self.busRate*10) == 0:
            self.buses.append(Bus(self))
        for bus in self.buses:
            bus.makestep(currentTime)
        self.draw()
    def getBuses(self):
        return [bus.getLocation for bus in self.buses]
    def remove_bus(self, bus):
        self.buses.remove(bus)
    def draw(self):
        pass
    def runSim(self, duration, **kwargs):
        """runs a simulation of length {duration} seconds"""
        self.buses = []
        self.setStations(**kwargs)
        #TODO: Error handling for wrong/insufficient kwargs
        for i in range(duration):
            self.makeStep(i)


if __name__ == '__main__':
    route = Route()
    route.runSim(3600)

