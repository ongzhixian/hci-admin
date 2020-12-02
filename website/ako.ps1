# Script to run python application

# Local variables declaration
$script:cmdFinder = $null
$script:cmdSearchResults = $null
$script:cmdPath = $null

function script:Start-Python_Win32NT {
    $script:cmdFinder = "where.exe"

    $script:cmdSearchResults = Invoke-Expression "$script:cmdFinder python"

    if ($null -eq $script:cmdSearchResults) {
        Write-Host "Cannot find python commands."
        exit(0)
    }

    $script:cmdPath = $script:cmdSearchResults | Select-Object -First 1
    Write-Host "Using python from [$script:cmdPath]"

    $argList = "main.py"

    Start-Process $script:cmdPath -ArgumentList $argList -WorkingDirectory $(Get-Location)
    
}

function script:Start-Python {
    $script:cmdFinder = "which"
}

# Main script

if ($null -ne $connection) {
    Write-Host "Connection using port [$script:datastore_port] exists."
    Write-Host "This script uses this port; unable to continue. Terminating script."
    exit(0)
}

if ($PSVersionTable.Platform -ceq "Win32NT") {
    script:Start-Python_Win32NT
} else {
    script:Start-Python
}
