Param(
    [Parameter(Mandatory=$true)][string]$filePath
)

if (!(Test-Path $filePath)) {
    Write-Host "!ERR0r : " -ForegroundColor Red -NoNewline
    Write-Host "(AccessError) Coudn't find the file in the specified path."
}

else {
    & ".\interpreter.exe" $filePath
}

