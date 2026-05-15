param(
  [Parameter(Mandatory=$true)][string]$PageUrl,
  [Parameter(Mandatory=$true)][ValidateSet('top','lower')][string]$Kind
)

$ErrorActionPreference = 'Stop'
$Root = 'C:\Users\R\Dropbox\drshin.kr'
$GeneratedDir = 'C:\Users\R\.codex\generated_images\019e0c39-010a-72b3-aafd-15bb5b42170e'
$Manifest = Join-Path $Root 'private-figures\page-image-generation-v2\detail_manifest.csv'

$row = Import-Csv -LiteralPath $Manifest | Where-Object { $_.page_url -eq $PageUrl } | Select-Object -First 1
if (-not $row) {
  throw "No manifest row for $PageUrl"
}

if ($Kind -eq 'top') {
  $privateRel = $row.top_image
  $publicRel = $row.public_top_image
} else {
  $privateRel = $row.lower_image
  $publicRel = $row.public_lower_image
}

$src = Get-ChildItem -LiteralPath $GeneratedDir -File | Sort-Object LastWriteTime -Descending | Select-Object -First 1
if (-not $src) {
  throw "No generated image found in $GeneratedDir"
}

$private = Join-Path $Root $privateRel
$public = Join-Path $Root ($publicRel.TrimStart('/') -replace '/', '\')
New-Item -ItemType Directory -Force -Path (Split-Path -Parent $private) | Out-Null
New-Item -ItemType Directory -Force -Path (Split-Path -Parent $public) | Out-Null
Copy-Item -LiteralPath $src.FullName -Destination $private -Force
Copy-Item -LiteralPath $src.FullName -Destination $public -Force

[PSCustomObject]@{
  page_url = $PageUrl
  kind = $Kind
  source = $src.Name
  private = $private
  public = $public
  bytes = (Get-Item -LiteralPath $private).Length
}
