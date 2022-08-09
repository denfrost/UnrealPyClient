@echo off
echo Syncing Perforce...Start!
rem Setup and Login Perforce demand
p4 sync -f //depot/Test_Poj_01/...
echo Syncing Perforce...Done!
pause