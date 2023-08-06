# CYGNSS Library

CYGNSS Library is a Python package for working with CYGNSS data. The package can be used for downloading SRTM data. Please see How to use the package for more details.


## Installation
you can install it using `pip`.

```console
pip install -U cygnsslib
```
or you can clone the repository and install it using the following command
```console
pip install .  
```
To use it with anaconda, install the environment as follows:
```console
conda create -n cygnss  
source activate cygnss  
conda install -c conda-forge --files requiremnts.txt
```
You can then remove the local copy if you wish. Alternatively, if you wish to be able to make changes to your local copy without having to reinstall the package for the changes to take effect (e.g., for development purposes), you can use the following instead:
```console
pip uninstall cygnsslib
```
### Required packages
Here the required Python packages:
```console
gdal geographiclib lxml matplotlib netcdf4 numpy openpyxl pandas pbkdf2 pycrypto requests tqdm
```
Note: `gdal` can be installed using conda   
```console
conda install -c conda-forge gdal
```
or using [this method](https://mothergeo-py.readthedocs.io/en/latest/development/how-to/gdal-ubuntu-pkg.html) in Ubuntu  
## How to Use The Package
The cygnsslib has several modules:  
1. Identify CYGNSS DDMs within a specific region  
2. Group DDMs within a specific distance  
3. Download CYGNSS antenna pattern  
4. CygDdmId Class, which work as CYGNSS DDM ID  
5. Download CYGNSS data from PO.DAAC  
6. Download SRTM data from NASA Earth Data
7. Other functionality related to CYGNSS data  
  
For most of the library, you need to set the environment variable ``CYGNSS_L1_PATH`` to the path of the CYGNSS L1 data. i.e.
```console 
CYGNSS_L1_PATH=/cygnss_data/L1/v3.0
```
Note the folder needs to be named as the version (e.g. `v3.0`)name in PODAAC, and the parent folder need to be `L1`
You can set the environment variable for the session in python as follows:
```python
import os
os.environ['CYGNSS_L1_PATH'] = '/cygnss_data/L1/v3.0'
```

For SRTM you can specify the main path by specifying the environment variable ``SRTM_PATH``. The files will be saved in `SRTM_PATH\hgt`
### Identify CYGNSS DDMs within a specific region

There are several ways to find the DDM within a region.  
1. find all the DDMs that their SP location within a specific distance from a specific location.  
2. find all the DDMs that their SP location is within the polygon in the specified kml file.  

Below an example of the usage:  
```python
import cygnsslib
import numpy as np
import datetime as dt

cygnss_l1_path = None  # this will make the strip get the path from os.environ["CYGNSS_L1_PATH"]
year = 2019
days_list = np.arange(1,100)
ref_pos = [37.1906, -105.9921] #  [lat,long]
radius = 10e3 # [m]
thesh_ddm_snr = 3.0 # split DDMs into above thesh_ddm_snr and below thesh_ddm_snr. Above this value the DDM image will be saved
thesh_noise = 1  # noise threshold, each pixel in the DDM below this value will be replaced by this value
kml_out_tag = f'my_data' # tag for all the output files, ex: my_data_above_thresh.kml
save_podaac_pass = True  # if True and download_cygnss_data is True the PO DAAC username/password will be saved
# The default options are: 
options = {'save_cvs': False, 
           'save_ddm_img': True, 
           'plt_tag': '',
           'title_img_inc_ddm_time': False,
           'img_save_type': ['png'],
           'sheet_type': 'xls'} 

cygnsslib.write_sp_within_radius(cygnss_l1_path, year=2019, daylist=days_list, ref_pos=ref_pos, 
                                 radius=radius, out_root=kml_out_tag, thresh_ddm_snr=thesh_ddm_snr, 
                                 thresh_noise=thesh_noise, download_cygnss_data=True, 
                                 out_options=options, save_podaac_pass=save_podaac_pass)

start_date = dt.date(year=2019,month=1,day=1)
end_date = dt.date(year=2019,month=6,day=10)  # the end date included in the search
cygnsslib.write_sp_within_radius_between_dates(cygnss_l1_path,start_date, end_date, ref_pos=ref_pos, 
                                               radius=radius, out_root=kml_out_tag, thresh_ddm_snr=thesh_ddm_snr,
                                               thresh_noise=thesh_noise, download_cygnss_data=True,
                                               out_options=options, save_podaac_pass=save_podaac_pass)

in_kml = f'my_poly.kml'
cygnsslib.write_sp_from_kml(cygnss_l1_path, year, days_list, in_kml=in_kml, out_root=kml_out_tag,
                            thresh_ddm_snr=thesh_ddm_snr, thresh_noise=thesh_noise, download_cygnss_data=True,
                            out_options=options, save_podaac_pass=save_podaac_pass)
cygnsslib.write_sp_from_kml_between_dates(cygnss_l1_path, start_date, end_date, in_kml=in_kml, out_root=kml_out_tag,
                            thresh_ddm_snr=thesh_ddm_snr, thresh_noise=thesh_noise, download_cygnss_data=True,
                            out_options=options, save_podaac_pass=save_podaac_pass)
```
### Group DDMs within a specific distance

This will group DDMs within specific distance in one group. The kml file need to be the output of `write_sp_from_kml()` or `write_sp_within_radius_between_dates()` or `write_sp_from_kml()` or `write_sp_from_kml_between_dates()`  
This function need to be used after identifying the DDMs within a specific region
```python
import cygnsslib
in_kml = f'my_data_above_thresh.kml'
max_dist = 1e3
out_kml = f'{in_kml[:-4]}_grp{max_dist:d}'
cygnsslib.group_sp_within_distance(in_kml, out_kml, max_dist, save_cvs=True, sheet_type=f'xls')
```

### Download CYGNSS antenna pattern
This function will download cygnss antenna patterns

```python
import cygnsslib
antenna_patterns_folder_path = f'/data/cygnss_antenna_patterns'
cygnsslib.download_cyg_antenna_patterns(antenna_patterns_folder_path)
```

### CygDdmId Class  
The ``CygDdmId`` class is basically work as an ID for the DDMs, with some features.  
There are multiple static functions, which are 
1. `get_land_prod_info_from_ocean_prod()`  
2. `find_cygnss_file()`  
3. `get_sample_id_from_time_rltv_tcs()`  
4. `cyg_id_list_from_kml()`  

The function `cyg_id_list_from_kml()` generate a list of objects of `CygDdmId` from a kml file. The kml file from  The kml file need to be the output of `write_sp_from_kml()` or `write_sp_within_radius_between_dates()` or `write_sp_from_kml()` or `write_sp_from_kml_between_dates()`

#### Input parameters
THe input parameters are:  
1. `file_name` [req]: `None` or the file name. It's better to set it to `None`.  
2. `year` [req]: data year  
3. `day` [req]: day of the year  
4. `sc_num` [req]: spacecraft id, (1-8)  
5. `ch_id` [req]: channel id (1-4)  
6. `samp_id` [req]: sample id (zero-based)  
7. `land_samp_id` [optional]: sample id of the land product (zero-based)  
8. `sample_time_sec` [optional]: time (in seconds) of the selected DDM (sample) from the beginning of the day  
9. `land_file_name` [optional]: land product file name  
10. `ddm_tag` [optional]: DDM tag  
   

### Methods 
The current implemented methods are:  
1. `set_land_sample_id()`: set `land_samp_id`  
2. `set_ddm_time()`: set `sample_time_sec`  
3. `set_land_file_name()`: set `land_file_name`  
4. `fill_file_name()`: fill file name automatically  
5. `fill_land_parameters()`: fill land product parameters, which are `land_file_name`, `land_samp_id` and `sample_time_sec`  
6. `get_utc_time()`: return DDM time  

### Examples  
There are many usage for this class here few   

```python
from cygnsslib import CygDdmId
year = 2019
day = 123
sc_num = 2
ch_id = 3
sample_id = 440
cyg_ddm_id = CygDdmId.CygDdmId(None, year, day, sc_num, ch_id, sample_id)
```
   

```python
from cygnsslib import CygDdmId

in_kml = f'my_data_above_thresh.kml'
cyg_ddmid_list = CygDdmId.cyg_id_list_from_kml(in_kml)
for cyg_ddmid in cyg_ddmid_list:
    cyg_ddmid.fill_file_name()
    cyg_ddmid.fill_land_parameters(l1_land_folder_name=f'v3Land')
```

### Download CYGNSS data from PO.DAAC

You can download both the standard DDMs and the rawif data. You can choose to download data between two dates or a list of days in the year.  
If a file exists, the code will not re-download it.  
Note if you select `check_md5_exist_file=True`, then the code will do an md5 check for existing files. This will ensure existing files are good. However, this will make it very slow.

Below an example of downloading DDMs and the rawif files. The files will be organized as they're in PODAAC.
```python
from cygnsslib import cygnss_download
import datetime as dt
import numpy as np

# Download data in the same year and range of days
days_list = np.arange(5, 10)
data_year = 2020
# list_sc_num = [3]
list_sc_num = None  # Will download all the 8 spacecrafts 
cyg_data_ver = f'v3.0'
cygnss_download.download_cyg_files(data_year, days_list, list_sc_num=list_sc_num, cyg_data_ver=cyg_data_ver, 
                                   check_md5_exist_file=False, cyg_data_lvl=f'L1', save_podaac_pass=True)
# Downloading data between two dates (including end date)
st_date = dt.date(year=2019, month=1, day=12)
end_date = dt.date(year=2020, month=1, day=3)

cygnss_download.download_cyg_files_between_date(st_date, end_date, list_sc_num=list_sc_num, cyg_data_ver=cyg_data_ver, 
                                                check_md5_exist_file=False, cyg_data_lvl=f'L1', save_podaac_pass=True)

# Downloading rawif data 
download_l1_data = True  # This will download the corresponding L1 data
cygnss_download.download_cyg_rawif_files(data_year,days_list, list_sc_num, save_podaac_pass=True, 
                                         download_l1_data=download_l1_data)
cygnss_download.download_rawif_cyg_files_between_date(st_date,end_date, list_sc_num, save_podaac_pass=True, 
                                                      download_l1_data=download_l1_data)

```
#### PODAAC user/pass related notes
You can get the PO.DAAC Drive API Credentials from https://podaac-tools.jpl.nasa.gov/drive/  
If you entered the wrong PODAAC user/pass, you'll be asked to re-enter them again. However, you need to re-start the code after that so the saved user/pass are loaded again.  

You can reset your PODAAC user/pass and enter new user/pass using the following code. Note when you run the code, you'll be asked to enter the new user/pass  

Note: if you want to remove the current user/pass, set `save_pass=False`  
```python
from cygnsslib import cygnss_download

cygnss_download.get_podaac_cred(save_pass=True, reset_pass=True) 
```

### Download SRTM data from NASA Earth Data
The files are in this URL: https://e4ftl01.cr.usgs.gov/MEASURES/SRTMGL1.003/2000.02.11/  
The username/password can be obtained from https://urs.earthdata.nasa.gov/home  

```python
from cygnsslib import srtm_download
import os
os.environ['SRTM_PATH'] = '/data/srtm_data'  # The files will be downloaded into SRTM_PATH/hgt path
files_lat = [21, 22, 20]
files_lon = [29, 30]
srtm_download.download_srtm_ght_files(files_lat, files_lon, save_pass=True, unzipfile=False, remove_zippedfile=True)  


```
#### EarthData username and pass related notes  
You can reset your EarthData user/pass and enter new user/pass using the following code. Note when you run the code, you'll be asked to enter the new user/pass  
```python
from cygnsslib import srtm_download

srtm_download.get_earthdata_cred(save_pass=True, reset_pass=True) 
```
### Other functionality related to CYGNSS data   

Create a circle or a square on the ground and export it to kml file  
```python
import cygnsslib
ref_pos = [37.1906, -105.9921] #  [lat,long]
radius = 10e3 # [m]
out_kml = f'my_circle.kml'
cygnsslib.create_centered_polygon(ref_pos, radius, out_kml, shape=f"circle")
```
Create a kml file from a list of positions  
```python
import cygnsslib
import numpy as np
lyr_name = f"my_pos"
point_names = ["Y1", "Y2", "Y3"]
loc_list = np.array([[-34.0, 145.0], [-34.0, 146.0], [-34.0, 148]])
out_kml = f"my_pos.kml"
cygnsslib.create_kml_from_list_points(loc_list, loc_names=point_names, out_kml=out_kml, lyr_name=lyr_name)
```

Get DDMs info from the kml file. The kml file need to be the output of `write_sp_from_kml()` or `write_sp_within_radius_between_dates()` or `write_sp_from_kml()` or `write_sp_from_kml_between_dates()`
The main goal of this function is extract the DDMs' parameters from the kml file. See ``CygDdmId`` Class for more functionality
```python
import cygnsslib

ddm_list = cygnsslib.get_list_ddm_info_from_kml(in_kml=f'my_data_above_thresh.kml')

```
Find CYGNSS Land product (experimental) from the standard ocean product. This function is still in developing.
```python
import cygnsslib
xls_in = f'my_xls.xlsx'
cygnsslib.find_land_prod_sample_id_from_excel(xls_in, xls_out=None, start_col=1, st_row=1)
```

## Contact Info  
For more info, please contact:   
Amer Melebari   
Microwave Systems, Sensors and Imaging Lab (MiXiL)  
University of Southern California  
amelebar[AT]usc.edu  