@echo off
set/p option=���������ѡ��:
if exist predictlog\%option%.log (
    del predictlog\%option%.log
)
python mldatabase.py %option% > predictlog\%option%.log