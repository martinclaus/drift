#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 25 12:07:13 2013

@author: Martin Claus

Note: Although this script is contained in the drift package, it is actually
not dealing with drifter trajectories. However, the Yomaha07 dataset is
composed from information of the ARGO float project.
"""
import numpy as np
import netCDF4 as nc
import time as tm
import sys
import getopt


def yomaha2nc4(finame, foname, line_buffer=100000, zlib=False):
    """
    Put the Yomoaha07 estimates of deep and surface velocities into a netcdf 4
    file. For a description of Yomaha07 and access to it, see
    http://apdrc.soest.hawaii.edu/projects/yomaha/index.php.

    finame : full path to the input file

    foname : full path to the output file
    """

    MISS_OUT = -999

    tic = tm.time()

    print "yomaha2nc4"
    print "working with"
    print finame
    print foname

    #=====================================================================
    # Set up the metadata
    #=====================================================================

    missing = ['-999.9999' if i in [0, 8, 15, 18, 21]
          else '-99.9999' if i in [1, 9, 16, 19, 22]
          else '-999.999' if i in [3, 10, 17, 20, 23]
          else '-999.9' if i == 2
          else '-999.99' if i in [4, 5, 6, 7, 11, 12, 13, 14]
          else '-128' if i == 27
          else '-999'
          for i in range(28)]

    variables = [
        {'name': 'x_deep',
         'unit': 'degrees_east',
         'long_name': 'Longitude'},
        {'name': 'y_deep',
         'unit': 'degrees_north',
         'long_name': 'Latitude'},
        {'name': 'z_park',
         'unit': 'dbar',
         'long_name': 'Parking Pressure'},
        {'name': 't_deep',
         'unit': 'days since 2000-01-01 0:0:0 UTC',
         'long_name': 'Time'},
        {'name': 'u_deep',
         'unit': 'cm/s',
         'long_name': 'Estimate of zonal deep velocity'},
        {'name': 'v_depth',
         'unit': 'cm/s',
         'long_name': 'Estimate of meridional deep velocity'},
        {'name': 'e_u_deep',
         'unit': 'cm/s',
         'long_name': 'Estimate of error of zonal deep velocity'},
        {'name': 'e_v_deep',
         'unit': 'cm/s',
         'long_name': 'Estimate of error of meridional deep velocity'},
        {'name': 'x_surf',
         'unit': 'degrees_east',
         'long_name': 'Longitude'},
        {'name': 'y_surf',
         'unit': 'degrees_north',
         'long_name': 'Latitude'},
        {'name': 't_surf',
         'unit': 'days since 2000-01-01 0:0:0 UTC',
         'long_name': 'Time'},
        {'name': 'u_surf',
         'unit': 'cm/s',
         'long_name': 'Estimate of zonal velocity at sea surface'},
        {'name': 'v_surf',
         'unit': 'cm/s',
         'long_name': 'Estimate of meridional velocity at sea surface'},
        {'name': 'e_u_surf',
         'unit': 'cm/s',
         'long_name': 'Estimate of error of zonal velocity at sea surface'},
        {'name': 'e_v_surf',
         'unit': 'cm/s',
         'long_name': 'Estimate of error of meridional velocity at sea surface'},
        {'name': 'x_last_prev',
         'unit': 'degrees_east',
         'long_name': 'Longitude of the last fix at the surface during previous cycle'},
        {'name': 'y_last_prev',
         'unit': 'degrees_north',
         'long_name': 'Latitude of the last fix at the surface during previous cycle'},
        {'name': 't_last_prev',
         'unit': 'days since 2000-01-01 0:0:0 UTC',
         'long_name': 'Time of the last fix at the surface during previous cycle'},
        {'name': 'x_first',
         'unit': 'degrees_east',
         'long_name': 'Longitude of the first fix at the surface'},
        {'name': 'y_first',
         'unit': 'degrees_north',
         'long_name': 'Latitude of the first fix at the surface'},
        {'name': 't_first',
         'unit': 'days since 2000-01-01 0:0:0 UTC',
         'long_name': 'Time of the first fix at the surface'},
        {'name': 'x_last',
         'unit': 'degrees_east',
         'long_name': 'Longitude of the last fix at the surface'},
        {'name': 'y_last',
         'unit': 'degrees_north',
         'long_name': 'Latitude of the last fix at the surface'},
        {'name': 't_last',
         'unit': 'days since 2000-01-01 0:0:0 UTC',
         'long_name': 'Time of the last fix at the surface'},
        {'name': 'n_fix',
         'unit': '',
         'long_name': 'Number of surface fixes'},
        {'name': 'float_id',
         'unit': '',
         'long_name': 'Float ID'},
        {'name': 'n_cycle',
         'unit': '',
         'long_name': 'Cycle number'},
        {'name': 'inv_flag',
         'unit': '',
         'long_name': 'Time inversion/duplication flag'},
    ]

    dtype = [np.int32 if i in [24, 25, 26]
       else np.byte if i == 27
       else np.float32
       for i in range(28)]

    #=====================================================================
    # Set up the output file
    #=====================================================================
    var = []

    # get file length
    length = 0
    with open(finame, 'r') as fi:
        for line in fi:
            length += 1

    # create the out-file
    fo = nc.Dataset(foname, mode='w', format='NETCDF4', clobber=True)

    # create dims and vlan data type
    fo.createDimension('id', size=length)
    id_v = fo.createVariable('id', np.int64, 'id',
                             zlib=zlib, fill_value=MISS_OUT)
    id_v[:] = range(1, length + 1)

    for i in range(len(variables)):
        v_dict = variables[i]
        v_obj = fo.createVariable(v_dict['name'], dtype[i], 'id', zlib=zlib,
                                  fill_value=missing[i])
        v_obj.units = v_dict['unit']
        v_obj.long_name = v_dict['long_name']
        var.append(v_obj)

    #=====================================================================
    # read and write the data
    #=====================================================================
    buf = [[] for i in range(len(variables))]
    idx = 0
    with open(finame, 'r') as fi:
        old_idx = idx
        for line in fi:
            idx += 1
            line = line.strip()
            [buf[i].append(dtype[i](val)) if val != missing[i]
                else buf[i].append(dtype[i](MISS_OUT))
                for i, val in enumerate(line.split())]
            # write chunk to disk and clear buffer
            if np.mod(idx, line_buffer) == 0:
#                id_v[old_idx:idx-1] = range(old_idx + 1,
#                                       len(buf[i][:]) + old_idx + 1)
                for i in range(len(variables)):
                    var[i][old_idx:idx] = np.ma.array(
                                            buf[i],
                                            mask=[val == dtype[i](MISS_OUT)
                                                  for val in buf[i]])

                old_idx = idx
                buf = [[] for i in range(len(variables))]
        # write last peace to file
        if old_idx != idx:
#            id_v[old_idx:idx - 1] = range(old_idx + 1, len(buf[i][:]) + old_idx + 1)
            for i in range(len(variables)):
                var[i][old_idx:idx] = np.ma.array(buf[i],
                                               mask=[val == dtype[i](MISS_OUT)
                                                   for val in buf[i]])

    #=====================================================================
    # clean up and finish
    #=====================================================================
    fo.close()
    print "yomaha2nc4 done after % 12.6f seconds" % (tm.time() - tic)

    return None

# Script execution block
if __name__ == "__main__":
    usage = """
usage: yomaha2nc4.py [-h -z -l<n_line_buffer> --help --line_buffer=N --zlib] <infile> <outfile>

-h, --help:                 print this message

-z, --zlib:                 enables gzip compression of the output file

-l<N> --line_buffer=<N>:    Number of records to hold in memory
"""
    try:
        opts, args = getopt.gnu_getopt(sys.argv[1:],
                                       "hzl:",
                                       ['line_buffer=', 'zlib', 'help'])
        in_args = {}
        for opt, arg in opts:
            if opt in ('-l', '--line_buffer'):
                in_args['line_buffer'] = int(arg)
            elif opt in ('-z', '--zlib'):
                in_args['zlib'] = True
            elif opt in ('h', '--help'):
                raise getopt.GetoptError('')
        if len(args) != 2:
            raise getopt.GetoptError('')

    except getopt.GetoptError:
        print usage
        sys.exit(2)
    except ValueError:
        print "Line buffer must be an integer"
        sys.exit(2)

    yomaha2nc4(*args, **in_args)
