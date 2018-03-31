code_check.bat script checks code in project against plyint

code_check.bat usage:
-e [s/e/f] default: s
 Specifies how accurate output should be.
 s - simple, only what file is being checed and how it was rated
 e - extended, all from simple but shows information about errors and warnings
 f - shows full output

-f
 Specifies where raport shound be dumped, when no file provided output is being written to console

-d default ../
 Which directory should be tested

More info:
If file and full output are required whole raport is dumped as html.