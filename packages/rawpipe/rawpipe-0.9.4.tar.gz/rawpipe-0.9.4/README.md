# rawpipe

[![Build Status](https://travis-ci.org/toaarnio/rawpipe.svg?branch=master)](https://travis-ci.org/toaarnio/rawpipe)

A collection of reference ISP algorithms, sufficient for producing a reasonably
good looking image from raw sensor data. Each algorithm takes in a frame in RGB
or raw format and returns a modified copy of the frame. The frame is expected to
be a NumPy float array with either 2 or 3 dimensions, depending on the function.
Some of the algorithms can be applied in different orders (demosaicing before or
after linearization, for example), but the reference ordering is as shown below.

**Example:**
```
import rawpipe
...
algs = rawpipe.Algorithms(verbose=True)
raw = algs.downsample(raw, iterations=2)
raw = algs.linearize(raw, blacklevel=64, whitelevel=1023)
rgb = algs.demosaic(raw, "RGGB")
rgb = algs.lsc(rgb, my_vignetting_map)
rgb = algs.lsc(rgb, my_color_shading_map)
rgb = algs.resize(rgb, 400, 300)
rgb = algs.wb(rgb, [1.5, 2.0])
rgb = algs.ccm(rgb, my_3x3_color_matrix)
rgb = algs.tonemap(rgb, "Reinhard")
rgb = algs.chroma_denoise(rgb)
rgb = algs.saturate(rgb, lambda x: x ** 0.5)
rgb = algs.gamma(rgb, "sRGB")
rgb = algs.quantize(rgb, 255)
```

**Installing on Linux:**
```
pip install rawpipe
```

**Documentation:**
```
pydoc rawpipe
```

**Building & installing from source:**
```
make install
```

**Building & releasing to PyPI:**
```
make release
```
