@echo off
setlocal
%~d0
cd %~p0
python svm.py %*
endlocal
