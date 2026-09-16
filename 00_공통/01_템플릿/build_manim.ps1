<#
  manim 장면 렌더링 빌드 스크립트
  ------------------------------------------------------------
  사용 예)
    # 강01의 모든 장면을 1080p 로 렌더링
    .\build_manim.ps1 -SceneFile "D:\test1234\02_수학1\I_지수함수와_로그함수\01_지수와_로그\05_자료\manim\k01_scenes.py"

    # 특정 장면만, 빠르게 미리보기(480p)
    .\build_manim.ps1 -SceneFile ... -Scenes S1NthRoot -Quality preview

  렌더된 mp4 는 해당 강의 02_강의안\media\ 로 복사됩니다.
  (HTML 강의 슬라이드가 이 경로를 참조합니다)
#>
param(
  [Parameter(Mandatory = $true)][string]$SceneFile,
  [string[]]$Scenes = @(),
  [ValidateSet('preview', 'draft', 'final')][string]$Quality = 'final',
  [string]$OutDir = ''
)

$ErrorActionPreference = 'Stop'

# ── 도구 경로 ────────────────────────────────────────────────
$Venv = 'C:\Users\Lab419_out\AppData\Local\Temp\claude\D--test1234\738dd28b-ab48-4967-8cef-e558bf9a3b6c\scratchpad\venv'
$MikTeX = 'C:\Users\Lab419_out\AppData\Local\Programs\MiKTeX\miktex\bin\x64'
$Python = Join-Path $Venv 'Scripts\python.exe'

if (-not (Test-Path $Python)) { throw "python 을 찾을 수 없습니다: $Python" }
if (-not (Test-Path $SceneFile)) { throw "장면 파일을 찾을 수 없습니다: $SceneFile" }

$env:PATH = "$Venv\Scripts;$MikTeX;$env:PATH"

# ── 출력 경로: <강 폴더>\02_강의안\media ──────────────────────
$sceneDir = Split-Path -Parent $SceneFile          # ...\05_자료\manim
$lessonDir = Split-Path -Parent (Split-Path -Parent $sceneDir)   # ...\01_지수와_로그
if ($OutDir -eq '') { $OutDir = Join-Path $lessonDir '02_강의안\media' }
New-Item -ItemType Directory -Force $OutDir | Out-Null

$mediaDir = Join-Path $sceneDir '_build'

# ── 품질 설정 ────────────────────────────────────────────────
switch ($Quality) {
  'preview' { $res = '854,480';   $fps = 15 }
  'draft'   { $res = '1280,720';  $fps = 30 }
  'final'   { $res = '1920,1080'; $fps = 30 }
}

# ── 장면 목록: 지정이 없으면 파일에서 Scene 클래스를 모두 찾는다 ──
if ($Scenes.Count -eq 0) {
  $Scenes = Select-String -Path $SceneFile -Pattern '^class\s+(\w+)\s*\(\s*\w*Scene' |
            ForEach-Object { $_.Matches[0].Groups[1].Value }
}
if ($Scenes.Count -eq 0) { throw "렌더링할 Scene 클래스를 찾지 못했습니다." }

Write-Host "장면 $($Scenes.Count)개 · 품질 $Quality ($res @ ${fps}fps)" -ForegroundColor Cyan
Write-Host "출력 → $OutDir`n" -ForegroundColor Cyan

$logDir = Join-Path $sceneDir '_build\logs'
New-Item -ItemType Directory -Force $logDir | Out-Null

$ok = 0; $fail = @()
foreach ($s in $Scenes) {
  Write-Host "  [$($Scenes.IndexOf($s)+1)/$($Scenes.Count)] $s ..." -NoNewline
  $sw = [Diagnostics.Stopwatch]::StartNew()
  $log = Join-Path $logDir "$s.log"

  # manim / latex 가 stderr 로 내보내는 경고를 PowerShell 이 치명적 오류로
  # 바꾸지 않도록, 파이프라인에 합치지 않고 파일로 직접 흘려보낸다.
  # (Windows PowerShell 5.1 에서 native stderr 를 2>&1 하면 NativeCommandError 발생)
  $prev = $ErrorActionPreference
  $ErrorActionPreference = 'Continue'
  & $Python -m manim render `
      --media_dir $mediaDir `
      -r $res --fps $fps `
      --format mp4 `
      --disable_caching `
      $SceneFile $s > $log 2> "$log.err"
  $ErrorActionPreference = $prev
  $sw.Stop()

  $produced = Get-ChildItem -Path $mediaDir -Recurse -Filter "$s.mp4" -ErrorAction SilentlyContinue |
              Sort-Object LastWriteTime -Descending | Select-Object -First 1
  if ($produced) {
    Copy-Item $produced.FullName (Join-Path $OutDir "$s.mp4") -Force
    $mb = [math]::Round($produced.Length / 1MB, 1)
    Write-Host " 완료 ($([int]$sw.Elapsed.TotalSeconds)초, ${mb}MB)" -ForegroundColor Green
    $ok++
  }
  else {
    Write-Host " 실패  (로그: $log.err)" -ForegroundColor Red
    $fail += $s
  }
}

Write-Host "`n성공 $ok / $($Scenes.Count)" -ForegroundColor Cyan
if ($fail.Count -gt 0) {
  Write-Host "실패한 장면: $($fail -join ', ')" -ForegroundColor Red
  Write-Host "원인을 보려면 아래를 직접 실행하세요:" -ForegroundColor Yellow
  Write-Host "  $Python -m manim render --media_dir `"$mediaDir`" `"$SceneFile`" $($fail[0])"
  exit 1
}
