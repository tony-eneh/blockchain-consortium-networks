param(
    [switch]$Clean
)

$paperDir = Join-Path $PSScriptRoot '..\paper'
Set-Location $paperDir

if ($Clean) {
    latexmk -C paper.tex
}

$busyFile = Join-Path $paperDir 'paper.synctex(busy)'
if (Test-Path $busyFile) {
    Remove-Item $busyFile -Force
}

latexmk -pdf -interaction=nonstopmode -file-line-error paper.tex