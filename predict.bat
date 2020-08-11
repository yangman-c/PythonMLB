@echo off
set/p option=ÇëÊäÈëÄãµÄÑ¡Ôñ:
if exist predictlog\%option%.log (
    del predictlog\%option%.log
)
set today=%date:~0,4%-%date:~5,2%-%date:~8,2%
if not exist predictlog\%today%\ (
	md  predictlog\%today%\
)
python mldatabase.py %option% > predictlog\%today%\%option%.log