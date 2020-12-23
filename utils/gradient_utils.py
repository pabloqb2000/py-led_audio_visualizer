import numpy as np
from colour import Color

'''
    Returns a gradient 
    of n different colors
    in list format
    between c1 and c2
    in 0-255 RGB format
    Modes: hsl / rgb
'''
def get_gradient_1d(c1, c2, mode="hsl", n=256):
    if 'rgb' == mode:
        r1, g1, b1 = c1.rgb
        r2, g2, b2 = c2.rgb
        r_range = np.floor(np.linspace(r1, r2, n)*255)
        g_range = np.floor(np.linspace(g1, g2, n)*255)
        b_range = np.floor(np.linspace(b1, b2, n)*255)
        return [(r, g, b) for r,g,b in zip(r_range, g_range, b_range)]
    else:
        gradient = list(c1.range_to(c2,n))
        return [(int(c.red*255), int(c.green*255), int(c.blue*255)) for c in gradient]

'''
    Returns a gradient
    in nxnx3 numpy array
    with this shape
    c1 -- c2
    |      |
    c3 -- c4
    in 0-255 RGB format
    Modes: hsl / rgb / hsl-l / rgb-l
'''
def get_gradient_2d(c1, c2, c3=Color('#000000'), c4=Color('#000000'), mode="hsl-l", n=256):
    if '-l' in mode:
        grad_1 = np.array(get_gradient_1d(c1, c2, mode[:3], n))
        gradient_2d = (np.linspace(1, 0, n).reshape((-1,1)) * grad_1.reshape(-1)).reshape((n,n,3))
    else:
        grad_1, grad_2 = get_gradient_1d(c1, c3, mode, n), get_gradient_1d(c2, c4, mode, n)
        gradient_2d = np.array([
            get_gradient_1d(
                Color(rgb=(c_a[0]/255, c_a[1]/255, c_a[2]/255)),
                Color(rgb=(c_b[0]/255, c_b[1]/255, c_b[2]/255)),
                mode,
                n
            )
            for c_a, c_b in zip(grad_1, grad_2)
        ])

    return gradient_2d