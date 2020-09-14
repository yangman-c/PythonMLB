@echo off
if exist ranking\%today%.log (
    del ranking\%today%.log
)
if not exist ranking (
	md ranking
)
set today=%date:~0,4%-%date:~5,2%-%date:~8,2%
python ranking.py > ranking\%today%.log
exit