@echo off
echo datasets.bat
call datasets.bat
echo ranking.bat
call ranking.bat
echo report.bat
call report.bat
git add .
git c -m "daily update"
git push
echo end