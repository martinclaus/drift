"""
drift -- deal with trajectories

"""

import numpy as np
import netCDF4 as nc
import time as tm

def gdp2nc4(finame, fmname, foname):
    """Put drifter data to a netCDF4 file.

    ATTENTION: For now, the file foname will be overwritten.

    finame : full path to the input file

    fmname : full path to the metadata file
    
    foname : full path to the output file

    """
    tic = tm.time()

    print "gdp2nc4"
    print "working with"
    print finame
    print fmname
    print foname

    #=====================================================================
    # Set up the output file
    #=====================================================================

    # create the out-file
    fo = nc.Dataset(foname, 'w', format='NETCDF4', clobber=True)

    # create dims and vlan data type
    fo.createDimension('buoycount', size=None)
    buoycount_v = fo.createVariable('buoycount', np.int64, 'buoycount')
    float64vl = fo.createVLType(np.float64, 'float64vl')

    # create the variables: data
    aomlid_v = fo.createVariable('aomlid', np.int64, 'buoycount')
    aomlid_v.long_name = 'AOML buoy identification number (PKey)'

    time_v = fo.createVariable('time', float64vl, 'buoycount')
    time_v.long_name = 'time stamp'
    time_v.units = 'seconds since 1980-01-01 00:00:00'

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

    # create the variables : metadata
    deptime_v = fo.createVariable('deptime', np.float64, 'buoycount')
    deptime_v.long_name = 'deployment time stamp'
    deptime_v.units = 'seconds since 1980-01-01 00:00:00'

    deplat_v = fo.createVariable('deplat', np.float64, 'buoycount')
    deplat_v.long_name = 'deployment latitude (-90,90)'
    deplat_v.units = 'degrees north'

    deplon_v = fo.createVariable('deplon', np.float64, 'buoycount')
    deplon_v.long_name = 'deployment longitude (-180, 180)'
    deplon_v.units = 'degrees east'

    endtime_v = fo.createVariable('endtime', np.float64, 'buoycount')
    endtime_v.long_name = 'end time stamp'
    endtime_v.units = 'seconds since 1980-01-01 00:00:00'

    endlat_v = fo.createVariable('endlat', np.float64, 'buoycount')
    endlat_v.long_name = 'end latitude (-90,90)'
    endlat_v.units = 'degrees north'

    endlon_v = fo.createVariable('endlon', np.float64, 'buoycount')
    endlon_v.long_name = 'end longitude (-180, 180)'
    endlon_v.units = 'degrees east'

    dltime_v = fo.createVariable('dltime', np.float64, 'buoycount')
    dltime_v.long_name = 'drogue lost time stamp'
    dltime_v.units = 'seconds since 1980-01-01 00:00:00'

    # global attributes
    fo.history = 'created by drift.gdp2nc2 on ' + tm.ctime(tm.time())
    fo.source  = 'from ' + finame + " and " + fmname

    #=====================================================================
    # get all the metadata (< 1MB)
    #=====================================================================

    print "get metadata ..."

    fm = open(fmname, 'r')

    # get line by line and put into arrays
    aomlid_m  = np.empty(0, np.int64)
    deptime_m = np.empty(0, np.float64)
    deplat_m  = np.empty(0, np.float64)
    deplon_m  = np.empty(0, np.float64)
    endtime_m = np.empty(0, np.float64)
    endlat_m  = np.empty(0, np.float64)
    endlon_m  = np.empty(0, np.float64)
    dltime_m  = np.empty(0, np.float64)
    reftime = tm.mktime(tm.strptime('1980/01/01 00:00', '%Y/%m/%d %H:%M')) 
    n = 0
    while True:
        lm = fm.readline()
        if lm == '': break
        n += 1
        mdata = lm.split()
        aomlid_m  = np.append(aomlid_m, np.int(mdata[0]))
        deplat_m  = np.append(deplat_m, np.float(mdata[6]))
        deplon_m  = np.append(deplon_m, np.float(mdata[7]))
        endlat_m  = np.append(endlat_m, np.float(mdata[10]))
        endlon_m  = np.append(endlon_m, np.float(mdata[11]))
        deptime_m = np.append(deptime_m, ( \
              tm.mktime(tm.strptime(mdata[4] + ' ' + mdata[5], '%Y/%m/%d %H:%M')) \
              - reftime))
        endtime_m = np.append(endtime_m, ( \
              tm.mktime(tm.strptime(mdata[8] + ' ' + mdata[9], '%Y/%m/%d %H:%M')) \
              - reftime))
        if mdata[12] == '0000/00/00':      
            dltime_m = np.append(dltime_m, np.NaN)
        else:    
            dltime_m = np.append(dltime_m, ( \
                  tm.mktime(tm.strptime(mdata[12] + ' ' + mdata[13], '%Y/%m/%d %H:%M')) \
                  - reftime))
    fm.close()      

    print "... done after %  12.6f seconds" % (tm.time() - tic)

    #=====================================================================
    # get and put the data
    #=====================================================================

    print "get data ..."

    fi = open(finame, 'r')

    # For each aomlid, get the whole trajectory and put it into the netCDF4
    # file.

    # empty fields
    time    = np.empty(0, np.float64)
    lat     = np.empty(0, np.float64)
    lon     = np.empty(0, np.float64)
    temp    = np.empty(0, np.float64)
    u       = np.empty(0, np.float64)
    v       = np.empty(0, np.float64)
    speed   = np.empty(0, np.float64)
    varlat  = np.empty(0, np.float64)
    varlon  = np.empty(0, np.float64)
    vartemp = np.empty(0, np.float64)
    aomlid = 0

    n = 0;
    while True:

        # get next line
        li = fi.readline()

        # if file ended (li empty) and buffers are written (aomlid is zero): finish
        if (li == '') and (aomlid == 0): break

        # if not end of file but all buffers are written: start new trajectory with aomlid
        if (li != '') and (aomlid == 0): aomlid = int(li.split()[0])

        # if not end of file and aomlid still valid: continue to fill buffers,
        # else: put to disk and start over
        if (li != '') and (aomlid == int(li.split()[0])):
            idata = li.split()
            time = np.append(time, \
              tm.mktime(tm.strptime(idata[3]+idata[1].zfill(2)+'01 00:00', '%Y%m%d %H:%M')) \
              + (float(idata[2]) - 1.0) * 24 * 3600 \
              - reftime)
            lat     = np.append(lat,     float(idata[4]))
            lon     = np.append(lon,     float(idata[5]))
            temp    = np.append(temp,    float(idata[6]))
            u       = np.append(u,       float(idata[7]))
            v       = np.append(v,       float(idata[8]))
            speed   = np.append(speed,   float(idata[8]))
            varlat  = np.append(varlat,  float(idata[9]))
            varlon  = np.append(varlon,  float(idata[10]))
            vartemp = np.append(vartemp, float(idata[11]))

        else:
            # replace NaN for missing value (999.999)
            temp[temp==999.999] = np.NaN
            u[u==999.999] = np.NaN
            v[v==999.999] = np.NaN
            speed[speed==999.999] = np.NaN
            varlat[varlat==999.999] = np.NaN
            varlon[varlon==999.999] = np.NaN
            vartemp[vartemp==999.999] = np.NaN

            # put data
            buoycount_v[n] = n
            aomlid_v[n]  = aomlid
            time_v[n]    = time
            lat_v[n]     = lat
            lon_v[n]     = lon
            u_v[n]       = u
            v_v[n]       = v
            speed_v[n]   = speed
            temp_v[n]    = temp
            varlat_v[n]  = varlat
            varlon_v[n]  = varlon
            vartemp_v[n] = vartemp

            # put metadata
            mindex = (aomlid_m == aomlid)
            deptime_v[n] = deptime_m[mindex]
            deplat_v[n]  = deplat_m[mindex]
            deplon_v[n]  = deplon_m[mindex]
            endtime_v[n] = endtime_m[mindex]
            endlat_v[n]  = endlat_m[mindex]
            endlon_v[n]  = endlon_m[mindex]
            dltime_v[n]  = dltime_m[mindex]

            # empty arrays
            time    = np.empty(0, np.float64)
            lat     = np.empty(0, np.float64)
            lon     = np.empty(0, np.float64)
            temp    = np.empty(0, np.float64)
            u       = np.empty(0, np.float64)
            v       = np.empty(0, np.float64)
            speed   = np.empty(0, np.float64)
            varlat  = np.empty(0, np.float64)
            varlon  = np.empty(0, np.float64)
            vartemp = np.empty(0, np.float64)

            # status report
            print "... done for aomlid = % 9d (n=% 6d) after % 12.6f seconds" \
              % (aomlid, n, tm.time() - tic)

            # reset buoy id  
            aomlid = 0
            n += 1
    
    #=====================================================================
    # clean up
    #=====================================================================

    # close the output file
    fo.close()

    # close the input file
    fi.close()

    print "gdp2nc4 done after % 12.6f seconds" % (tm.time() - tic)

    return None
