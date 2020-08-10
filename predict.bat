@echo off
set/p option=ÇëÊäÈëÄãµÄÑ¡Ôñ:
if exist predictlog\%option%.log (
    del predictlog\%option%.log
)
python mldatabase.py %option% > predictlog\%option%.log