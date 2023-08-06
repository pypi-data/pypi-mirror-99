#############################################################################
#  Copyright Kitware Inc.
#
#  Licensed under the Apache License, Version 2.0 ( the "License" );
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#############################################################################

import math
import numpy
import palettable
import PIL.Image
import pyproj
import struct
import threading
from operator import attrgetter
from osgeo import gdal
from osgeo import gdal_array
from osgeo import gdalconst
from osgeo import osr
from pkg_resources import DistributionNotFound, get_distribution

from large_image import config
from large_image.cache_util import LruCacheMetaclass, methodcache, CacheProperties
from large_image.constants import SourcePriority, TileInputUnits, TILE_FORMAT_NUMPY, TILE_FORMAT_PIL
from large_image.exceptions import TileSourceException
from large_image.tilesource import FileTileSource


try:
    __version__ = get_distribution(__name__).version
except DistributionNotFound:
    # package is not installed
    pass


TileInputUnits['projection'] = 'projection'
TileInputUnits['proj'] = 'projection'
TileInputUnits['wgs84'] = 'proj4:EPSG:4326'
TileInputUnits['4326'] = 'proj4:EPSG:4326'

# Inform the tile source cache about the potential size of this tile source
CacheProperties['tilesource']['itemExpectedSize'] = max(
    CacheProperties['tilesource']['itemExpectedSize'],
    100 * 1024 ** 2)

# Used to cache pixel size for projections
ProjUnitsAcrossLevel0 = {}
ProjUnitsAcrossLevel0_MaxSize = 100

InitPrefix = '+init='


