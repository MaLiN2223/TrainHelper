$pythonScript = "code_check.py"

$directory = $args[0]
$extended = $args[1]
$filename = $args[2]

write-host $args
write-host "ARGUMENTS?"
if ($directory -eq " " -or $directory -eq "")
{
    $directory= "../../"
}

if ($filename -eq " "){
    $filename = ""
}

write-host "Configuration: "

if ($extended  -ne "s")
{
    write-host "Extended view enabled."
}
if($filename  -ne "")
{
    write-host "File dump is enabled, no output will be visible in console"
    $filename  = "../../docs/code_check/"+$filename
}
$type = "text"
if($filename -ne "" -and $filename  -ne " " -and $extended  -eq "f")
{
    write-host "Dumping as html"
    $filename  = $filename +".html"
    $type = "html"
}
elseif($filename  -ne "" -and $filename  -ne " ")
{
    write-host "Dumping as .txt"
    $args[2] = $args[2]+".txt"
}
write-host "Starting script"
python $pythonScript  $directory  $extended  $type $filename
write-host "All done"