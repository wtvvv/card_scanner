@echo off

rem path to activate conda env, make sure conda env has required packages
cd "C:\Users\Scanning"
call conda activate base
echo activated conda-base

rem path to project directory
cd desktop\scanformepls
echo opened project directory

rem python script file path
python "C:\Users\Scanning\Desktop\scanformepls\scanformepls.py"
pause
