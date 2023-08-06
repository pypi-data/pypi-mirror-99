#!/usr/bin/env python
# define some variables
from __future__ import print_function
from builtins import input
import numpy
import sys
import matplotlib
if matplotlib.get_backend() != "TKAgg":
   matplotlib.use("TKAgg")

import pmagpy.pmag as pmag
import pmagpy.pmagplotlib as pmagplotlib

def main():
    """
    NAME 
        plot_map_pts.py 

    DESCRIPTION
        plots points on map
 
    SYNTAX
        plot_map_pts.py [command line options]

    OPTIONS
        -h prints help and quits
        -sym [ro, bs, g^, r., b-, etc.] [1,5,10] symbol and size for points
           colors are r=red,b=blue,g=green, etc.
           symbols are '.' for points, ^, for triangle, s for square, etc.
            -, for lines, -- for dotted lines, see matplotlib online documentation for plot()
        -eye  ELAT ELON [specify eyeball location]
        -etp  put on topography
        -cmap color map [default is jet]
        -f FILE, specify input file
        -o color ocean blue/land green (default is not)
        -res [c,l,i,h] specify resolution (crude, low, intermediate, high]
        -fmt [pdf,eps, png] specify output format (default is pdf)
        -R don't plot details of rivers
        -B don't plot national/state boundaries, etc.
        -pad [LAT LON] pad bounding box by LAT/LON (default is not)
        -grd SPACE specify grid spacing
        -sav  save plot and quit
        -prj PROJ,  specify one of the supported projections: 
            pc = Plate Carree
            aea = Albers Equal Area
            aeqd = Azimuthal Equidistant
            lcc = Lambert Conformal
            lcyl = Lambert Cylindrical
            merc = Mercator
            mill = Miller Cylindrical
            moll = Mollweide [default]
            ortho = Orthographic
            robin = Robinson
            sinu = Sinusoidal
            stere = Stereographic
            tmerc = Transverse Mercator
            utm = UTM
            laea = Lambert Azimuthal Equal Area
            geos = Geostationary
            npstere = North-Polar Stereographic
            spstere = South-Polar Stereographic
        Special codes for MagIC formatted input files:
            -n
            -l
    
    INPUTS
        space or tab delimited LON LAT data
        OR: 
           standard MagIC formatted er_sites or pmag_results table
    DEFAULTS
        res:  c
        prj: mollweide;  lcc for MagIC format files 
        ELAT,ELON = 0,0
        pad LAT,LON=0,0
        NB: high resolution or lines can be very slow
    
    """
    dir_path='.'
    plot=0
    ocean=0
    res='c'
    proj='moll'
    Lats,Lons=[],[]
    fmt='pdf'
    sym='ro'
    symsize=5
    fancy=0
    rivers,boundaries,ocean=1,1,0
    latmin,latmax,lonmin,lonmax,lat_0,lon_0=-90,90,0.,360.,0.,0.
    padlat,padlon,gridspace=0,0,30
    lat_0,lon_0="",""
    basemap=1
    prn_name,prn_loc,names,locs=0,0,[],[]
    if '-WD' in sys.argv:
        ind = sys.argv.index('-WD')
        dir_path=sys.argv[ind+1]
    if '-h' in sys.argv:
        print(main.__doc__)
        sys.exit()
    if '-fmt' in sys.argv:
        ind = sys.argv.index('-fmt')
        fmt=sys.argv[ind+1]
    if '-res' in sys.argv:
        ind = sys.argv.index('-res')
        res=sys.argv[ind+1]
        if res!= 'c' and res!='l':
            print('this resolution will take a while - be patient')
    if '-etp' in sys.argv: 
        fancy=1
        print ('-W- plotting will require patience!')
    if '-ctp' in sys.argv: basemap=0
    if '-sav' in sys.argv: plot=1
    if '-R' in sys.argv:rivers=0
    if '-B' in sys.argv:boundaries=0
    if '-o' in sys.argv:ocean=1
    if '-cmap' in sys.argv:
        ind = sys.argv.index('-cmap')
        cmap=float(sys.argv[ind+1])
    else:
        cmap='jet'
    if '-grd' in sys.argv:
        ind = sys.argv.index('-grd')
        gridspace=float(sys.argv[ind+1])
    if '-eye' in sys.argv:
        ind = sys.argv.index('-eye')
        lat_0=float(sys.argv[ind+1])
        lon_0=float(sys.argv[ind+2])
    if '-sym' in sys.argv:
        ind = sys.argv.index('-sym')
        sym=sys.argv[ind+1]
        symsize=int(sys.argv[ind+2])
    if '-pad' in sys.argv:
        ind = sys.argv.index('-pad')
        padlat=float(sys.argv[ind+1])
        padlon=float(sys.argv[ind+2])
    if '-f' in sys.argv:
        ind = sys.argv.index('-f')
        file=dir_path+'/'+sys.argv[ind+1]
        header=open(file,'r').readlines()[0].split('\t')
        if 'tab' in header[0]:
            proj='lcc'
            if 'sites' in header[1]:
                latkey='lat'
                lonkey='lon'
                namekey='site'
                lockey=''
            else:  
                print('file type not supported')
                print(main.__doc__)
                sys.exit()
            Sites,file_type=pmag.magic_read(file)
            Lats=pmag.get_dictkey(Sites,latkey,'f')
            Lons=pmag.get_dictkey(Sites,lonkey,'f')
            if prn_name==1:names=pmag.get_dictkey(Sites,namekey,'')
            if prn_loc==1:names=pmag.get_dictkey(Sites,lockey,'')
        else:
            ptdata=numpy.loadtxt(file)
            Lons=ptdata.transpose()[0]
            Lats=ptdata.transpose()[1]
        latmin=numpy.min(Lats)-padlat
        lonmin=numpy.min(Lons)-padlon
        latmax=numpy.max(Lats)+padlat
        lonmax=numpy.max(Lons)+padlon
        if lon_0=="":
            lon_0=0.5*(lonmin+lonmax)
            lat_0=0.5*(latmin+latmax)
    else:
        print("input file must be specified")
        sys.exit()
    if '-prj' in sys.argv:
        ind = sys.argv.index('-prj')
        proj=sys.argv[ind+1]
    FIG={'map':1}
    pmagplotlib.plot_init(FIG['map'],6,6)
    cnt=0
    Opts={'latmin':latmin,'latmax':latmax,'lonmin':lonmin,'lonmax':lonmax,'lat_0':lat_0,'lon_0':lon_0,'proj':proj,'sym':sym,'symsize':3,'pltgrid':1,'res':res,'boundinglat':0.,'padlon':padlon,'padlat':padlat,'gridspace':gridspace,'cmap':cmap}
    Opts['details']={}
    Opts['details']['coasts']=1
    Opts['details']['rivers']=rivers
    Opts['details']['states']=boundaries
    Opts['details']['countries']=boundaries
    Opts['details']['ocean']=ocean
    Opts['details']['fancy']=fancy
    if len(names)>0:Opts['names']=names
    if len(locs)>0:Opts['loc_name']=locs
    if proj=='merc':
        Opts['latmin']=-70
        Opts['latmax']=70
        Opts['lonmin']=-180
        Opts['lonmax']=180
    print('please wait to draw points')
    Opts['sym']=sym
    Opts['symsize']=symsize
    if basemap: 
        pmagplotlib.plot_map(FIG['map'],Lats,Lons,Opts)
    else:
        pmagplotlib.plot_map(FIG['map'],Lats,Lons,Opts)
    files={}
    titles={}
    titles['map']='PT Map'
    for key in list(FIG.keys()):
        files[key]='map_pts'+'.'+fmt
    if pmagplotlib.isServer:
        black     = '#000000'
        purple    = '#800080'
        FIG = pmagplotlib.add_borders(FIG,titles,black,purple)
        pmagplotlib.save_plots(FIG,files)
    if plot==1:
        pmagplotlib.save_plots(FIG,files)
    else:
        pmagplotlib.draw_figs(FIG)
        ans=input(" S[a]ve to save plot, Return to quit:  ")
        if ans=="a": pmagplotlib.save_plots(FIG,files)

if __name__ == "__main__":
    main()