class GDALFileTileSource(FileTileSource, metaclass=LruCacheMetaclass):
    """
    Provides tile access to geospatial files.
    """

    cacheName = 'tilesource'
    name = 'gdalfile'
    extensions = {
        None: SourcePriority.MEDIUM,
        # National Imagery Transmission Format
        'ntf': SourcePriority.PREFERRED,
        'nitf': SourcePriority.PREFERRED,
        'tif': SourcePriority.LOW,
        'tiff': SourcePriority.LOW,
        'vrt': SourcePriority.PREFERRED,
    }
    mimeTypes = {
        None: SourcePriority.FALLBACK,
        'image/geotiff': SourcePriority.PREFERRED,
        'image/tiff': SourcePriority.LOW,
        'image/x-tiff': SourcePriority.LOW,
    }
    geospatial = True

    def __init__(self, path, projection=None, unitsPerPixel=None, **kwargs):
        """
        Initialize the tile class.  See the base class for other available
        parameters.

        :param path: a filesystem path for the tile source.
        :param projection: None to use pixel space, otherwise a proj4
            projection string or a case-insensitive string of the form
            'EPSG:<epsg number>'.  If a string and case-insensitively prefixed
            with 'proj4:', that prefix is removed.  For instance,
            'proj4:EPSG:3857', 'PROJ4:+init=epsg:3857', and '+init=epsg:3857',
            and 'EPSG:3857' are all equivilant.
        :param unitsPerPixel: The size of a pixel at the 0 tile size.  Ignored
            if the projection is None.  For projections, None uses the default,
            which is the distance between (-180,0) and (180,0) in EPSG:4326
            converted to the projection divided by the tile size.  Proj4
            projections that are not latlong (is_geographic is False) must
            specify unitsPerPixel.
        """
        super().__init__(path, **kwargs)
        self._logger = config.getConfig('logger')
        self._bounds = {}
        self._path = self._getLargeImagePath()
        try:
            self.dataset = gdal.Open(self._path, gdalconst.GA_ReadOnly)
        except RuntimeError:
            raise TileSourceException('File cannot be opened via GDAL')
        self._getDatasetLock = threading.RLock()
        self.tileSize = 256
        self.tileWidth = self.tileSize
        self.tileHeight = self.tileSize
        self._projection = projection
        if projection and projection.lower().startswith('epsg:'):
            projection = InitPrefix + projection.lower()
        if projection and not isinstance(projection, bytes):
            projection = projection.encode('utf8')
        self.projection = projection
        try:
            with self._getDatasetLock:
                self.sourceSizeX = self.sizeX = self.dataset.RasterXSize
                self.sourceSizeY = self.sizeY = self.dataset.RasterYSize
        except AttributeError:
            raise TileSourceException('File cannot be opened via GDAL.')
        is_netcdf = self._checkNetCDF()
        try:
            scale = self.getPixelSizeInMeters()
        except RuntimeError:
            raise TileSourceException('File cannot be opened via GDAL.')
        if not scale and not is_netcdf:
            raise TileSourceException(
                'File does not have a projected scale, so will not be '
                'opened via GDAL.')
        self.sourceLevels = self.levels = int(max(0, math.ceil(max(
            math.log(float(self.sizeX) / self.tileWidth),
            math.log(float(self.sizeY) / self.tileHeight)) / math.log(2))) + 1)
        self._unitsPerPixel = unitsPerPixel
        if self.projection:
            self._initWithProjection(unitsPerPixel)
        self._getTileLock = threading.Lock()
        self._setDefaultStyle()

    def _checkNetCDF(self):
        return False

    def _styleBands(self):
        interpColorTable = {
            'red': ['#000000', '#ff0000'],
            'green': ['#000000', '#00ff00'],
            'blue': ['#000000', '#0000ff'],
            'gray': ['#000000', '#ffffff'],
            'alpha': ['#ffffff00', '#ffffffff'],
        }
        style = []
        if hasattr(self, 'style'):
            styleBands = self.style['bands'] if 'bands' in self.style else [self.style]
            for styleBand in styleBands:

                styleBand = styleBand.copy()
                # Default to band 1 -- perhaps we should default to gray or
                # green instead.
                styleBand['band'] = self._bandNumber(styleBand.get('band', 1))
                style.append(styleBand)
        if not len(style):
            for interp in ('red', 'green', 'blue', 'gray', 'palette', 'alpha'):
                band = self._bandNumber(interp, False)
                # If we don't have the requested band, or we only have alpha,
                # or this is gray or palette and we already added another band,
                # skip this interpretation.
                if (band is None or
                        (interp == 'alpha' and not len(style)) or
                        (interp in ('gray', 'palette') and len(style))):
                    continue
                if interp == 'palette':
                    bandInfo = self.getOneBandInformation(band)
                    style.append({
                        'band': band,
                        'palette': 'colortable',
                        'min': 0,
                        'max': len(bandInfo['colortable']) - 1})
                else:
                    style.append({
                        'band': band,
                        'palette': interpColorTable[interp],
                        'min': 'auto',
                        'max': 'auto',
                        'nodata': 'auto',
                        'composite': 'multiply' if interp == 'alpha' else 'lighten'
                    })
        return style

    def _setDefaultStyle(self):
        """If not style was specified, create a default style."""
        if hasattr(self, 'style'):
            styleBands = self.style['bands'] if 'bands' in self.style else [self.style]
            if not len(styleBands) or (len(styleBands) == 1 and isinstance(
                    styleBands[0].get('band', 1), int) and styleBands[0].get('band', 1) <= 0):
                del self.style
        style = self._styleBands()
        if len(style):
            hasAlpha = False
            for bstyle in style:
                hasAlpha = hasAlpha or self.getOneBandInformation(
                    bstyle.get('band', 0)).get('iterpretation') == 'alpha'
                if 'palette' in bstyle:
                    if bstyle['palette'] == 'colortable':
                        bandInfo = self.getOneBandInformation(bstyle.get('band', 0))
                        bstyle['palette'] = [(
                            '#%02X%02X%02X' if len(entry) == 3 else
                            '#%02X%02X%02X%02X') % entry for entry in bandInfo['colortable']]
                    if not isinstance(bstyle['palette'], list):
                        bstyle['palette'] = self.getHexColors(bstyle['palette'])
                if bstyle.get('nodata') == 'auto':
                    bandInfo = self.getOneBandInformation(bstyle.get('band', 0))
                    bstyle['nodata'] = bandInfo.get('nodata', None)
            if not hasAlpha and self.projection:
                style.append({
                    'band': len(self.getBandInformation()) + 1,
                    'min': 0,
                    'max': 'auto',
                    'composite': 'multiply',
                    'palette': ['#ffffff00', '#ffffffff'],
                })
            self._logger.debug('Using style %r', style)
            self.style = {'bands': style}
        self._bandNames = {}
        for idx, band in self.getBandInformation().items():
            if band.get('interpretation'):
                self._bandNames[band['interpretation'].lower()] = idx

    def _scanForMinMax(self, dtype, frame=None, analysisSize=1024):
        frame = frame or 0
        bandInfo = self.getBandInformation()
        if (not frame and all(
                band.get('min') is not None and band.get('max') is not None
                for band in bandInfo.values())):
            with self._getDatasetLock:
                dtype = gdal_array.GDALTypeCodeToNumericTypeCode(
                    self.dataset.GetRasterBand(1).DataType)
            self._bandRanges[0] = {
                'min': numpy.array([band['min'] for band in bandInfo.values()], dtype=dtype),
                'max': numpy.array([band['max'] for band in bandInfo.values()], dtype=dtype),
            }
        else:
            kwargs = {}
            if self.projection:
                bounds = self.getBounds(self.projection)
                kwargs = {'region': {
                    'left': bounds['xmin'],
                    'top': bounds['ymax'],
                    'right': bounds['xmax'],
                    'bottom': bounds['ymin'],
                    'units': 'projection'
                }}
            super(GDALFileTileSource, GDALFileTileSource)._scanForMinMax(
                self, dtype=dtype, frame=frame, analysisSize=analysisSize, **kwargs)
        # Add the maximum range of the data type to the end of the band
        # range list.  This changes autoscaling behavior.  For non-integer
        # data types, this adds the range [0, 1].
        self._bandRanges[frame]['min'] = numpy.append(self._bandRanges[frame]['min'], 0)
        try:
            # only valid for integer dtypes
            range_max = numpy.iinfo(self._bandRanges[frame]['max'].dtype).max
        except ValueError:
            range_max = 1
        self._bandRanges[frame]['max'] = numpy.append(self._bandRanges[frame]['max'], range_max)

    def _getDriver(self):
        """
        Get the GDAL driver used to read this dataset.

        :returns: The name of the driver.
        """
        if not hasattr(self, '_driver'):
            with self._getDatasetLock:
                if not self.dataset or not self.dataset.GetDriver():
                    self._driver = None
                else:
                    self._driver = self.dataset.GetDriver().ShortName
        return self._driver

    def _initWithProjection(self, unitsPerPixel=None):
        """
        Initialize aspects of the class when a projection is set.
        """
        inProj = self._proj4Proj(InitPrefix + 'epsg:4326')
        # Since we already converted to bytes decoding is safe here
        outProj = self._proj4Proj(self.projection)
        if outProj.crs.is_geographic:
            raise TileSourceException(
                'Projection must not be geographic (it needs to use linear '
                'units, not longitude/latitude).')
        if unitsPerPixel:
            self.unitsAcrossLevel0 = float(unitsPerPixel) * self.tileSize
        else:
            self.unitsAcrossLevel0 = ProjUnitsAcrossLevel0.get(self.projection)
            if self.unitsAcrossLevel0 is None:
                # If unitsPerPixel is not specified, the horizontal distance
                # between -180,0 and +180,0 is used.  Some projections (such as
                # stereographic) will fail in this case; they must have a
                # unitsPerPixel specified.
                equator = pyproj.Transformer.from_proj(inProj, outProj, always_xy=True).transform(
                    [-180, 180], [0, 0])
                self.unitsAcrossLevel0 = abs(equator[0][1] - equator[0][0])
                if not self.unitsAcrossLevel0:
                    raise TileSourceException(
                        'unitsPerPixel must be specified for this projection')
                if len(ProjUnitsAcrossLevel0) >= ProjUnitsAcrossLevel0_MaxSize:
                    ProjUnitsAcrossLevel0.clear()
                ProjUnitsAcrossLevel0[self.projection] = self.unitsAcrossLevel0
        # This was
        #   self.projectionOrigin = pyproj.transform(inProj, outProj, 0, 0)
        # but for consistency, it should probably always be (0, 0).  Whatever
        # renders the map would need the same offset as used here.
        self.projectionOrigin = (0, 0)
        # Calculate values for this projection
        self.levels = int(max(int(math.ceil(
            math.log(self.unitsAcrossLevel0 / self.getPixelSizeInMeters() / self.tileWidth) /
            math.log(2))) + 1, 1))
        # Report sizeX and sizeY as the whole world
        self.sizeX = 2 ** (self.levels - 1) * self.tileWidth
        self.sizeY = 2 ** (self.levels - 1) * self.tileHeight

    @staticmethod
    def getLRUHash(*args, **kwargs):
        return super(GDALFileTileSource, GDALFileTileSource).getLRUHash(
            *args, **kwargs) + ',%s,%s' % (
                kwargs.get('projection', args[1] if len(args) >= 2 else None),
                kwargs.get('unitsPerPixel', args[3] if len(args) >= 4 else None))

    def getState(self):
        return super().getState() + ',%s,%s' % (
            self._projection, self._unitsPerPixel)

    @staticmethod
    def getHexColors(palette):
        """
        Returns list of hex colors for a given color palette

        :returns: List of colors
        """
        try:
            return attrgetter(palette)(palettable).hex_colors
        except AttributeError:
            raise TileSourceException('Palette is not a valid palettable path.')

    def getProj4String(self):
        """
        Returns proj4 string for the given dataset

        :returns: The proj4 string or None.
        """
        with self._getDatasetLock:
            wkt = self.dataset.GetProjection()
        if not wkt:
            if hasattr(self, '_netcdf') or self._getDriver() in {'NITF'}:
                return InitPrefix + 'epsg:4326'
            return
        proj = osr.SpatialReference()
        proj.ImportFromWkt(wkt)
        return proj.ExportToProj4()

    def getPixelSizeInMeters(self):
        """
        Get the approximate base pixel size in meters.  This is calculated as
        the average scale of the four edges in the WGS84 ellipsoid.

        :returns: the pixel size in meters or None.
        """
        bounds = self.getBounds(InitPrefix + 'epsg:4326')
        if not bounds:
            return
        geod = pyproj.Geod(ellps='WGS84')
        az12, az21, s1 = geod.inv(bounds['ul']['x'], bounds['ul']['y'],
                                  bounds['ur']['x'], bounds['ur']['y'])
        az12, az21, s2 = geod.inv(bounds['ur']['x'], bounds['ur']['y'],
                                  bounds['lr']['x'], bounds['lr']['y'])
        az12, az21, s3 = geod.inv(bounds['lr']['x'], bounds['lr']['y'],
                                  bounds['ll']['x'], bounds['ll']['y'])
        az12, az21, s4 = geod.inv(bounds['ll']['x'], bounds['ll']['y'],
                                  bounds['ul']['x'], bounds['ul']['y'])
        return (s1 + s2 + s3 + s4) / (self.sourceSizeX * 2 + self.sourceSizeY * 2)

    def getNativeMagnification(self):
        """
        Get the magnification at the base level.

        :return: width of a pixel in mm, height of a pixel in mm.
        """
        scale = self.getPixelSizeInMeters()
        return {
            'magnification': None,
            'mm_x': scale * 100 if scale else None,
            'mm_y': scale * 100 if scale else None,
        }

    def getBounds(self, srs=None):
        """
        Returns bounds of the image.

        :param srs: the projection for the bounds.  None for the default.
        :returns: an object with the four corners and the projection that was
            used.  None if we don't know the original projection.
        """
        if srs not in self._bounds:
            with self._getDatasetLock:
                gt = self.dataset.GetGeoTransform()
            nativeSrs = self.getProj4String()
            if not nativeSrs:
                self._bounds[srs] = None
                return
            bounds = {
                'll': {
                    'x': gt[0] + self.sourceSizeY * gt[2],
                    'y': gt[3] + self.sourceSizeY * gt[5]
                },
                'ul': {
                    'x': gt[0],
                    'y': gt[3],
                },
                'lr': {
                    'x': gt[0] + self.sourceSizeX * gt[1] + self.sourceSizeY * gt[2],
                    'y': gt[3] + self.sourceSizeX * gt[4] + self.sourceSizeY * gt[5]
                },
                'ur': {
                    'x': gt[0] + self.sourceSizeX * gt[1],
                    'y': gt[3] + self.sourceSizeX * gt[4]
                },
                'srs': nativeSrs,
            }
            # Make sure geographic coordinates do not exceed their limits
            if self._proj4Proj(nativeSrs).crs.is_geographic and srs:
                try:
                    self._proj4Proj(srs)(0, 90, errcheck=True)
                    yBound = 90.0
                except RuntimeError:
                    yBound = 89.999999
                for key in ('ll', 'ul', 'lr', 'ur'):
                    bounds[key]['y'] = max(min(bounds[key]['y'], yBound), -yBound)
            if srs and srs != nativeSrs:
                inProj = self._proj4Proj(nativeSrs)
                outProj = self._proj4Proj(srs)
                keys = ('ll', 'ul', 'lr', 'ur')
                pts = pyproj.Transformer.from_proj(inProj, outProj, always_xy=True).itransform([
                    (bounds[key]['x'], bounds[key]['y']) for key in keys])
                for idx, pt in enumerate(pts):
                    key = keys[idx]
                    bounds[key]['x'] = pt[0]
                    bounds[key]['y'] = pt[1]
                bounds['srs'] = srs.decode('utf8') if isinstance(srs, bytes) else srs
            bounds['xmin'] = min(bounds['ll']['x'], bounds['ul']['x'],
                                 bounds['lr']['x'], bounds['ur']['x'])
            bounds['xmax'] = max(bounds['ll']['x'], bounds['ul']['x'],
                                 bounds['lr']['x'], bounds['ur']['x'])
            bounds['ymin'] = min(bounds['ll']['y'], bounds['ul']['y'],
                                 bounds['lr']['y'], bounds['ur']['y'])
            bounds['ymax'] = max(bounds['ll']['y'], bounds['ul']['y'],
                                 bounds['lr']['y'], bounds['ur']['y'])
            self._bounds[srs] = bounds
        return self._bounds[srs]

    def getBandInformation(self, dataset=None):
        if not getattr(self, '_bandInfo', None) or dataset:
            with self._getDatasetLock:
                cache = not dataset
                if not dataset:
                    dataset = self.dataset
                infoSet = {}
                for i in range(dataset.RasterCount):
                    band = dataset.GetRasterBand(i + 1)
                    info = {}
                    try:
                        stats = band.GetStatistics(True, True)
                        # The statistics provide a min and max, so we don't
                        # fetch those separately
                        info.update(dict(zip(('min', 'max', 'mean', 'stdev'), stats)))
                    except RuntimeError:
                        self._logger.info('Failed to get statistics for band %d', i + 1)
                    info['nodata'] = band.GetNoDataValue()
                    info['scale'] = band.GetScale()
                    info['offset'] = band.GetOffset()
                    info['units'] = band.GetUnitType()
                    info['categories'] = band.GetCategoryNames()
                    interp = band.GetColorInterpretation()
                    info['interpretation'] = {
                        gdalconst.GCI_GrayIndex: 'gray',
                        gdalconst.GCI_PaletteIndex: 'palette',
                        gdalconst.GCI_RedBand: 'red',
                        gdalconst.GCI_GreenBand: 'green',
                        gdalconst.GCI_BlueBand: 'blue',
                        gdalconst.GCI_AlphaBand: 'alpha',
                        gdalconst.GCI_HueBand: 'hue',
                        gdalconst.GCI_SaturationBand: 'saturation',
                        gdalconst.GCI_LightnessBand: 'lightness',
                        gdalconst.GCI_CyanBand: 'cyan',
                        gdalconst.GCI_MagentaBand: 'magenta',
                        gdalconst.GCI_YellowBand: 'yellow',
                        gdalconst.GCI_BlackBand: 'black',
                        gdalconst.GCI_YCbCr_YBand: 'Y',
                        gdalconst.GCI_YCbCr_CbBand: 'Cb',
                        gdalconst.GCI_YCbCr_CrBand: 'Cr',
                    }.get(interp, interp)
                    if band.GetColorTable():
                        info['colortable'] = [band.GetColorTable().GetColorEntry(pos)
                                              for pos in range(band.GetColorTable().GetCount())]
                    if band.GetMaskBand():
                        info['maskband'] = band.GetMaskBand().GetBand() or None
                    # Only keep values that aren't None or the empty string
                    infoSet[i + 1] = {k: v for k, v in info.items() if v not in (None, '')}
            if not cache:
                return infoSet
            self._bandInfo = infoSet
        return self._bandInfo

    def getOneBandInformation(self, band):
        return self.getBandInformation()[band]

    def getMetadata(self):
        with self._getDatasetLock:
            metadata = {
                'geospatial': bool(self.dataset.GetProjection() or hasattr(self, '_netcdf')),
                'levels': self.levels,
                'sizeX': self.sizeX,
                'sizeY': self.sizeY,
                'sourceLevels': self.sourceLevels,
                'sourceSizeX': self.sourceSizeX,
                'sourceSizeY': self.sourceSizeY,
                'tileWidth': self.tileWidth,
                'tileHeight': self.tileHeight,
                'bounds': self.getBounds(self.projection),
                'sourceBounds': self.getBounds(),
                'bands': self.getBandInformation(),
            }
        metadata.update(self.getNativeMagnification())
        if hasattr(self, '_netcdf'):
            # To ensure all band information from all subdatasets in netcdf,
            # we could do the following:
            # for key in self._netcdf['datasets']:
            #     dataset = self._netcdf['datasets'][key]
            #     if 'bands' not in dataset:
            #         gdaldataset = gdal.Open(dataset['name'], gdalconst.GA_ReadOnly)
            #         dataset['bands'] = self.getBandInformation(gdaldataset)
            #         dataset['sizeX'] = gdaldataset.RasterXSize
            #         dataset['sizeY'] = gdaldataset.RasterYSize
            metadata['netcdf'] = self._netcdf
        return metadata

    def getInternalMetadata(self, **kwargs):
        """
        Return additional known metadata about the tile source.  Data returned
        from this method is not guaranteed to be in any particular format or
        have specific values.

        :returns: a dictionary of data or None.
        """
        result = {}
        with self._getDatasetLock:
            result['driverShortName'] = self.dataset.GetDriver().ShortName
            result['driverLongName'] = self.dataset.GetDriver().LongName
            result['fileList'] = self.dataset.GetFileList()
            result['RasterXSize'] = self.dataset.RasterXSize
            result['RasterYSize'] = self.dataset.RasterYSize
            result['GeoTransform'] = self.dataset.GetGeoTransform()
            result['GCPProjection'] = self.dataset.GetGCPProjection()
            result['Metadata'] = self.dataset.GetMetadata_List()
            for key in ['IMAGE_STRUCTURE', 'SUBDATASETS', 'GEOLOCATION', 'RPC']:
                metadatalist = self.dataset.GetMetadata_List(key)
                if metadatalist:
                    result['Metadata_' + key] = metadatalist
        return result

    def getTileCorners(self, z, x, y):
        """
        Returns bounds of a tile for a given x,y,z index.

        :param z: tile level
        :param x: tile offset from left.
        :param y: tile offset from right
        :returns: (xmin, ymin, xmax, ymax) in the current projection or base
            pixels.
        """
        x, y = float(x), float(y)
        if self.projection:
            # Scale tile into the range [-0.5, 0.5], [-0.5, 0.5]
            xmin = -0.5 + x / 2.0 ** z
            xmax = -0.5 + (x + 1) / 2.0 ** z
            ymin = 0.5 - (y + 1) / 2.0 ** z
            ymax = 0.5 - y / 2.0 ** z
            # Convert to projection coordinates
            xmin = self.projectionOrigin[0] + xmin * self.unitsAcrossLevel0
            xmax = self.projectionOrigin[0] + xmax * self.unitsAcrossLevel0
            ymin = self.projectionOrigin[1] + ymin * self.unitsAcrossLevel0
            ymax = self.projectionOrigin[1] + ymax * self.unitsAcrossLevel0
        else:
            xmin = 2 ** (self.sourceLevels - 1 - z) * x * self.tileWidth
            ymin = 2 ** (self.sourceLevels - 1 - z) * y * self.tileHeight
            xmax = xmin + 2 ** (self.sourceLevels - 1 - z) * self.tileWidth
            ymax = ymin + 2 ** (self.sourceLevels - 1 - z) * self.tileHeight
            ymin, ymax = self.sourceSizeY - ymax, self.sourceSizeY - ymin
        return xmin, ymin, xmax, ymax

    def _bandNumber(self, band, exc=True):
        """
        Given a band number or interpretation name, return a validated band
        number.

        :param band: either -1, a positive integer, or the name of a band
            interpretation that is present in the tile source.
        :param exc: if True, raise an exception if no band matches.
        :returns: a validated band, either 1 or a positive integer, or None if
            no matching band and exceptions are not enabled.
        """
        if hasattr(self, '_netcdf') and (':' in str(band) or str(band).isdigit()):
            key = None
            if ':' in str(band):
                key, band = band.split(':', 1)
            if str(band).isdigit():
                band = int(band)
            else:
                band = 1
            if not key or key == 'default':
                key = self._netcdf.get('default', None)
                if key is None:
                    return band
            if key in self._netcdf['datasets']:
                return (key, band)
        bands = self.getBandInformation()
        if not isinstance(band, int):
            try:
                band = next(bandIdx for bandIdx in sorted(bands)
                            if band == bands[bandIdx]['interpretation'])
            except StopIteration:
                pass
        if hasattr(band, 'isdigit') and band.isdigit():
            band = int(band)
        if band != -1 and band not in bands:
            if exc:
                raise TileSourceException(
                    'Band has to be a positive integer, -1, or a band '
                    'interpretation found in the source.')
            return None
        return int(band)

    @methodcache()
    def getTile(self, x, y, z, pilImageAllowed=False, numpyAllowed=False, **kwargs):
        if not self.projection:
            self._xyzInRange(x, y, z)
            factor = int(2 ** (self.levels - 1 - z))
            x0 = int(x * factor * self.tileWidth)
            y0 = int(y * factor * self.tileHeight)
            x1 = int(min(x0 + factor * self.tileWidth, self.sourceSizeX))
            y1 = int(min(y0 + factor * self.tileHeight, self.sourceSizeY))
            w = int(max(1, round((x1 - x0) / factor)))
            h = int(max(1, round((y1 - y0) / factor)))
            with self._getDatasetLock:
                tile = self.dataset.ReadAsArray(
                    xoff=x0, yoff=y0, xsize=x1 - x0, ysize=y1 - y0, buf_xsize=w, buf_ysize=h)
        else:
            xmin, ymin, xmax, ymax = self.getTileCorners(z, x, y)
            bounds = self.getBounds(self.projection)
            if (xmin >= bounds['xmax'] or xmax <= bounds['xmin'] or
                    ymin >= bounds['ymax'] or ymax <= bounds['ymin']):
                pilimg = PIL.Image.new('RGBA', (self.tileWidth, self.tileHeight))
                return self._outputTile(
                    pilimg, TILE_FORMAT_PIL, x, y, z, applyStyle=False, **kwargs)
            res = (self.unitsAcrossLevel0 / self.tileSize) * (2 ** -z)
            if not hasattr(self, '_warpSRS'):
                self._warpSRS = (self.getProj4String(),
                                 self.projection.decode('utf8'))
                if self._warpSRS[1].startswith(InitPrefix) and tuple(
                        int(p) for p in gdal.__version__.split('.')[:2]) >= (3, 1):
                    self._warpSRS = (self._warpSRS[0], self._warpSRS[1][len(InitPrefix):])
            with self._getDatasetLock:
                ds = gdal.Warp(
                    '', self.dataset, format='VRT',
                    srcSRS=self._warpSRS[0], dstSRS=self._warpSRS[1],
                    dstAlpha=True,
                    # Valid options are GRA_NearestNeighbour, GRA_Bilinear,
                    # GRA_Cubic, GRA_CubicSpline, GRA_Lanczos, GRA_Med,
                    # GRA_Mode, perhaps others; because we have some indexed
                    # datasets, generically, this should probably either be
                    # GRA_NearestNeighbour or GRA_Mode.
                    resampleAlg=gdal.GRA_NearestNeighbour,
                    multithread=True,
                    # We might get a speed-up with acceptable distortion if we
                    # set the polynomicalOrder or ask for an optimal transform
                    # around the outputBounds.
                    polynomialOrder=1,
                    xRes=res, yRes=res, outputBounds=[xmin, ymin, xmax, ymax])
                tile = ds.ReadAsArray()
        if len(tile.shape) == 3:
            tile = numpy.rollaxis(tile, 0, 3)
        return self._outputTile(tile, TILE_FORMAT_NUMPY, x, y, z,
                                pilImageAllowed, numpyAllowed, **kwargs)

    @staticmethod
    def _proj4Proj(proj):
        """
        Return a pyproj.Proj based on either a binary or unicode string.

        :param proj: a binary or unicode projection string.
        :returns: a proj4 projection object.  None if the specified projection
            cannot be created.
        """
        if isinstance(proj, bytes):
            proj = proj.decode('utf8')
        if not isinstance(proj, str):
            return
        if proj.lower().startswith('proj4:'):
            proj = proj.split(':', 1)[1]
        if proj.lower().startswith('epsg:'):
            proj = InitPrefix + proj.lower()
        try:
            if proj.startswith(InitPrefix) and int(pyproj.proj_version_str.split('.')[0]) >= 6:
                proj = proj[len(InitPrefix):]
        except Exception:
            pass  # failed to parse version
        return pyproj.Proj(proj)

    def _convertProjectionUnits(self, left, top, right, bottom, width, height,
                                units, **kwargs):
        """
        Given bound information and a units string that consists of a proj4
        projection (starts with `'proj4:'`, `'epsg:'`, `'+proj='` or is an
        enumerated value like `'wgs84'`), convert the bounds to either pixel or
        the class projection coordinates.

        :param left: the left edge (inclusive) of the region to process.
        :param top: the top edge (inclusive) of the region to process.
        :param right: the right edge (exclusive) of the region to process.
        :param bottom: the bottom edge (exclusive) of the region to process.
        :param width: the width of the region to process.  Ignored if both
            left and right are specified.
        :param height: the height of the region to process.  Ignores if both
            top and bottom are specified.
        :param units: either 'projection', a string starting with 'proj4:',
            'epsg:', or '+proj=' or a enumerated value like 'wgs84', or one of
            the super's values.
        :param **kwargs: optional parameters.
        :returns: left, top, right, bottom, units.  The new bounds in the
            either pixel or class projection units.
        """
        if not kwargs.get('unitsWH') or kwargs.get('unitsWH') == units:
            if left is None and right is not None and width is not None:
                left = right - width
            if right is None and left is not None and width is not None:
                right = left + width
            if top is None and bottom is not None and height is not None:
                top = bottom - height
            if bottom is None and top is not None and height is not None:
                bottom = top + height
        if (left is None and right is None) or (top is None and bottom is None):
            raise TileSourceException(
                'Cannot convert from projection unless at least one of '
                'left and right and at least one of top and bottom is '
                'specified.')
        if not self.projection:
            pleft, ptop = self.toNativePixelCoordinates(
                right if left is None else left,
                bottom if top is None else top,
                units)
            pright, pbottom = self.toNativePixelCoordinates(
                left if right is None else right,
                top if bottom is None else bottom,
                units)
            units = 'base_pixels'
        else:
            inProj = self._proj4Proj(units)
            outProj = self._proj4Proj(self.projection)
            transformer = pyproj.Transformer.from_proj(inProj, outProj, always_xy=True)
            pleft, ptop = transformer.transform(
                right if left is None else left,
                bottom if top is None else top)
            pright, pbottom = transformer.transform(
                left if right is None else right,
                top if bottom is None else bottom)
            units = 'projection'
        left = pleft if left is not None else None
        top = ptop if top is not None else None
        right = pright if right is not None else None
        bottom = pbottom if bottom is not None else None
        return left, top, right, bottom, units

    def _getRegionBounds(self, metadata, left=None, top=None, right=None,
                         bottom=None, width=None, height=None, units=None,
                         **kwargs):
        """
        Given a set of arguments that can include left, right, top, bottom,
        width, height, and units, generate actual pixel values for left, top,
        right, and bottom.  If units is `'projection'`, use the source's
        projection.  If units starts with `'proj4:'` or `'epsg:'` or a
        custom units value, use that projection.  Otherwise, just use the super
        function.

        :param metadata: the metadata associated with this source.
        :param left: the left edge (inclusive) of the region to process.
        :param top: the top edge (inclusive) of the region to process.
        :param right: the right edge (exclusive) of the region to process.
        :param bottom: the bottom edge (exclusive) of the region to process.
        :param width: the width of the region to process.  Ignored if both
            left and right are specified.
        :param height: the height of the region to process.  Ignores if both
            top and bottom are specified.
        :param units: either 'projection', a string starting with 'proj4:',
            'epsg:' or a enumarted value like 'wgs84', or one of the super's
            values.
        :param **kwargs: optional parameters.  See above.
        :returns: left, top, right, bottom bounds in pixels.
        """
        units = TileInputUnits.get(units.lower() if units else units, units)
        # If a proj4 projection is specified, convert the left, right, top, and
        # bottom to the current projection or to pixel space if no projection
        # is used.
        if (units and (units.lower().startswith('proj4:') or
                       units.lower().startswith('epsg:') or
                       units.lower().startswith('+proj='))):
            left, top, right, bottom, units = self._convertProjectionUnits(
                left, top, right, bottom, width, height, units, **kwargs)

        if units == 'projection' and self.projection:
            bounds = self.getBounds(self.projection)
            # Fill in missing values
            if left is None:
                left = bounds['xmin'] if right is None or width is None else right - width
            if right is None:
                right = bounds['xmax'] if width is None else left + width
            if top is None:
                top = bounds['ymax'] if bottom is None or width is None else bottom - width
            if bottom is None:
                bottom = bounds['ymin'] if width is None else top + width
            if not kwargs.get('unitsWH') or kwargs.get('unitsWH') == units:
                width = height = None
            # Convert to [-0.5, 0.5], [-0.5, 0.5] coordinate range
            left = (left - self.projectionOrigin[0]) / self.unitsAcrossLevel0
            right = (right - self.projectionOrigin[0]) / self.unitsAcrossLevel0
            top = (top - self.projectionOrigin[1]) / self.unitsAcrossLevel0
            bottom = (bottom - self.projectionOrigin[1]) / self.unitsAcrossLevel0
            # Convert to world=wide 'base pixels' and crop to the world
            xScale = 2 ** (self.levels - 1) * self.tileWidth
            yScale = 2 ** (self.levels - 1) * self.tileHeight
            left = max(0, min(xScale, (0.5 + left) * xScale))
            right = max(0, min(xScale, (0.5 + right) * xScale))
            top = max(0, min(yScale, (0.5 - top) * yScale))
            bottom = max(0, min(yScale, (0.5 - bottom) * yScale))
            # Ensure correct ordering
            left, right = min(left, right), max(left, right)
            top, bottom = min(top, bottom), max(top, bottom)
            units = 'base_pixels'
        return super()._getRegionBounds(
            metadata, left, top, right, bottom, width, height, units, **kwargs)

    @methodcache()
    def getThumbnail(self, width=None, height=None, levelZero=False, **kwargs):
        """
        Get a basic thumbnail from the current tile source.  Aspect ratio is
        preserved.  If neither width nor height is given, a default value is
        used.  If both are given, the thumbnail will be no larger than either
        size.

        :param width: maximum width in pixels.
        :param height: maximum height in pixels.
        :param levelZero: if true, always use the level zero tile.  Otherwise,
            the thumbnail is generated so that it is never upsampled.
        :param **kwargs: optional arguments.  Some options are encoding,
            jpegQuality, jpegSubsampling, and tiffCompression.
        :returns: thumbData, thumbMime: the image data and the mime type.
        """
        if self.projection:
            if ((width is not None and width < 2) or
                    (height is not None and height < 2)):
                raise ValueError('Invalid width or height.  Minimum value is 2.')
            if width is None and height is None:
                width = height = 256
            params = dict(kwargs)
            params['output'] = {'maxWidth': width, 'maxHeight': height}
            params['region'] = {'units': 'projection'}
            return self.getRegion(**params)
        return super().getThumbnail(width, height, levelZero, **kwargs)

    def toNativePixelCoordinates(self, x, y, proj=None, roundResults=True):
        """
        Convert a coordinate in the native projection (self.getProj4String) to
        pixel coordinates.

        :param x: the x coordinate it the native projection.
        :param y: the y coordinate it the native projection.
        :param proj: input projection.  None to use the sources's projection.
        :param roundResults: if True, round the results to the nearest pixel.
        :return: (x, y) the pixel coordinate.
        """
        if proj is None:
            proj = self.projection
        # convert to the native projection
        inProj = self._proj4Proj(proj)
        outProj = self._proj4Proj(self.getProj4String())
        px, py = pyproj.Transformer.from_proj(inProj, outProj, always_xy=True).transform(x, y)
        # convert to native pixel coordinates
        with self._getDatasetLock:
            gt = self.dataset.GetGeoTransform()
        d = gt[2] * gt[4] - gt[1] * gt[5]
        x = (gt[0] * gt[5] - gt[2] * gt[3] - gt[5] * px + gt[2] * py) / d
        y = (gt[1] * gt[3] - gt[0] * gt[4] + gt[4] * px - gt[1] * py) / d
        if roundResults:
            x = int(round(x))
            y = int(round(y))
        return x, y

    def getPixel(self, **kwargs):
        """
        Get a single pixel from the current tile source.
        :param **kwargs: optional arguments.  Some options are region, output,
            encoding, jpegQuality, jpegSubsampling, tiffCompression, fill.  See
            tileIterator.
        :returns: a dictionary with the value of the pixel for each channel on
            a scale of [0-255], including alpha, if available.  This may
            contain additional information.
        """
        # TODO: netCDF - currently this will read the values from the
        # default subdatatset; we may want it to read values from all
        # subdatasets and the main raster bands (if they exist), and label the
        # bands better
        pixel = super().getPixel(includeTileRecord=True, **kwargs)
        tile = pixel.pop('tile', None)
        if tile:
            # Coordinates in the max level tile
            x, y = tile['gx'], tile['gy']
            if self.projection:
                # convert to a scale of [-0.5, 0.5]
                x = 0.5 + x / 2 ** (self.levels - 1) / self.tileWidth
                y = 0.5 - y / 2 ** (self.levels - 1) / self.tileHeight
                # convert to projection coordinates
                x = self.projectionOrigin[0] + x * self.unitsAcrossLevel0
                y = self.projectionOrigin[1] + y * self.unitsAcrossLevel0
                # convert to native pixel coordinates
                x, y = self.toNativePixelCoordinates(x, y)
            if 0 <= int(x) < self.sizeX and 0 <= int(y) < self.sizeY:
                with self._getDatasetLock:
                    for i in range(self.dataset.RasterCount):
                        band = self.dataset.GetRasterBand(i + 1)
                        try:
                            value = band.ReadRaster(int(x), int(y), 1, 1, buf_type=gdal.GDT_Float32)
                            if value:
                                pixel.setdefault('bands', {})[i + 1] = struct.unpack('f', value)[0]
                        except RuntimeError:
                            pass
        return pixel


def open(*args, **kwargs):
    """
    Create an instance of the module class.
    """
    return GDALFileTileSource(*args, **kwargs)


def canRead(*args, **kwargs):
    """
    Check if an input can be read by the module class.
    """
    return GDALFileTileSource.canRead(*args, **kwargs)
