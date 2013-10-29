drift 
================================================================================

gdp2nc4
--------------------------------------------------------------------------------

Transfers the ascii files containing the interpolated drifter trajectories from
the **G**lobal **D**rifter **P**rogram (GDP) **to** ragged arrays in a 
**n**et **C**DF-**4** file.

For an implementation of netCDF-4 for python see
<https://code.google.com/p/netcdf4-python/>.

How to obtain the ascii data:
<http://www.aoml.noaa.gov/envids/gld/FtpInterpolatedInstructions.php>


yomaha2nc4
--------------------------------------------------------------------------------

Convert the Yomaha07 data, contained in an ASCII table, to a netCDF4 file.
The output file will have a fixed dimension length, which reduces the required
disk space dramatically.
