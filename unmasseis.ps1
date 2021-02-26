taskkill /im /f xmrig

cd C:\ProgramData

# unhide XMRig folder
attrib -s -h ./xmrig

# delete XMRig
rm ./xmrig -Recurse

schtasks /delete /tn StudentFileBackup /f
