# Starts Ollama with models on E: and cloud features off.
Get-Process ollama* -ErrorAction SilentlyContinue | Stop-Process -Force
Start-Sleep 3
$env:OLLAMA_MODELS = "E:\ollama-models"
$env:OLLAMA_NO_CLOUD = "1"
Start-Process "E:\Ollama\ollama.exe" -ArgumentList "serve" -WindowStyle Hidden
Start-Sleep 8
Invoke-RestMethod http://localhost:11434/api/version
