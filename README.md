# ImgPointIndicator
    ImagePointIndicator is a tool on which we can generate coordinates of polygons we drew on an image 

## Features
* Draw a polygon in 2 different mode: [Drag mode](#drag-mode) & [Point mode](#point-mode-precision-mode)
* Add label to identify drawn polygon
* Import image 
* Export / Import date file which contains coordinates of polygons
* Remove the last polygon
* Change the format of print in text area (transform data already printed)
* Copy data in the text area to clipboard
* Zoom the image for better precision

### Drag mode
We can draw simple rectangles or squares by dragging from the first point and dropping at the last point.

### Point mode (Precision mode)
In this mode we can draw a real polygon point by point to get the best and the most precise polygon.
 
## Requirements
* [Python 3.x](https://docs.python.org/3/)
* [Pillow](https://pillow.readthedocs.io/en/stable/) (PIL fork)  
    Installation by Pip:
    ``` bash
        pip install Pillow
    ```

## Licence
MIT License

Copyright (c) [2018] [casafan.yang@gmail.com]
