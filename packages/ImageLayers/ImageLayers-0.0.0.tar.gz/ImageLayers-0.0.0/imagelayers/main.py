from PIL import Image, ImageDraw
from collections import defaultdict
import copy

from .util import coordgen


class ImageLayer:
    def __init__(self, image, pixelcoords=[], color=(0,0,0,255)):
        self.pxcs = set(pixelcoords)
        self.color = tuple(color)
        self.image = image
    
    def add_pixel(self, x, y):
        self.pxcs = set(list(self.pxcs) + [(x,y)])

    def set_color(self, rgb):
        self.color = rgb
    
    def copy(self):
        return ImageLayer(self.image, copy.copy(self.pxcs), copy.copy(self.color))

    def __add__(self, other):
        pxcs = list(self.pxcs) + list(other.pxcs)
        return ImageLayer(self.image, pxcs, self.color)
    
    def __sub__(self, other):
        pxcs = [coord for coord in self.pxcs if coord not in other.pxcs]
        return ImageLayer(self.image, pxcs, color=self.color)

    def __pos__(self):
        return self.copy()
    
    def __neg__(self):
        pxcs = []
        for x in range(self.image.width):
            for y in range(self.image.height):
                if (x,y) not in self.pxcs:
                    pxcs.append((x,y))
        return ImageLayer(self.image, pxcs, copy.copy(self.color))
    
    def __eq__(self, other):
        return set(self.pxcs) == set(other.pxcs)

    def __or__(self, other):
        pxcs = [xy for xy in other.pxcs if xy in self.pxcs]
        return ImageLayer(self.image, pxcs, self.color)

    def __repr__(self):
        return f'<ImageLayer color={self.color}>'
    
    def save(self, *args, **kwargs):
        return self.toimage().save(*args, **kwargs)
    
    def toimage(self):
        img = Image.new('RGBA', self.image.size, color=(0,0,0,255))
        px = img.load()
        for x, y in self.pxcs:
            px[x,y] = self.color
        return img
    
    def hexcolor(self, include_a=False):
        r,g,b,a = self.color
        color = (r,g,b,a) if include_a else (r,g,b)
        return '0x' + ''.join([hex(val)[2:].zfill(2) for val in color])

    def __len__(self):
        return len(self.pxcs)


class OptimalColors:
    def __init__(self, colors: tuple):
        for tup in colors:
            if type(tup) not in [list, tuple]:
                raise ValueError('Color must be tuple or list')
        self.colors = colors

    def adjustpixelrgb(self, pixel, limit=1, shift=0):
        r,g,b = pixel
        for mr,mg,mb in self.colors:
            if mr - limit + shift < r < mr + limit + shift and \
                mg - limit + shift < g < mg + limit + shift and \
                mb - limit + shift < b < mb + limit + shift:
                return mr,mg,mb
        return pixel
    
    def adjustpixelrgba(self, pixel, limit=1, shift=0):
        r,g,b,a = pixel
        for mr,mg,mb,ma in self.colors:
            if mr - limit + shift < r < mr + limit + shift and \
                mg - limit + shift < g < mg + limit + shift and \
                mb - limit + shift < b < mb + limit + shift and \
                ma - limit + shift < a < ma + limit +shift:
                return mr,mg,mb,ma
        return pixel
    
    def optimize_image(self, image, tolerance=1, bwshift=0):
        px = image.load()
        for x in range(image.width):
            for y in range(image.height):
                try:
                    px[x,y] = self.adjustpixelrgb(px[x,y], tolerance, bwshift)
                except ValueError:
                    px[x,y] = self.adjustpixelrgba(px[x,y], tolerance, bwshift)

class LayeredImage:
    def __init__(self, image):
        self.image = image
        
    def colorset(self):
        px = self.image.load()
        colors = [px[x,y] for x,y in coordgen(*self.image.size)]
        return set(colors)
    
    def layersbycolor(self):
        pixels = defaultdict(list)
        px = self.image.load()
        for x,y in coordgen(*self.image.size):
            pixels[str(px[x,y])].append((x,y))
        for color, coords in pixels.items():
            color = [int(x) for x in color[:-1][1:].split(', ')]
            yield ImageLayer(self.image, coords, color)

    def layersbyedge(self):
        orig = self.image.copy()
        px = orig.load()

        pixels = set()
        for x in range(orig.width):
            for y in range(orig.height):
                if (x,y) in pixels:
                    continue
                ImageDraw.floodfill(orig, xy=(x,y), value=(0,0,0,0))
                group = filter(lambda x: px[x] == (0,0,0,0), coordgen(*orig.size))
                layer = ImageLayer(self.image, group, color=(255,255,255,255))
                del group
                for pixel in layer.pxcs:
                    if pixel not in pixels:
                        pixels.add(pixel)
                yield layer
                del layer

                orig = self.image.copy()
                px = orig.load()
        
    def optimize_color_boundaries(self, colors: tuple):
        optcolors = OptimalColors(colors)
        optcolors.optimize_image(self.image)

