# Seam Carving

This is basically just turning the repo [here](https://github.com/AlexZeGamer/distort-video) into a module that can be imported into Python and used,
since I liked the functionality of the program but needed to use it by calling it from another Python script and passing it arguments.
I also removed the wobbly sound effect and added a few extra options that I specifically needed for my project.
It is still very much a work in progress.

# Installation:
- You'll need to have Image Magick installed and the script needs to be able to find it. On Windows, this means adding it to your PATH.
- pip install -r requirements.txt

# Usage
```
from seamcarvelib import seamcarve
seamcarve.carve_seams(in_file, out_file, distort_percentage=60, silent=False)
```
Please note that due to the nature of seam carving, it will take a rather long time to process larger files. 

# TODO:
- [ ] Add more tests to pytest
- [ ] Add more options for wiggling
- [ ] Potentially allow for other (Or maybe arbitrary, using Image Magick FX) effects besides seam carving
- [ ] Publish to PyPi
