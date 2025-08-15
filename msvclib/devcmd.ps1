# PowerShell version of devcmd.bat
# Get the directory where this script is located
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path

# Display directory tree (equivalent to tree /f)
Get-ChildItem -Path $scriptDir -Recurse | Format-Table -Property Mode, LastWriteTime, Length, Name -AutoSize

Write-Host "success"
