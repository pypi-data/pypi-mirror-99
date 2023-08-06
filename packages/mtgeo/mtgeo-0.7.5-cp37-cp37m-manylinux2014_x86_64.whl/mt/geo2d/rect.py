'''A 2D rectangle.'''

from mt import np
from mt.base.casting import *

from ..geo import TwoD, register_approx, register_join_volume
from ..geond import Hyperbox
from .moments import Moments2d
from .iou import iou_impl


__all__ = ['Rect', 'cast_Hyperbox_to_Rect', 'cast_Rect_to_Moments2d', 'approx_Moments2d_to_Rect']


class Rect(TwoD, Hyperbox):
    '''A 2D rectangle,

    Note we do not care if the rectangle is open or partially closed or closed.'''

    
    # ----- internal representations -----


    @property
    def shapely(self):
        '''Shapely representation for fast intersection operations.'''
        if not hasattr(self, '_shapely'):
            import shapely.geometry as _sg
            self._shapely = _sg.box(self.min_x, self.min_y, self.max_x, self.max_y)
            self._shapely = self._shapely.buffer(0.0001) # to clean up any (multi and/or non-simple) polygon into a simple polygon
        return self._shapely


    # ----- derived properties -----

    
    @property
    def min_x(self):
        '''lowest x-coordinate.'''
        return self.min_coords[0]

    @property
    def min_y(self):
        '''lowest x-coodinate.'''
        return self.min_coords[1]

    @property
    def max_x(self):
        '''highest x-coordinate.'''
        return self.max_coords[0]

    @property
    def max_y(self):
        '''highest y-coordinate.'''
        return self.max_coords[1]

    @property
    def x(self):
        '''left, same as min_x.'''
        return self.min_x

    @property
    def y(self):
        '''top, same as min_y.'''
        return self.min_y

    @property
    def w(self):
        '''width'''
        return self.max_x - self.min_x

    @property
    def h(self):
        '''height'''
        return self.max_y - self.min_y

    @property
    def cx(self):
        '''Center x-coordinate.'''
        return (self.min_x + self.max_x)/2

    @property
    def cy(self):
        '''Center y-coordinate.'''
        return (self.min_y + self.max_y)/2

    @property
    def area(self):
        '''Absolute area.'''
        return abs(self.w*self.h)

    @property
    def circumference(self):
        '''Circumference.'''
        return (abs(self.w)+abs(self.h))*2

    @property
    def min_pt(self):
        '''Corner point with minimum coordinates.'''
        return np.array([self.min_x, self.min_y])

    @property
    def max_pt(self):
        '''Corner point with maximum coordinates.'''
        return np.array([self.max_x, self.max_y])

    @property
    def center_pt(self):
        '''Center point.'''
        return np.array([self.cx, self.cy])

    
    # ----- moments -----


    @property
    def signed_area(self):
        '''Returns the signed area of the rectangle.'''
        return self.w*self.h

    @property
    def moment_x(self):
        '''Returns the integral of x over the rectangle's interior.'''
        return self.signed_area*self.cx

    @property
    def moment_y(self):
        '''Returns the integral of y over the rectangle's interior.'''
        return self.signed_area*self.cy

    @property
    def moment_xy(self):
        '''Returns the integral of x*y over the rectangle's interior.'''
        return self.moment_x*self.cy

    @property
    def moment_xx(self):
        '''Returns the integral of x*x over the rectangle's interior.'''
        return self.signed_area*(self.min_x*self.min_x+self.min_x*self.max_x+self.max_x*self.max_x)/3

    @property
    def moment_yy(self):
        '''Returns the integral of y*y over the rectangle's interior.'''
        return self.signed_area*(self.min_y*self.min_y+self.min_y*self.max_y+self.max_y*self.max_y)/3


    # ----- serialization -----


    def to_json(self):
        '''Returns a list [min_x, min_y, max_x, max_y].'''
        return [self.min_x, self.min_y, self.max_x, self.max_y]


    @staticmethod
    def from_json(json_obj):
        '''Creates a Rect from a JSON-like object.

        Parameters
        ----------
        json_obj : list
            list [min_x, min_y, max_x, max_y]

        Returns
        -------
        Rect
            output rectangle
        '''
        return Rect(json_obj[0], json_obj[1], json_obj[2], json_obj[3])

    
    # ----- methods -----

    
    def __init__(self, min_x, min_y, max_x, max_y, force_valid=False):
        super(Rect, self).__init__(np.array([min_x, min_y]), np.array([max_x, max_y]), force_valid = force_valid)

    def __repr__(self):
        return "Rect(x={}, y={}, w={}, h={})".format(self.x, self.y, self.w, self.h)

    def intersect(self, other):
        res = super(Rect, self).intersect(other)
        return Rect(res.min_coords[0], res.min_coords[1], res.max_coords[0], res.max_coords[1])

    def iou(self, other, epsilon=1E-7):
        return iou_impl(self.intersect(other).area, self.area, other.area, eps=epsilon)
        
    def move(self, offset):
        '''Moves the Rect by a given offset vector.'''
        return Rect(self.min_x + offset[0], self.min_y + offset[1], self.max_x + offset[0], self.max_y + offset[1])


