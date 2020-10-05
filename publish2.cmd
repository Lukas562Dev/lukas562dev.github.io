@echo off
echo.
echo Adding everything to local git...
echo.
git add .
echo.
echo.
echo Commiting everything to local git...
echo.
set /P localGITcommit="What description will you add for the commit? "
echo.
git commit -m "%localGITcommit%"
echo.
echo.
echo Pushing to github...
echo.
git push -u origin master
echo.
@echo on
