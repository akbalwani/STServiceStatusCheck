echo "%date%_%time%	running from wrapper script" >>C:\PSO\PSOPROJECTS\STATE_OF_COLORADO\DaemonStatus\run\script-logs.log
::python C:\PSO\PSOPROJECTS\STATE_OF_COLORADO\DaemonStatus\DaemonStatusChecker
echo %cd% >> C:\cwd.txt
"C:\Program Files\Python310\python.exe" "C:\PSO\PSOPROJECTS\STATE_OF_COLORADO\DaemonStatus\DaemonStatusChecker.py"
exit