# ----- casting -----
        

register_cast(Rect, Hyperbox, lambda x: Hyperbox(x.dlt_tfm))
register_castable(Hyperbox, Rect, lambda x: x.dim==2)

def cast_Hyperbox_to_Rect(x):
    '''Casts a Hyperbox to a Rect.'''
    min_coords = x.min_coords
    max_coords = x.max_coords
    return Rect(min_coords[0], min_coords[1], max_coords[0], max_coords[1])
register_cast(Hyperbox, Rect, cast_Hyperbox_to_Rect)


def cast_Rect_to_Moments2d(obj):
    m0 = obj.signed_area
    m1 = [obj.moment_x, obj.moment_y]
    mxy = obj.moment_xy
    m2 = [[obj.moment_xx, mxy], [mxy, obj.moment_yy]]
    return Moments2d(m0, m1, m2)
register_cast(Rect, Moments2d, cast_Rect_to_Moments2d)


# ----- approximation -----


def approx_Moments2d_to_Rect(obj):
    '''Approximates a Moments2d instance with a rect such that the mean aligns with the rect's center, and the covariance matrix of the instance is closest to the moment convariance matrix of the rect.'''
    cx, cy = obj.mean
    cov = obj.cov

    # w = half width, h = half height
    size = abs(obj.m0)
    hw3 = cov[0][0]*size*0.75 # should be >= 0
    wh3 = cov[1][1]*size*0.75 # should be >= 0
    wh = np.sqrt(np.sqrt(wh3*hw3))
    h = np.sqrt(wh3/wh)
    w = np.sqrt(hw3/wh)
    return Rect(cx-w, cy-h, cx+w, cy+h)
register_approx(Moments2d, Rect, approx_Moments2d_to_Rect)


# ----- joining volumes -----


def join_volume_Rect_and_Rect(obj1, obj2):
    '''Joins the areas of two Rects.

    Parameters
    ----------
    obj1 : Rect
        the first rectangle
    obj2 : Rect
        the second rectangle

    Returns
    -------
    intersection_area : float
        the area of the intersection of the two Rects' interior regions
    obj1_only_area : float
        the area of the interior of obj1 that does not belong to obj2
    obj2_only_area : float
        the area of the interior of obj2 that does not belong to obj1
    union_area : float
        the area of the union of the two Rects' interior regions
    '''
    inter = obj1.intersect(obj2)
    inter_area = inter.area
    obj1_area = obj1.area
    obj2_area = obj2.area
    return (inter_area, obj1_area - inter_area, obj2_area - inter_area, obj1_area + obj2_area - inter_area)
register_join_volume(Rect, Rect, join_volume_Rect_and_Rect)
