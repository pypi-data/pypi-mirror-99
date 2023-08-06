# ImageLayers


## Installation
There are a variety of ways to install this project.

### From [Github](https://github.com/GrandMoff100/ImageLayers)
```
$ git clone https://github.com/GrandMoff100/ImageLayers
```

### From [PyPI](https://pypi.org/project/imagelayers)
```
$ pip install imagelayers
```

## Usage

This project provides two classes, `ImageLayer`, and `LayeredImage`.

### Example
```py
from PIL import Image

with Image.open('image.png') as f:
    img = LayeredImage(f)

    i = 0
    for layer in img.layersbyedge(): # layer is an instance of `ImageLayer`
        layer.save(f'layer{i}.png')
        i += 1
```
