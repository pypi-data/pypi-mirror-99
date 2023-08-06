from pymusement.parks.universal.UniversalStudiosFlorida import UniversalStudiosFlorida
from pymusement.parks.universal.IslandsOfAdventure import IslandsOfAdventure
from pymusement.parks.universal.UniversalHollywood import UniversalHollywood
from pymusement.parks.universal.UniversalVolcano import UniversalVolcano
from pymusement.parks.HersheyPark import HersheyPark
from pymusement.parks.disney.AnimalKingdom import AnimalKingdom
from pymusement.parks.disney.CaliforniaAdventure import CaliforniaAdventure
from pymusement.parks.disney.Disneyland import Disneyland
from pymusement.parks.disney.Epcot import Epcot
from pymusement.parks.disney.HollywoodStudios import HollywoodStudios
from pymusement.parks.disney.MagicKingdom import MagicKingdom

PARKS = {
    'universal-florida' : UniversalStudiosFlorida(),
    'islands-adventure' : IslandsOfAdventure(),
    'universal-hollywood' : UniversalHollywood(),
    'volcano-bay' : UniversalVolcano(),
    'hersheypark' : HersheyPark(),
    'magic-kingdom' : MagicKingdom(),
    'animal-kingdom' : AnimalKingdom(),
    'epcot' : Epcot(),
    'hollywood-studios':HollywoodStudios(),
    'disneyland': Disneyland(),
    'california-adventure' : CaliforniaAdventure()
}
