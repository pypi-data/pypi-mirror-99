from odak import np
import torch

def quadratic_phase_function(nx,ny,k,focal=0.4,dx=0.001,offset=[0,0]):
    """ 
    A definition to generate 2D quadratic phase function, which is typically use to represent lenses.

    Parameters
    ----------
    nx         : int
                 Size of the output along X.
    ny         : int
                 Size of the output along Y.
    k          : odak.wave.wavenumber
                 See odak.wave.wavenumber for more.
    focal      : float
                 Focal length of the quadratic phase function.
    dx         : float
                 Pixel pitch.
    offset     : list
                 Deviation from the center along X and Y axes.

    Returns
    ---------
    function   : ndarray
                 Generated quadratic phase function.
    """
    size  = [ny,nx]
    x     = torch.linspace(-size[0]*dx/2,size[0]*dx/2,size[0])-offset[1]*dx
    y     = torch.linspace(-size[1]*dx/2,size[1]*dx/2,size[1])-offset[0]*dx
    X,Y   = torch.meshgrid(x,y)
    Z     = X**2+Y**2
    focal = torch.tensor([focal])
    k     = torch.tensor([k])
    qwf  = torch.exp(1j*k*0.5*torch.sin(Z/focal))
    return qwf

def prism_phase_function(nx,ny,k,angle,dx=0.001,axis='x'):
    """
    A definition to generate 2D phase function that represents a prism. See Goodman's Introduction to Fourier Optics book for more.

    Parameters
    ----------
    nx         : int
                 Size of the output along X.
    ny         : int
                 Size of the output along Y.
    k          : odak.wave.wavenumber
                 See odak.wave.wavenumber for more.
    angle      : float
                 Tilt angle of the prism in degrees.
    dx         : float
                 Pixel pitch.
    axis       : str
                 Axis of the prism.

    Returns
    ----------
    prism      : torch.tensor
                 Generated phase function for a prism.
    """
    angle = torch.deg2rad(torch.tensor([angle]))
    size  = [ny,nx]
    x     = torch.linspace(-size[0]*dx/2,size[0]*dx/2,size[0])
    y     = torch.linspace(-size[1]*dx/2,size[1]*dx/2,size[1])
    X,Y   = torch.meshgrid(x,y)
    if axis == 'y':
        prism = torch.exp(-1j*k*torch.sin(angle)*Y)
    elif axis == 'x':
        prism = torch.exp(-1j*k*torch.sin(angle)*X)
    return prism
