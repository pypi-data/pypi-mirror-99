import pyqtgraph as pg
import numpy as np
from pyqtgraph.Qt import QtCore
from pyqtgraph import functions as fn
from pyqtgraph.Point import Point
from pyqtgraph import debug as debug
from collections.abc import Callable
import pandas as pd
from ..CustomViewBox.NoPaddingPlot import NoPaddingPlot
import pytplot

class UpdatingImage(pg.ImageItem):
    '''
    This is the class used to plot images of spectrogram data.

    It automatically updates to higher and higher resolutions when you zoom in, thus the name
    "updating image".

    '''


    _MAX_IMAGE_WIDTH = 10000
    _MAX_IMAGE_HEIGHT = 2000
    
    def __init__(self, data, spec_bins, ascending_descending, ytype, ztype, lut, ymin, ymax, zmin, zmax):


        pg.ImageItem.__init__(self)
        
        if ztype=='log':
            data[data <= 0] = np.NaN
            self.data = np.log10(data)
            self.zmin = np.log10(zmin)
            self.zmax = np.log10(zmax)
        else:
            self.data = data
            self.zmin = zmin
            self.zmax = zmax

        self.ytype = ytype
        self.lut = lut
        self.bin_sizes = spec_bins
        self.bins_inc = ascending_descending
        self.w = 100
        self.h = 100
        self.x = self.data.index.tolist()
        self.xmin = np.nanmin(self.x)
        self.xmax = np.nanmax(self.x)

        if len(spec_bins) != 1:

            # If time varying spec bins, we need to reformat the data once.  Turn it into a 1000x100 grid.

            xp = np.linspace(self.xmin, self.xmax, 1000)
            closest_xs = np.searchsorted(self.x, xp)
            minbin = ymin
            maxbin = ymax

            # This will be the values of the 100 y axis pixels
            if ytype == 'log':
                yp = np.logspace(np.log10(minbin), np.log10(maxbin), 100)
            else:
                yp = np.linspace(minbin, maxbin, 100)

            data_reformatted = []
            y_sort = np.argsort(self.bin_sizes.iloc[0].tolist())
            prev_bins = self.bin_sizes.iloc[0]
            prev_closest_ys = np.searchsorted(self.bin_sizes.iloc[0], yp, sorter=y_sort)
            prev_closest_ys[prev_closest_ys > (len(self.bin_sizes.iloc[0]) - 1)] = len(self.bin_sizes.iloc[0]) - 1

            # Loop through every X value and inspect the spec_bins.
            for i in closest_xs:
                if (self.bin_sizes.iloc[i] == prev_bins).all():
                    closest_ys = prev_closest_ys
                else:
                    prev_bins = self.bin_sizes.iloc[i]
                    closest_ys = np.searchsorted(self.bin_sizes.iloc[i], yp, sorter=y_sort)
                    closest_ys[closest_ys > (len(self.bin_sizes.iloc[i])-1)] = len(self.bin_sizes.iloc[i]) - 1
                    prev_closest_ys = closest_ys
                temp_data = self.data.iloc[i][closest_ys].values
                try:
                    temp_data[yp < np.nanmin(self.bin_sizes.iloc[i])] = np.NaN
                    temp_data[yp > np.nanmax(self.bin_sizes.iloc[i])] = np.NaN
                except RuntimeWarning:
                    # If the entire bin is NaN the above stuff fails, so just continue on
                    pass
                data_reformatted.append(temp_data)
            data_reformatted = pd.DataFrame(data_reformatted)

            self.x = xp
            if ytype == 'log':
                self.y = np.linspace(np.log10(minbin), np.log10(maxbin), 100)
            else:
                self.y = np.linspace(minbin, maxbin, 100)
            self.data = data_reformatted
        else:
            if ytype == 'log':
                self.y = np.log10(self.bin_sizes.iloc[0])
            else:
                self.y = self.bin_sizes.iloc[0]

        # Get the ymin/ymax
        if ytype == 'log':
            self.ymin = np.log10(ymin)
            self.ymax = np.log10(ymax)
        else:
            self.ymin = ymin
            self.ymax = ymax

        self.picturenotgened=True
        self.generatePicture()
        

    def generatePicture(self, pixel_size=None):
        # Get the dimensions in pixels and in plot coordiantes
        if pixel_size is None:
            width_in_pixels = pytplot.tplot_opt_glob['window_size'][0]
            height_in_pixels = pytplot.tplot_opt_glob['window_size'][1]
            width_in_plot_coords = pytplot.tplot_opt_glob['window_size'][0]
            height_in_plot_coords = pytplot.tplot_opt_glob['window_size'][1]
        else:
            width_in_pixels = pixel_size.width()
            height_in_pixels = pixel_size.height()
            width_in_plot_coords = self.getViewBox().viewRect().width()
            height_in_plot_coords = self.getViewBox().viewRect().height()
        
        image_width_in_plot_coords = self.xmax - self.xmin
        image_height_in_plot_coords = self.ymax - self.ymin
        
        image_width_in_pixels = int(image_width_in_plot_coords/width_in_plot_coords * width_in_pixels)
        image_height_in_pixels = int(image_height_in_plot_coords/height_in_plot_coords * height_in_pixels)
        if image_width_in_pixels > self._MAX_IMAGE_WIDTH:
            image_width_in_pixels = self._MAX_IMAGE_WIDTH
        if image_height_in_pixels > self._MAX_IMAGE_HEIGHT:
            image_height_in_pixels = self._MAX_IMAGE_HEIGHT
        if self.w != image_width_in_pixels or self.h != image_height_in_pixels:
            self.w = image_width_in_pixels
            self.h = image_height_in_pixels
            if self.w == 0:
                self.w = 1
            if self.h == 0:
                self.h = 1

            data = np.zeros((self.h,self.w))

            # Create an appropriate grid based on the window size, and interpolate the spectrogram to that
            xp = np.linspace(self.xmin, self.xmax, self.w)
            yp = np.linspace(self.ymin, self.ymax, self.h)

            # Find the closest x values in the data for each pixel on the screen
            closest_xs = np.searchsorted(self.x, xp)

            # Find the closest y values in the dat afor each pixel on the screen
            y_sort = np.argsort(self.y.tolist())
            closest_ys = np.searchsorted(self.y, yp, sorter=y_sort)
            closest_ys[closest_ys == len(self.y)] = len(self.y) - 1
            if not self.bins_inc:
                closest_ys = np.flipud(closest_ys)

            # Get the data at those x and y values
            data = self.data.iloc[closest_xs][closest_ys].values

            # Set the image with that data
            self.setImage(data.T, levels=(self.zmin, self.zmax))

            #Image can't handle NaNs, but you can set nan to the minimum and make the minimum transparent.  
            self.setLookupTable(self.lut, update=False)
            self.setRect(QtCore.QRectF(self.xmin,self.ymin,self.xmax-self.xmin,self.ymax-self.ymin))
            return
        
    def paint(self, p, *args):
        '''
        I have no idea why, but we need to generate the picture after painting otherwise 
        it draws incorrectly.  
        '''
        parents = self.getBoundingParents()
        for x in parents:
            if type(x) is NoPaddingPlot:
                parent_viewbox = x
        if self.picturenotgened:
            self.generatePicture(parent_viewbox.rect())
            self.picturenotgened = False
        pg.ImageItem.paint(self, p, *args)
        self.generatePicture(parent_viewbox.rect())

    def render(self):
        #The same as pyqtgraph's ImageItem.render, with the exception that the makeARGB function is slightly different
        
        profile = debug.Profiler()
        if self.image is None or self.image.size == 0:
            return
        if isinstance(self.lut, Callable):
            lut = self.lut(self.image)
        else:
            lut = self.lut

        if self.autoDownsample:
            # reduce dimensions of image based on screen resolution
            o = self.mapToDevice(QtCore.QPointF(0,0))
            x = self.mapToDevice(QtCore.QPointF(1,0))
            y = self.mapToDevice(QtCore.QPointF(0,1))
            w = Point(x-o).length()
            h = Point(y-o).length()
            if w == 0 or h == 0:
                self.qimage = None
                return
            xds = max(1, int(1.0 / w))
            yds = max(1, int(1.0 / h))
            axes = [1, 0] if self.axisOrder == 'row-major' else [0, 1]
            image = fn.downsample(self.image, xds, axis=axes[0])
            image = fn.downsample(image, yds, axis=axes[1])
            self._lastDownsample = (xds, yds)
        else:
            image = self.image

        # if the image data is a small int, then we can combine levels + lut
        # into a single lut for better performance
        levels = self.levels
        if levels is not None and levels.ndim == 1 and image.dtype in (np.ubyte, np.uint16):
            if self._effectiveLut is None:
                eflsize = 2**(image.itemsize*8)
                ind = np.arange(eflsize)
                minlev, maxlev = levels
                levdiff = maxlev - minlev
                levdiff = 1 if levdiff == 0 else levdiff  # don't allow division by 0
                if lut is None:
                    efflut = fn.rescaleData(ind, scale=255./levdiff, 
                                            offset=minlev, dtype=np.ubyte)
                else:
                    lutdtype = np.min_scalar_type(lut.shape[0]-1)
                    efflut = fn.rescaleData(ind, scale=(lut.shape[0]-1)/levdiff,
                                            offset=minlev, dtype=lutdtype, clip=(0, lut.shape[0]-1))
                    efflut = lut[efflut]
                
                self._effectiveLut = efflut
            lut = self._effectiveLut
            levels = None
        
        # Assume images are in column-major order for backward compatibility
        # (most images are in row-major order)
        
        if self.axisOrder == 'col-major':
            image = image.transpose((1, 0, 2)[:image.ndim])
        
        argb, alpha = makeARGBwithNaNs(image, lut=lut, levels=levels)
        self.qimage = fn.makeQImage(argb, alpha, transpose=False)

    def setImage(self, image=None, autoLevels=None, **kargs):
        """
        Same this as ImageItem.setImage, but we don't update the drawing
        """
        
        profile = debug.Profiler()

        gotNewData = False
        if image is None:
            if self.image is None:
                return
        else:
            gotNewData = True
            shapeChanged = (self.image is None or image.shape != self.image.shape)
            image = image.view(np.ndarray)
            if self.image is None or image.dtype != self.image.dtype:
                self._effectiveLut = None
            self.image = image
            if self.image.shape[0] > 2**15-1 or self.image.shape[1] > 2**15-1:
                if 'autoDownsample' not in kargs:
                    kargs['autoDownsample'] = True
            if shapeChanged:
                self.prepareGeometryChange()
                self.informViewBoundsChanged()

        profile()

        if autoLevels is None:
            if 'levels' in kargs:
                autoLevels = False
            else:
                autoLevels = True
        if autoLevels:
            img = self.image
            while img.size > 2**16:
                img = img[::2, ::2]
            mn, mx = img.min(), img.max()
            if mn == mx:
                mn = 0
                mx = 255
            kargs['levels'] = [mn,mx]

        profile()

        self.setOpts(update=False, **kargs)

        profile()

        self.qimage = None
        self.update()

        profile()

        if gotNewData:
            self.sigImageChanged.emit()
            
    
