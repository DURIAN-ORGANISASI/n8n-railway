$ErrorActionPreference = 'Stop'
$bytes = New-Object byte[] 32
$rng = [System.Security.Cryptography.RandomNumberGenerator]::Create()
try {
    $rng.GetBytes($bytes)
} finally {
    $rng.Dispose()
}
[System.BitConverter]::ToString($bytes).Replace('-', '').ToLowerInvariant()
