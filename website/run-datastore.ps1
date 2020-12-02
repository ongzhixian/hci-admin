# Script to run Google Cloud Datastore Emulator

# Local variables declaration
$script:cmdFinder = $null
$script:gcloudSearchResults = $null
$script:gcloudPath = $null

$script:datastore_timeout = 5
$script:gcloudComponent = "beta emulators datastore"
$script:datastore_data_dir = "D:\data\datastore"
$script:datastore_host = "localhost"
$script:datastore_port = "38089"



function script:Start-Datastore_Win32NT {

    # Find location of gcloud command using where.exe (Windows) or which (MacOS/Linux)
    # Use where.exe on Windows otherwise use which

    $script:cmdFinder = "where.exe"

    # Now that we have cmdFinder, find the location of gcloud command

    $script:gcloudSearchResults = Invoke-Expression "$script:cmdFinder gcloud"

    if ($null -eq $script:gcloudSearchResults) {
        Write-Host "Cannot find gcloud commands."
        exit(0)
    }

    # $gcloudSearchResults should return multiple lines like the below; 
    # We need to find the most compatible one to use based on Platform
    # C:\Apps\Google\CloudSDK\google-cloud-sdk\bin\gcloud
    # C:\Apps\Google\CloudSDK\google-cloud-sdk\bin\gcloud.cmd

    $script:gcloudPath = $script:gcloudSearchResults | Where-Object {$_ -like "*.cmd" }

    if ($null -eq $script:gcloudPath) {
        Write-Host "Compatible gcloud command not found."
        exit(0)
    }

    # Finally, we are ready to spin up Gcloud Datastore Emulator in new window
    # Full command looks like the below:
    # "gcloud beta emulators datastore start --data-dir=D:\data\datastore --host-port=localhost:38089"

    #Start-Process $script:gcloudPath -ArgumentList "$script:gcloudComponent start --data-dir=$script:datastore_data_dir --host-port=$script:datastore_host:$script:datastore_port"
    $argList = "$script:gcloudComponent start --data-dir=$script:datastore_data_dir --host-port=$script:datastore_host`:$script:datastore_port"
    
    Write-Host "gcloud command found at [$script:gcloudPath]"
    Write-Host "Running gcloud component [$script:gcloudComponent]"
    Write-Host "Argument list [$argList]"

    Start-Process $script:gcloudPath -ArgumentList $argList
    
}

function script:Start-Datastore {

    # Find location of gcloud command using where.exe (Windows) or which (MacOS/Linux)
    # Use where.exe on Windows otherwise use which

    $script:cmdFinder = "which"

    # Now that we have cmdFinder, find the location of gcloud command

    $script:gcloudSearchResults = Invoke-Expression "$script:cmdFinder gcloud"

    if ($null -eq $script:gcloudSearchResults) {
        Write-Host "Cannot find gcloud commands."
        exit(0)
    }

    # $gcloudSearchResults should return multiple lines like the below; 
    # We need to find the most compatible one to use based on Platform
    # C:\Apps\Google\CloudSDK\google-cloud-sdk\bin\gcloud
    # C:\Apps\Google\CloudSDK\google-cloud-sdk\bin\gcloud.cmd

    $script:gcloudPath = $script:gcloudSearchResults | Where-Object {$_ -notlike "*.cmd" }

    if ($null -eq $script:gcloudPath) {
        Write-Host "Compatible gcloud command not found."
        exit(0)
    }

    # Finally, we are ready to spin up Gcloud Datastore Emulator in new window
    # Full command looks like the below:
    # "gcloud beta emulators datastore start --data-dir=D:\data\datastore --host-port=localhost:38089"

    #Start-Process $script:gcloudPath -ArgumentList "$script:gcloudComponent start --data-dir=$script:datastore_data_dir --host-port=$script:datastore_host:$script:datastore_port"
    $argList = "$script:gcloudComponent start --data-dir=$script:datastore_data_dir --host-port=$script:datastore_host`:$script:datastore_port"
    
    Write-Host "gcloud command found at [$script:gcloudPath]"
    Write-Host "Running gcloud component [$script:gcloudComponent]"
    Write-Host "Argument list [$argList]"

    Start-Process $script:gcloudPath -ArgumentList $argList
}

# Main script

$connection = Get-NetTCPConnection -State Listen -LocalPort $script:datastore_port -WarningAction SilentlyContinue -ErrorAction SilentlyContinue

if ($null -ne $connection) {
    Write-Host "Connection using port [$script:datastore_port] exists."
    Write-Host "This script uses this port; unable to continue. Terminating script."
    exit(0)
}

if ($PSVersionTable.Platform -ceq "Win32NT") {
    script:Start-Datastore_Win32NT

    
} else {
    script:Start-Datastore
}

    
# Waiting for datastore to run before we proceed to set environment variables
# for Google App Engine to detect/connect to local datastore emulator.

$datastoreStarted = $false
Write-Host "`nWaiting for datastore to start running"

while (-not $datastoreStarted) {
    Start-Sleep -Milliseconds 1000
    
    Write-Host "Checking if datastore is up; Timeouts [$script:datastore_timeout]"
    $connection = Get-NetTCPConnection -State Listen -LocalPort $script:datastore_port -WarningAction SilentlyContinue -ErrorAction SilentlyContinue

    if ($null -ne $connection) {
        break
    }

    $script:datastore_timeout = $script:datastore_timeout - 1
    if ($script:datastore_timeout -le 0) {
        Write-Host "Datastore startup timeout."
        exit(0)
    }
}

Write-Host "Setting datastore variables"
# "gcloud beta emulators datastore env-init --data-dir=D:\data\datastore"
#Start-Process $script:gcloudPath -ArgumentList "$script:gcloudComponent start --data-dir=$script:datastore_data_dir --host-port=$script:datastore_host:$script:datastore_port"
$argList = "$script:gcloudComponent env-init --data-dir=$script:datastore_data_dir"

Write-Host "gcloud command found at [$script:gcloudPath]"
Write-Host "Running gcloud component [$script:gcloudComponent]"
Write-Host "Argument list [$argList]"

$variableList = Invoke-Expression "$script:gcloudPath $argList"
$variableList | ForEach-Object { Invoke-Expression ($_ -replace 'set (.+)=(.+)', '$env:$1="$2"') }

$credPath = Join-Path $(Get-Location) GOOGLE_APPLICATION_CREDENTIALS.json
Invoke-Expression '$env:GOOGLE_APPLICATION_CREDENTIALS="$credPath"'