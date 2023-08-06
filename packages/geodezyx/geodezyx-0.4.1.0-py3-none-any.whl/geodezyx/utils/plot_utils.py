#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 31 14:19:37 2019

@author: psakicki
"""

########## BEGIN IMPORT ##########
#### External modules
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import os
import scipy
#### geodeZYX modules
from geodezyx import utils

##########  END IMPORT  ##########


def color_list(L , colormap='jet'):
    cm     = plt.get_cmap(colormap)
    NCOL   = len(np.unique(L))
    colist = [cm(1.*i/NCOL) for i in range(NCOL)]
    return colist

def symbols_list(L=None):

    Lsym = ["o",
    "v",
    "^",
    "<",
    ">",
    ".",
    ",",
    "1",
    "2",
    "3",
    "4",
    "8",
    "s",
    "p",
    "P",
    "*",
    "h",
    "H",
    "+",
    "x",
    "X",
    "D",
    "d",
    "|",
    "_"]

    if not L:
        return Lsym
    else:
        return Lsym[:len(L)]



def colors_from_colormap_getter(ncolors , colormap = 'viridis'):
    import matplotlib.pyplot as plt
    cm = plt.get_cmap(colormap)
    return [cm(1.*i/ncolors) for i in range(ncolors)]

def ylim_easy(Lin,delta = .1, min_null_if_neg = False):
    minn = np.min(Lin)
    maxx = np.max(Lin)
    rangee = np.abs(maxx - minn)
    if  min_null_if_neg and (minn - delta * rangee) < 0. :
        return (0. , maxx + delta * rangee)
    else:
        return (minn - delta * rangee , maxx + delta * rangee)

def get_figure(figin = 0):
    # Un autre exemple comme défini dans
    # export_ts_figure_pdf
    #    if type(fig) is int:
    #        f = plt.figure(fig)
    #    elif type(fig) is Figure:
    #        f = fig
    if isinstance(figin,matplotlib.figure.Figure):
        figout = figin
    elif figin == 0:
        figout = plt.figure()
    else:
        figout = plt.figure(figin)
    # be sure the fig have a axe (necessary ?)
    if figout.get_axes() == []:
        figout.add_subplot(111)
    plt.figure(figout.number)
    return figout


def figure_saver(figobjt_in , outdir , outname ,
                 outtype = ('.png','.pdf','.figpik') , formt = 'a4' ,
                 transparent=False):
    
    if not utils.is_iterable(outtype):
         outtype = (outtype,) 
         
    outpath_stk = []
    for outtype_iter in outtype:
        if "pik" in outtype_iter:
            outpath = utils.pickle_saver(figobjt_in,outdir,
                                         outname,outtype_iter)
        else:   
            outpath = os.path.join(outdir,outname+outtype_iter)
            #figobjt_in.savefig(outpath)
            figobjt_in.savefig(outpath,transparent=transparent)

        outpath_stk.append(outpath)
        
    if len(outpath_stk) == 1:
        outpath_stk = outpath_stk[0]
    return outpath_stk


def axis_data_coords_sys_transform(axis_obj_in,xin,yin,inverse=False):
    """ inverse = False : Axis => Data
                = True  : Data => Axis
    """
    xlim = axis_obj_in.get_xlim()
    ylim = axis_obj_in.get_ylim()

    xdelta = xlim[1] - xlim[0]
    ydelta = ylim[1] - ylim[0]
    if not inverse:
        xout =  xlim[0] + xin * xdelta
        yout =  ylim[0] + yin * ydelta
    else:
        xdelta2 = xin - xlim[0]
        ydelta2 = yin - ylim[0]
        xout = xdelta2 / xdelta
        yout = ydelta2 / ydelta
    return xout,yout

def id2val(value_lis,id_lis,idin):
    """ from a value list and a id pointer list
        return the good val from the good id
        replace dico bc. set is not supproted as key"""
    return value_lis[id_lis.index(idin)]

def set_size_for_pub(width=418.25368, fraction=1,subplot=[1, 1]):
    """ Set aesthetic figure dimensions to avoid scaling in latex.

    Parameters
    ----------
    width: float
            Width in pts
    fraction: float
            Fraction of the width which you wish the figure to occupy

    Returns
    -------
    fig_dim: tuple
            Dimensions of figure in inches
    """
    # Width of figure
    fig_width_pt = width * fraction

    # Convert from pt to inches
    inches_per_pt = 1 / 72.27

    # Golden ratio to set aesthetic figure height
    golden_ratio = (5**.5 - 1) / 2

    # Figure width in inches
    fig_width_in = fig_width_pt * inches_per_pt
    # Figure height in inches
    fig_height_in = fig_width_in * golden_ratio * (subplot[0] / subplot[1])

    fig_dim = (fig_width_in, fig_height_in)

    return fig_dim


def gaussian_for_plot(D,density=False,nbins=500,nsigma=3.5):
    """
    generate a gaussian curve for histogram plot

    Parameters
    ----------
    D : iterable
        data vector.
    density : bool, optional
        Adapted curve for desity mode. The default is False.
    nbins : int, optional
        number of bins. The default is 500.
    nsigma : TYPE, optional
        n sigmas for the x axis. The default is 3.5.

    Returns
    -------
    Xpdf : array
        gaussian curve x.
    Ypdf_out : TYPE
        gaussian curve x.

    """

    mu = np.mean(D)
    sigma = np.std(D)
    Xpdf = np.linspace(mu - nsigma*sigma,
                       mu + nsigma*sigma,
                       nbins)
    Ypdf = scipy.stats.norm.pdf(Xpdf, mu, sigma)
    Ypdf_out = Ypdf
    if not density:
        Ybin,Xbin = np.histogram(D,bins=nbins)
        area_bin = np.trapz(Ybin,dx=np.diff(Xbin)[0])
        
        Ypdf_out = Ypdf*area_bin
        
    return Xpdf,Ypdf_out    
