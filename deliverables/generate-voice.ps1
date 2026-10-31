Add-Type -AssemblyName System.Speech
$root = Split-Path -Parent $MyInvocation.MyCommand.Path
$data = Get-Content -LiteralPath (Join-Path $root 'narration.json') -Raw -Encoding UTF8 | ConvertFrom-Json
$audioDir = Join-Path $root 'audio'
New-Item -ItemType Directory -Force -Path $audioDir | Out-Null
$index = 0
foreach ($scene in $data.scenes) {
  foreach ($sentence in $scene.sentences) {
    $index += 1
    $voice = New-Object System.Speech.Synthesis.SpeechSynthesizer
    $voice.SelectVoice('Microsoft Huihui Desktop')
    $voice.Rate = 1
    $voice.Volume = 100
    $path = Join-Path $audioDir ('{0:D2}.wav' -f $index)
    $voice.SetOutputToWaveFile($path)
    $voice.Speak($sentence)
    $voice.Dispose()
  }
}
Write-Output "Generated $index narration clips"
