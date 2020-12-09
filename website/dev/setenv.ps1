# 
$credentials_json_file = Join-Path $([System.IO.Path]::GetDirectoryName($PROFILE)) "hci-admin-6ec8912b4124.json"
$env:GOOGLE_APPLICATION_CREDENTIALS=$credentials_json_file
Write-Host "Set path: $env:GOOGLE_APPLICATION_CREDENTIALS"
