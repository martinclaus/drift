"""
drift -- deal with trajectories

"""

import numpy as np
import netCDF4 as nc
import datetime as dt
import time as tm

def gdp2nc4(finame, fmname, foname):
    """Put drifter data to a netCDF4 file.

    ATTENTION: For now, the file foname will be overwritten.

    finame : full path to the input file

    fmname : full path to the metadata file
    
    foname : full path to the output file

    """

    #=====================================================================
    # Set up the output file
    #=====================================================================
    #==========================================================

    # create the out-file
    fo = nc.Dataset(foname, 'w', format='NETCDF4', clobber=True)

    # create dims and vlan data type
    fo.createDimension('buoycount', size=None)
    fo.createVariable('buoycount', np.int64, 'buoycount')
    float64vl = fo.createVLType(np.float64, 'float64vl')

    # create the variables 
    # first all those that are part of the actual data set
    aomlid_v = fo.createVariable('aomlid', np.int64, 'buoycount')
    aomlid_v.long_name = 'AOML buoy identification number (PKey)'

    time_v = fo.createVariable('time', float64vl, 'buoycount')
    time_v.long_name = 'time stamp'
    time_v.units = 'days since 1980-01-01 00:00:00'

    lat_v = fo.createVariable('lat', float64vl, 'buoycount')
    lat_v.long_name = 'latitude (-90,90)'
    lat_v.units = 'degrees north'

    lon_v = fo.createVariable('lon', float64vl, 'buoycount')
    lon_v.long_name = 'longitude (-180, 180)'
    lon_v.units = 'degrees east'

    temp_v = fo.createVariable('temp', float64vl, 'buoycount')
    temp_v.long_name = 'temperature'
    temp_v.units = 'deg C'

    u_v = fo.createVariable('u', float64vl, 'buoycount')
    u_v.long_name = 'eastward velocity'
    u_v.units = 'cm/s'

    v_v = fo.createVariable('v', float64vl, 'buoycount')
    v_v.long_name = 'northward velocity'
    v_v.units = 'cm/s'

    speed_v = fo.createVariable('speed', float64vl, 'buoycount')
    speed_v.long_name = 'modulus of (u,v)'
    speed_v.units = 'cm/s'

    varlat_v = fo.createVariable('varlat', float64vl, 'buoycount')
    varlat_v.long_name = 'variance of the latitude'
    varlat_v.units = 'degrees**2'

    varlon_v = fo.createVariable('varlon', float64vl, 'buoycount')
    varlon_v.long_name = 'variance of the longitude'
    varlon_v.units = 'degrees**2'

    vartemp_v = fo.createVariable('vartemp', float64vl, 'buoycount')
    vartemp_v.long_name = 'variance of the temperature'
    vartemp_v.units = 'K**2'

    # create the variables 
    # then the metadata
    deptime_v = fo.createVariable('deptime', np.float64, 'buoycount')
    deptime_v.long_name = 'deployment time stamp'
    deptime_v.units = 'days since 1980-01-01 00:00:00'

    deplat_v = fo.createVariable('deplat', np.float64, 'buoycount')
    deplat_v.long_name = 'deployment latitude (-90,90)'
    deplat_v.units = 'degrees north'

    deplon_v = fo.createVariable('deplon', np.float64, 'buoycount')
    deplon_v.long_name = 'deployment longitude (-180, 180)'
    deplon_v.units = 'degrees east'

    endtime_v = fo.createVariable('endtime', np.float64, 'buoycount')
    endtime_v.long_name = 'end time stamp'
    endtime_v.units = 'days since 1980-01-01 00:00:00'

    endlat_v = fo.createVariable('endlat', np.float64, 'buoycount')
    endlat_v.long_name = 'end latitude (-90,90)'
    endlat_v.units = 'degrees north'

    endlon_v = fo.createVariable('endlon', np.float64, 'buoycount')
    endlon_v.long_name = 'end longitude (-180, 180)'
    endlon_v.units = 'degrees east'

    dltime_v = fo.createVariable('dltime', np.float64, 'buoycount')
    dltime_v.long_name = 'drogue lost time stamp'
    dltime_v.units = 'days since 1980-01-01 00:00:00'

    # global attributes
    fo.history = 'created by drift.gdp2nc2 on ' + tm.ctime(tm.time())
    fo.source  = 'from ' + finame + " and " + fmname

    #=====================================================================
    # set up the input file and the metadata file
    #=====================================================================

    fi = open(finame, 'r')

    fm = open(fmname, 'r')

    #=====================================================================
    # get all the metadata (< 1MB)
    #=====================================================================

    #=====================================================================
    # get and put the data
    #=====================================================================

    # For each aomlid, get the whole trajectory and put it into the netCDF4
    # file.

    # initalize with aomlid = 0 and empty fields

    # while reading line by line:
        # if the aomlid changed or end of file (empty line)
            # put the fields to the netCDF4 file
            # put the relevant metadata as well
            # empty fields
        # if end of file
            # break the loop 
        # continue accumulating the fields
    
    #=====================================================================
    # clean up
    #=====================================================================

    # close the output file
    fo.close()

    # close the input file
    fi.close()

    # close the metadata file

    return None
