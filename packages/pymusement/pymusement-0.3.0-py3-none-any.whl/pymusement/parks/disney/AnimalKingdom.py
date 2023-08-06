#!/usr/bin/env python
from pymusement.parks.disney.DisneyPark import DisneyPark
class AnimalKingdom(DisneyPark):

    def __init__(self):
        super(AnimalKingdom, self).__init__()

    def getId(self):
        return '80007823'

    def getName(self):
        return "Disney's Animal Kingdom"
   
    def get_api_id(self):
        return 'WaltDisneyWorldAnimalKingdom'

