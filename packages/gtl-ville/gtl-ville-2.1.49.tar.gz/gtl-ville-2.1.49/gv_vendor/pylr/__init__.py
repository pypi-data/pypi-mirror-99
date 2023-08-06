# -*- coding: utf-8 -*-
'''
Created on 4 déc. 2013

.. moduleauthor:: David Marteau <david.marteau@mappy.com>

OpenLR decoder

'''

from gv_vendor.pylr.version import __version_info__, __version_info__

from gv_vendor.pylr.parser import (BinaryParseError,
                                   BinaryVersionError,
                                   InvalidDataSizeError,
                                   init_binary_parsing,
                                   parse_binary,
                                   LocationType,
                                   LineLocation,
                                   GeoCoordinateLocation,
                                   BBox,
                                   CircleLocation,
                                   RectangleLocation,
                                   GridLocation,
                                   PolygonLocation,
                                   PoiWithAccessPointLocation,
                                   ClosedLineLocation,
                                   PointAlongLineLocation,
                                   GeoCoordinateLocation,
                                   PoiWithAccessPointLocation,
                                   RectangleLocation,
                                   BBox)

from gv_vendor.pylr.binary import (Coords,
                                   LocationReferencePoint)

from gv_vendor.pylr.constants import (LocationType,
                                      LENGTH_INTERVAL,
                                      BEARING_SECTOR,
                                      RELATIVE_OFFSET_LENGTH,
                                      RIGTH_SIDE,
                                      LEFT_SIDE,
                                      BOTH_SIDE,
                                      NO_ORIENTATION_OR_UNKNOWN,
                                      WITH_LINE_DIRECTION,
                                      AGAINST_LINE_DIRECTION,
                                      BOTH_DIRECTIONS,
                                      ON_ROAD_OR_UNKNOWN)



from gv_vendor.pylr import fow


from gv_vendor.pylr.decoder import (DecoderError,
                                    DecoderInvalidLocation,
                                    RouteSearchException,
                                    RouteNotFoundException,
                                    RouteConstructionFailed,
                                    MapDatabase,
                                    DecoderBase,
                                    RatingCalculator,
                                    ClassicDecoder)

Decoder = ClassicDecoder
