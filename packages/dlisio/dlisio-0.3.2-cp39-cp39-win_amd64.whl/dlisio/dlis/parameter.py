import logging
import numpy as np
from collections import OrderedDict

from .basicobject import BasicObject
from . import utils


class Parameter(BasicObject):
    """Parameter

    A parameter object describes a parameter used in the acquisition and
    processing of data.  The parameter value(s) may be scalars or an array. In
    the later case, the structure of the array is defined in the dimension
    attribute. The zones attribute specifies which zones the parameter is
    defined. If there are no zones the parameter is defined everywhere.

    The axis attribute, if present, defines axis labels for multidimensional
    value(s).

    Attributes
    ----------

    long_name : Longname
        Descriptive name of the channel.

    dimension : list(int)
        Dimensions of the parameter values

    axis : list(Axis)
        Coordinate axes of the parameter values

    zones : list(Zone)
        Mutually disjoint intervals where the parameter values is constant

    See also
    --------

    BasicObject : The basic object that Parameter is derived from

    Notes
    -----

    The Parameter object reflects the logical record type PARAMETER, described
    in rp66. PARAMETER objects are defined in Appendix A.2 - Logical Record
    Types, described in detail in Chapter 5.8.2 - Static and Frame Data,
    PARAMETER objects.
    """
    attributes = {
        'LONG-NAME' : utils.scalar,
        'DIMENSION' : utils.reverse,
        'AXIS'      : utils.reverse,
        'ZONES'     : utils.vector,
        'VALUES'    : utils.vector,
    }

    linkage = {
        'LONG-NAME' : utils.obname('LONG-NAME'),
        'AXIS'      : utils.obname('AXIS'),
        'ZONES'     : utils.obname('ZONE')
    }

    def __init__(self, attic, lf):
        super().__init__(attic, lf=lf)

    @property
    def long_name(self):
        return self['LONG-NAME']

    @property
    def dimension(self):
        return self['DIMENSION']

    @property
    def axis(self):
        return self['AXIS']

    @property
    def zones(self):
        return self['ZONES']

    @property
    def values(self):
        """ Parameter values

        Parameter value(s) may be scalar or array's. The size/dimensionallity
        of each value is defined in the dimensions attribute.

        Each value may or may not be zoned, i.e. it is only defined in a
        certain zone. If this is the case the first zone, parameter.zones[0],
        will correspond to the first value, parameter.values[0] and so on.  If
        there is no zones, there should only be one value, which is said to be
        unzoned, i.e. it is defined everywere.

        Raises
        ------

        ValueError
            Unable to structure the values based on the information available.

        Returns
        -------

        values : structured np.ndarray

        Notes
        -----

        If dlisio is unable to structure the values due to insufficient or
        contradictory information in the object, an ValueError is raised.  The
        raw array can still be accessed through attic, but note that in this
        case, the semantic meaning of the array is undefined.

        Examples
        --------

        First value:

        >>> parameter.values[0]
        [10, 20, 30]

        Zone (if any) where that parameter value is valid:

        >>> parameter.zones[0]
        Zone('ZONE-A')
        """
        try:
            values = self.attic['VALUES'].value
        except KeyError:
            return np.empty(0)

        shape = utils.validshape(values, self.dimension, samplecount=len(self.zones))
        return utils.sampling(values, shape)

    def describe_attr(self, buf, width, indent, exclude):
        utils.describe_description(buf, self.long_name, width, indent, exclude)

        d = OrderedDict()
        d['Sample dimensions'] = 'DIMENSION'
        d['Axis labels']       = 'AXIS'
        d['Zones']             = 'ZONES'

        utils.describe_attributes(buf, d, self, width, indent, exclude)

        utils.describe_sampled_attrs(
            buf,
            self.attic,
            self.dimension,
            'VALUES',
            None,
            width,
            indent,
            exclude
        )
