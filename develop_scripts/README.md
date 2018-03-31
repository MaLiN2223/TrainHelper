test.bat executes all tests
assuming there is existing python variable pointing to python.exe  
-nc
 with this switch script does not clean temporary files
-cov
 generates coverage files, if no python version is specified coverage is being generated for both versions and merged

Example:
test.bat -nc
will test and not clean afterwards

test.bat -cov -nc
will generate coverage and will not clean temp files

test.bat -cov
will generate coverage and will clean temp files
