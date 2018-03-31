$clean = $args[0]
$coverage = $args[1]
$files = ".eggs","TrainHelper.egg-info",".cache", ".pytest_cache"
$dir = ".\"
$commands ="test"

$pythonScript = "setup.py"
if( -Not (Test-Path "$dir$pythonScript")){
   cd ..
}
write-host "Starting tests..."

#version choose
if($coverage -ne "no")
{
    write-host "Getting coverage "
    coverage erase
    python -m coverage run $pythonScript test
    write-host "Generating coverage HTML file..."
    coverage html
}
else
{
	write-host "Testing python 3"
	python $pythonScript $commands
}

#cleaning
if($clean -eq "yes")
{
    write-host "Removing tmp directories ..."
    foreach($file in $files){
        if(Test-Path "$dir$file"){
            Remove-Item -Force -Recurse "$dir$file"
        }
    }
    write-host "Clearing compiled python files ..."
    get-childitem ./ -include *.pyc -recurse | foreach ($_) {remove-item $_.fullname -recurse}
    get-childitem ./ -include *.egg -recurse | foreach ($_) {remove-item $_.fullname -recurse}
    get-childitem ./ -include __pycache__ -recurse | foreach ($_) {remove-item $_.fullname -recurse}
}
write-host "All done."