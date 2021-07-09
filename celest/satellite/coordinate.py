"""
"""


from celest.core.decorators import set_module
from celest.satellite import Time, Interpolation
from celest.encounter import GroundPosition
import numpy as np


@set_module('celest.satellite')
class Coordinate(object):
    """
    """

    def __init__(self, basePos: np.array, type: str, timeData: Time, factor: int=0) -> None:
        """Initialize attributes."""

        self.time = timeData

        self._GEO = None
        self._ERA = None
        self._ICRS = None
        self._GCRS = None
        self._ITRS = None
        self._CIRS = None
        self._horizontal = None
        self._off_nadir = None
        self._altitude = None
        self._distance = None
        self._equatorial = None
        self._ecliptic = None
        self._galactic = None
        self._super_galactic = None

        self.interp = Interpolation()

        self.length = None
        self._set_base_position(basePos, type, factor)
    
    def _set_base_position(self, basePos: np.array, type: str, factor: int) -> None:
        pass
    
    def GEO(self, **kwargs) -> np.array:
        pass
    
    def ERA(self, **kwargs) -> np.array:
        pass
    
    def ICRS(self, **kwargs) -> np.array:
        pass
    
    def GCRS(self, **kwargs) -> np.array:
        pass
    
    def ITRS(self, **kwargs) -> np.array:
        pass
    
    def CIRS(self, **kwargs) -> np.array:
        pass
    
    def horizontal(self, goundPos: GroundPosition, **kwargs) -> np.array:
        pass
    
    def off_nadir(self, groundPos: GroundPosition, **kwargs) -> np.array:
        pass
    
    def altitude(self, **kwargs) -> np.array:
        """Get the altitude above Earth's surface.

        Parameters
        ----------
        kwargs : dict, optional
            Optional keyword arguments passed into the `Interpolation()`
            callable.

        Returns
        -------
        np.array
            Array of shape (n,) containing time varying altitudes.
        
        Notes
        -----
        This method implements WGS84 to calculate the Earth's radius before
        computing the positions altitude.
        """

        if type(self._altitude) != type(None):
            if kwargs:
                return self.interp(self._altitude)
            else:
                return self._altitude

        if type(self._ITRS) == type(None):
            self.ITRS()

        ITRSdata = self._ITRS
        x = ITRSdata[:, 0]
        y = ITRSdata[:, 1]
        z = ITRSdata[:, 2]
        arg = np.sqrt(x**2 + y**2) / z
        lattitude = np.arctan(arg)

        earthRadius = self._WGS84_radius(lattitude)
        satRadius = np.linalg.norm(ITRSdata, axis=1)

        altitude = satRadius - earthRadius
        self._altitude = altitude

        if kwargs:
            altitude = self.interp(altitude, **kwargs)

        return altitude
    
    def distance(self, groundPos: GroundPosition, **kwargs) -> np.array:
        pass
    
    def equatorial(self, **kwargs) -> np.array:
        pass
    
    def ecliptic(self, **kwargs) -> np.array:
        pass
    
    def galactic(self, **kwargs) -> np.array:
        pass
    
    def super_galactic(self, **kwargs) -> np.array:
        pass
    
    def sexagesimal(self, angles: np.array) -> np.array:
        """Convert decimal angles into sexagesimal angles.

        Parameters
        ----------
        angles : np.array
            Array of shape (n,) containing angles in decimal degrees.

        Returns
        -------
        np.array
            Array of shape (n,) containing sexagesimal angles as strings.
        """

        length = angles.shape[0]
        sexagesimalAng = np.empty((length,), dtype="<U32")

        for i in range(length):

            num = angles[i]
            sign = "+" if num >= 0 else "-"
            degrees = str(int(abs(num) - num % 1)).zfill(2)
            minutes = str(int(60 * (num % 1) - (60 * (num % 1)) % 1)).zfill(2)
            seconds = "{:.3f}".format(60 * ((60 * (num % 1)) % 1)).zfill(5)
            degree_symbol = u"\u00B0"
            minute_symbol = u"\u2032"
            second_symbol = u"\u2033"
            sexagesimalAng[i] = f"{sign}{degrees}{degree_symbol}{minutes}{minute_symbol}{seconds}{second_symbol}"

        return sexagesimalAng