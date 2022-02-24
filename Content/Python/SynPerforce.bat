@echo off
rem Figure out if we should append the -prompt argument
echo Syncing Perforce...Begin!
p4 sync -f //depot/Test_Poj_01/...
rem Done!
echo Syncing Perforce...Done!