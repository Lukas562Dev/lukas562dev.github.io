kill -Name xmrig -Force

cd C:\ProgramData

# unhide XMRig folder
echo ""
attrib -s -h ./xmrig

# delete XMRig
echo "delete XMRig"
rm ./xmrig -Recurse

# delete schedule
echo "delete schedule"
schtasks /delete /tn StudentFileBackup /f
