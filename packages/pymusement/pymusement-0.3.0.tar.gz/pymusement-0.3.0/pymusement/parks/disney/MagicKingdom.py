#!/usr/bin/env python
from pymusement.parks.disney.DisneyPark import DisneyPark
class MagicKingdom(DisneyPark):

    def __init__(self):
        super(MagicKingdom, self).__init__()

    def getId(self):
        return '80007944'

    def getName(self):
        return "Disney's Magic Kingdom"
    
    def get_api_id(self):
        return 'WaltDisneyWorldMagicKingdom'
