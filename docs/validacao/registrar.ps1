param([Parameter(Mandatory=$true)][string]$Versao,[Parameter(Mandatory=$true)][string]$OriginaisTabnet)
$ErrorActionPreference = 'Stop'
$dest = Join-Path $PSScriptRoot ('windows-' + (Get-Date -Format yyyyMMdd-HHmmss))
New-Item -ItemType Directory -Path $dest | Out-Null
$os = Get-CimInstance Win32_OperatingSystem
$cpu = Get-CimInstance Win32_Processor
$pc = Get-CimInstance Win32_ComputerSystem
$ver = Get-ItemProperty 'HKLM:\SOFTWARE\Microsoft\Windows NT\CurrentVersion'
$commit = git -C $Versao rev-parse HEAD
if ($LASTEXITCODE -ne 0) {throw 'Use a pasta versao_avaliada de um clone git.'}
$python = Join-Path $Versao '.venv\Scripts\python.exe'
if (!(Test-Path $python)) {throw 'Ambiente .venv ausente. Consulte LEIA_PRIMEIRO.md.'}
$pv = & $python --version
if ($LASTEXITCODE -ne 0) {throw 'Falha ao executar Python'}
[ordered]@{coleta=(Get-Date -Format o); fuso=(Get-TimeZone).Id; sistema=$os.Caption; arquitetura=$os.OSArchitecture; versao=$ver.DisplayVersion; build=$os.BuildNumber; revisao_build=$ver.UBR; cpu=$cpu.Name; nucleos=$cpu.NumberOfCores; ram_GiB=[math]::Round($pc.TotalPhysicalMemory/1GB,1); gpu=@((Get-CimInstance Win32_VideoController).Name); powershell=$PSVersionTable.PSVersion.ToString(); git=(git --version); commit=$commit; python=$pv} | ConvertTo-Json | Set-Content (Join-Path $dest 'ambiente.json') -Encoding UTF8
$deps = & $python -m pip list --format=json
if ($LASTEXITCODE -ne 0) {throw 'Falha ao listar pacotes'}
$deps | Set-Content (Join-Path $dest 'pacotes.json') -Encoding UTF8
$items = foreach ($rel in @('dados/sih_cnv_nidf165441138_0_247_22.csv','maio/sih_cnv_nidf201212138_0_247_22.csv')) {
    $nome = Split-Path $rel -Leaf
    $arquivo = Get-Item -LiteralPath (Join-Path $OriginaisTabnet $nome)
    $hash = (Get-FileHash -LiteralPath $arquivo.FullName -Algorithm SHA256).Hash
    $href = (Get-FileHash -LiteralPath (Join-Path (Join-Path $Versao 'conciliacao') $rel) -Algorithm SHA256).Hash
    [pscustomobject]@{arquivo=$nome; bytes=$arquivo.Length; criacao_local=$arquivo.CreationTime.ToString('o'); modificacao_local=$arquivo.LastWriteTime.ToString('o'); sha256=$hash; sha256_commit=$href; coincide=($hash -eq $href); cabecalho=((Get-Content -LiteralPath $arquivo.FullName -TotalCount 4 -Encoding Default) -join ' | ')}
}
$items | Export-Csv (Join-Path $dest 'tabnet.csv') -NoTypeInformation -Encoding UTF8
Write-Output "Evidencias em $dest"
if ($items | Where-Object { !$_.coincide }) {throw 'Conteudo diferente do arquivo versionado. Preserve as duas copias.'}
