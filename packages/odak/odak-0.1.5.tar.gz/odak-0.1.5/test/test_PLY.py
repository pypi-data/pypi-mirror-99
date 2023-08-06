import odak.raytracing as raytracer
import sys
import numpy as np
import odak
from odak.visualize import PLY_object

def test():
    cad = odak.visualize.PLY_object()
    for i in np.linspace(-10,10,5):
        for j in np.linspace(-10,10,5):
            color = [
                     np.int(np.random.rand()*255),
                     np.int(np.random.rand()*255),
                     np.int(np.random.rand()*255)
                    ]
            cad.draw_a_ray([0.,0.,0.],[i,j,50.],color=color)
    cad.save_PLY(savefn='out.ply')
    assert True==True

if __name__ == '__main__':
    sys.exit(test())
