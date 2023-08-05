##############################################################################
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
##############################################################################

import builtins
import glymur
import io
import math
import multiprocessing
import PIL.Image
import queue
import warnings

from xml.etree import ElementTree

from pkg_resources import DistributionNotFound, get_distribution

from large_image.cache_util import LruCacheMetaclass, methodcache
from large_image.constants import SourcePriority, TILE_FORMAT_NUMPY
from large_image.exceptions import TileSourceException
from large_image.tilesource import FileTileSource, etreeToDict


try:
    __version__ = get_distribution(__name__).version
except DistributionNotFound:
    # package is not installed
    pass


warnings.filterwarnings('ignore', category=UserWarning, module='glymur')


class OpenjpegFileTileSource(FileTileSource, metaclass=LruCacheMetaclass):
    """
    Provides tile access to jp2 files and other files the openjpeg library can
    read.
    """

    cacheName = 'tilesource'
    name = 'openjpegfile'
    extensions = {
        None: SourcePriority.MEDIUM,
        'jp2': SourcePriority.PREFERRED,
        'jpf': SourcePriority.PREFERRED,
        'j2k': SourcePriority.PREFERRED,
        'jpx': SourcePriority.PREFERRED,
    }
    mimeTypes = {
        None: SourcePriority.FALLBACK,
        'image/jp2': SourcePriority.PREFERRED,
        'image/jpx': SourcePriority.PREFERRED,
    }

    _boxToTag = {
        # In the few samples I've seen, both of these appear to be macro images
        b'mig ': 'macro',
        b'mag ': 'label',
        # This contains a largish image
        # b'psi ': 'other',
    }
    _xmlTag = b'mxl '

    _minTileSize = 256
    _maxTileSize = 512
    _maxOpenHandles = 6

    def __init__(self, path, **kwargs):
        """
        Initialize the tile class.  See the base class for other available
        parameters.

        :param path: a filesystem path for the tile source.
        """
        super().__init__(path, **kwargs)

        largeImagePath = self._getLargeImagePath()

        self._largeImagePath = largeImagePath
        self._pixelInfo = {}
        try:
            self._openjpeg = glymur.Jp2k(largeImagePath)
        except glymur.jp2box.InvalidJp2kError:
            raise TileSourceException('File cannot be opened via Glymur and OpenJPEG.')
        glymur.set_option('lib.num_threads', multiprocessing.cpu_count())
        self._openjpegHandles = queue.LifoQueue()
        for _ in range(self._maxOpenHandles - 1):
            self._openjpegHandles.put(None)
        self._openjpegHandles.put(self._openjpeg)
        try:
            self.sizeY, self.sizeX = self._openjpeg.shape[:2]
        except IndexError:
            raise TileSourceException('File cannot be opened via Glymur and OpenJPEG.')
        self.levels = int(self._openjpeg.codestream.segment[2].num_res) + 1
        self._minlevel = 0
        self.tileWidth = self.tileHeight = 2 ** int(math.ceil(max(
            math.log(float(self.sizeX)) / math.log(2) - self.levels + 1,
            math.log(float(self.sizeY)) / math.log(2) - self.levels + 1)))
        # Small and large tiles are both inefficient.  Large tiles don't work
        # with some viewers (leaflet and Slide Atlas, for instance)
        if self.tileWidth < self._minTileSize or self.tileWidth > self._maxTileSize:
            self.tileWidth = self.tileHeight = min(
                self._maxTileSize, max(self._minTileSize, self.tileWidth))
            self.levels = int(math.ceil(math.log(float(max(
                self.sizeX, self.sizeY)) / self.tileWidth) / math.log(2))) + 1
            self._minlevel = self.levels - self._openjpeg.codestream.segment[2].num_res - 1
        self._getAssociatedImages()

    def _getAssociatedImages(self):
        """
        Read associated images and metadata from boxes.
        """
        self._associatedImages = {}
        for box in self._openjpeg.box:
            box_id = box.box_id
            if box_id == 'xxxx':
                box_id = getattr(box, 'claimed_box_id', box.box_id)
            if box_id == self._xmlTag or box_id in self._boxToTag:
                data = self._readbox(box)
                if data is None:
                    continue
                if box_id == self._xmlTag:
                    self._parseMetadataXml(data)
                    continue
                try:
                    self._associatedImages[self._boxToTag[box_id]] = PIL.Image.open(
                        io.BytesIO(data))
                except Exception:
                    pass
            if box_id == 'jp2c':
                for segment in box.codestream.segment:
                    if segment.marker_id == 'CME' and hasattr(segment, 'ccme'):
                        self._parseMetadataXml(segment.ccme)

    def getNativeMagnification(self):
        """
        Get the magnification at a particular level.

        :return: magnification, width of a pixel in mm, height of a pixel in mm.
        """
        mm_x = self._pixelInfo.get('mm_x')
        mm_y = self._pixelInfo.get('mm_y')
        # Estimate the magnification if we don't have a direct value
        mag = self._pixelInfo.get('magnification') or 0.01 / mm_x if mm_x else None
        return {
            'magnification': mag,
            'mm_x': mm_x,
            'mm_y': mm_y,
        }

    def _parseMetadataXml(self, meta):
        if not isinstance(meta, str):
            meta = meta.decode('utf8', 'ignore')
        try:
            xml = ElementTree.fromstring(meta)
        except Exception:
            return
        self._description_record = etreeToDict(xml)
        xml = self._description_record
        try:
            # Optrascan metadata
            scanDetails = xml.get('ScanInfo', xml.get('EncodeInfo'))['ScanDetails']
            mag = float(scanDetails['Magnification'])
            # In microns; convert to mm
            scale = float(scanDetails['PixelResolution']) * 1e-3
            self._pixelInfo = {
                'magnification': mag,
                'mm_x': scale,
                'mm_y': scale,
            }
        except Exception:
            pass

    def _getAssociatedImage(self, imageKey):
        """
        Get an associated image in PIL format.

        :param imageKey: the key of the associated image.
        :return: the image in PIL format or None.
        """
        return self._associatedImages.get(imageKey)

    def getAssociatedImagesList(self):
        """
        Return a list of associated images.

        :return: the list of image keys.
        """
        return list(sorted(self._associatedImages.keys()))

    def _readbox(self, box):
        if box.length > 16 * 1024 * 1024:
            return
        try:
            fp = builtins.open(self._largeImagePath, 'rb')
            headerLength = 16
            fp.seek(box.offset + headerLength)
            data = fp.read(box.length - headerLength)
            return data
        except Exception:
            pass

    def getInternalMetadata(self, **kwargs):
        """
        Return additional known metadata about the tile source.  Data returned
        from this method is not guaranteed to be in any particular format or
        have specific values.

        :returns: a dictionary of data or None.
        """
        results = {}
        if hasattr(self, '_description_record'):
            results['xml'] = self._description_record
        return results

    @methodcache()
    def getTile(self, x, y, z, pilImageAllowed=False, numpyAllowed=False, **kwargs):
        self._xyzInRange(x, y, z)
        step = int(2 ** (self.levels - 1 - z))
        x0 = x * step * self.tileWidth
        x1 = min((x + 1) * step * self.tileWidth, self.sizeX)
        y0 = y * step * self.tileHeight
        y1 = min((y + 1) * step * self.tileHeight, self.sizeY)
        scale = None
        if z < self._minlevel:
            scale = int(2 ** (self._minlevel - z))
            step = int(2 ** (self.levels - 1 - self._minlevel))
        # possible open the file multiple times so multiple threads can access
        # it concurrently.
        while True:
            try:
                # A timeout prevents uniterupptable waits on some platforms
                openjpegHandle = self._openjpegHandles.get(timeout=1.0)
                break
            except queue.Empty:
                continue
        if openjpegHandle is None:
            openjpegHandle = glymur.Jp2k(self._largeImagePath)
        try:
            tile = openjpegHandle[y0:y1:step, x0:x1:step]
        finally:
            self._openjpegHandles.put(openjpegHandle)
        if scale:
            tile = tile[::scale, ::scale]
        return self._outputTile(tile, TILE_FORMAT_NUMPY, x, y, z,
                                pilImageAllowed, numpyAllowed, **kwargs)


def open(*args, **kwargs):
    """
    Create an instance of the module class.
    """
    return OpenjpegFileTileSource(*args, **kwargs)


def canRead(*args, **kwargs):
    """
    Check if an input can be read by the module class.
    """
    return OpenjpegFileTileSource.canRead(*args, **kwargs)
