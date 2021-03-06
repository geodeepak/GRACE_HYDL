gfz_isdc_dealiasing_ftp.py
==========================

- Syncs GRACE Level-1b dealiasing products from the GFZ Information System and Data Center (ISDC)
- Optionally outputs as monthly tar files

#### Calling Sequence
```bash
python gfz_isdc_dealiasing_ftp.py --tar --directory <path_to_grace_directory> --release RL06
```
[Source code](https://github.com/tsutterley/read-GRACE-harmonics/blob/main/scripts/gfz_isdc_dealiasing_ftp.py)

#### Command Line Options
- `-D X`, `--directory X`: Working Data Directory
- `-r X`, `--release X`: GRACE/GRACE-FO Data Releases to sync (RL05,RL06)
- `-Y X`, `--year X`: Years of data to sync
- `-m X`, `--month X`: Months of data to sync
- `-T`, `--tar`: Output data as monthly tar files (.tar.gz or .tgz)
- `-t X`, `--timeout X`: Timeout in seconds for blocking operations
- `-C`, `--clobber`: Overwrite existing data in transfer
- `-l`, `--log`: Output log file
- `-M X`, `--mode X`: Permission mode of directories and files synced