def makeARGBwithNaNs(data, lut=None, levels=None, scale=None, useRGBA=False): 
    """ 
    This is the same as pyqtgraph.makeARGB, except that all NaN's in the data are set to transparent pixels
    """
    
    nanlocations = np.isnan(data)
    profile = debug.Profiler()

    if data.ndim not in (2, 3):
        raise TypeError("data must be 2D or 3D")
    if data.ndim == 3 and data.shape[2] > 4:
        raise TypeError("data.shape[2] must be <= 4")
    
    if lut is not None and not isinstance(lut, np.ndarray):
        lut = np.array(lut)
    
    if levels is None:
        # automatically decide levels based on data dtype
        if data.dtype.kind == 'u':
            levels = np.array([0, 2**(data.itemsize*8)-1])
        elif data.dtype.kind == 'i':
            s = 2**(data.itemsize*8 - 1)
            levels = np.array([-s, s-1])
        elif data.dtype.kind == 'b':
            levels = np.array([0,1])
        else:
            raise Exception('levels argument is required for float input types')
    if not isinstance(levels, np.ndarray):
        levels = np.array(levels)
    if levels.ndim == 1:
        if levels.shape[0] != 2:
            raise Exception('levels argument must have length 2')
    elif levels.ndim == 2:
        if lut is not None and lut.ndim > 1:
            raise Exception('Cannot make ARGB data when both levels and lut have ndim > 2')
        if levels.shape != (data.shape[-1], 2):
            raise Exception('levels must have shape (data.shape[-1], 2)')
    else:
        raise Exception("levels argument must be 1D or 2D (got shape=%s)." % repr(levels.shape))

    profile()

    # Decide on maximum scaled value
    if scale is None:
        if lut is not None:
            scale = lut.shape[0] - 1
        else:
            scale = 255.

    # Decide on the dtype we want after scaling
    if lut is None:
        dtype = np.ubyte
    else:
        dtype = np.min_scalar_type(lut.shape[0]-1)
            
    # Apply levels if given
    if levels is not None:
        if isinstance(levels, np.ndarray) and levels.ndim == 2:
            # we are going to rescale each channel independently
            if levels.shape[0] != data.shape[-1]:
                raise Exception("When rescaling multi-channel data, there must be the same number of levels as channels (data.shape[-1] == levels.shape[0])")
            newData = np.empty(data.shape, dtype=int)
            for i in range(data.shape[-1]):
                minVal, maxVal = levels[i]
                if minVal == maxVal:
                    maxVal += 1e-16
                newData[...,i] = fn.rescaleData(data[...,i], scale/(maxVal-minVal), minVal, dtype=dtype)
            data = newData
        else:
            # Apply level scaling unless it would have no effect on the data
            minVal, maxVal = levels
            if minVal != 0 or maxVal != scale:
                if minVal == maxVal:
                    maxVal += 1e-16
                data = fn.rescaleData(data, scale/(maxVal-minVal), minVal, dtype=dtype)
            

    profile()

    # apply LUT if given
    if lut is not None:
        data = fn.applyLookupTable(data, lut)
    else:
        if data.dtype is not np.ubyte:
            data = np.clip(data, 0, 255).astype(np.ubyte)
    
    #Set NaNs to transparent
    data[nanlocations] = [0,0,0,0]
    
    profile()

    # this will be the final image array
    imgData = np.empty(data.shape[:2]+(4,), dtype=np.ubyte)

    profile()

    # decide channel order
    if useRGBA:
        order = [0,1,2,3] # array comes out RGBA
    else:
        order = [2,1,0,3] # for some reason, the colors line up as BGR in the final image.
        
    # copy data into image array
    if data.ndim == 2:
        # This is tempting:
        #   imgData[..., :3] = data[..., np.newaxis]
        # ..but it turns out this is faster:
        for i in range(3):
            imgData[..., i] = data
    elif data.shape[2] == 1:
        for i in range(3):
            imgData[..., i] = data[..., 0]
    else:
        for i in range(0, data.shape[2]):
            imgData[..., i] = data[..., order[i]] 
        
    profile()
    
    # add opaque alpha channel if needed
    if data.ndim == 2 or data.shape[2] == 3:
        alpha = False
        imgData[..., 3] = 255
    else:
        alpha = True
        
    profile()
    return imgData, alpha