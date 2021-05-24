"""Ground position information localization.

The groundposition module contains the GroundPosition class used to localize
information ties to a specific ground location. The GroundPosition class is
used in conjunction with both the Satellite and Encounter class' to manage
altitude, azimuth, nadir angle, and window information. In short, the
GroundPosition class was created for managerial purposes.
"""


from math import sin, cos, sqrt, radians
import numpy as np
from typing import Tuple


class GroundPosition(object):
    """Localize ground position based information.

    The GoundPosition class stores ground location data and is used in the
    Satellite and Encounter class' to manage altitude, azimuth, nadir angle,
    and window information.

    Parameters
    ----------
    name : str
        Name of ground location used for identification and indexing.
    coor : tuple
        Geodetic coordinates for the ground position location given in decimal
        degrees in the (latitude, longitude) format.

    Attributes
    ----------
    name : str
        Name of ground location used for identification and indexing.
    coor : tuple
        Geodetic coordinates for the ground position location given in decimal
        degrees in the (latitude, longitude) format.
    radius : float
        Radius of earths surface at the given coordinates using WGS84.
    ECEFpos : np.ndarray
        Array of shape (3,) representing the GroundPosition location in the
        ECEF cartesian frame.
    alt : np.ndarray
        Altitude data as an array of shape (n,) given in degrees.
    az : np.ndarray
        Azimuth data as an array of shape (n,) given in degrees.
    nadirAng : np.ndarray
        Nadir angle data as an array of shape (n,) given in degrees.
    length : int
        Length, n, of data attributes.

    Methods
    -------
    getRadius(obsCoor)
        Used to instantiate the radius attribute.
    getECEF(obsCoor, radius)
        Used to instantiate the ECEFpos attribute.

    Examples
    --------
    >>> toronto = GroundPosition(name="Toronto", coor=(43.662300, -79.394530))
    """
    def __init__(self, name: str, coor: Tuple[float, float]) -> None:
        """Define instance variables."""
        self.name = name
        self.coor = coor
        self.radius = self.getRadius(coor)
        self.ECEFpos = self.getECEF(coor, self.radius)
        self.alt = None
        self.az = None
        self.nadirAng = None
        self.length = None

    def __str__(self) -> str:
        """Defines GroundPosition information string."""
        title = 'Celest.GoundPosition Object\n'
        name = f'Name: {self.name}\t'
        coor = f'Coordinates: {self.coor}\t'
        radius = f'Radius: {self.radius}'

        return title + name + coor + radius

    def getRadius(self, obsCoor: Tuple[float, float]) -> float:
        """Instantiates radius attribute.

        This method uses the World Geodetic System, WGS84, to calculate the
        Earth's radius at the given coordinates.

        Parameters
        ----------
        obsCoor : tuple
            Geodetic coordinates for the ground position location given in
            decimal degrees in the (latitude, longitude) format.

        Returns
        -------
        float
            The Earths radius at obsCoor given in km.

        Notes
        -----
        The Earth can be modeled as an ellipsoid given by the following
        equation:

        .. math:: r = \sqrt{\frac{(6378.14)^2(6356.75)^2}{(6378.14)^2
                            \sin{\phi}^2+(6356.75)^2\cos{\phi}^2}}

        where :math:`\phi` is the observers lattitude.
        """
        phi = radians(obsCoor[0])

        # Define WGS84 Parameters.
        semiMajor = 6378.137**2
        semiMinor = 6356.752314245**2

        numerator = semiMajor * semiMinor
        denominator = semiMajor * sin(phi)**2 + semiMinor * cos(phi)**2

        return sqrt(numerator / denominator)

    def getECEF(self, obsCoor: Tuple[float, float], radius: float) -> np.ndarray:
        """Instantiates ECEFpos attribute.

        Converts the ground positions geographical coordinates and radius into
        the ECEF cartesian reference frame.

        Parameters
        ----------
        coor : tuple
            Geodetic coordinates for the ground position location given in
            decimal degrees in the (latitude, longitude) format.
        radius : float
            Radius of earths surface at the given coordinates using WGS84.

        Returns
        -------
        np.ndarray
            Array of shape (3,) representing the GroundPosition location in the
            ECEF cartesian frame.
        """
        if obsCoor[1] < 0:
            theta = radians(360 + obsCoor[1])
        else:
            theta = radians(obsCoor[1])
        phi = np.radians(90 - obsCoor[0])
        x = radius*cos(theta)*sin(phi)
        y = radius*sin(theta)*sin(phi)
        z = radius*cos(phi)
        ECEFpos = np.array([x, y, z])

        return ECEFpos
