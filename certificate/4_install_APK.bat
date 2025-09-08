@echo off
echo "安装apk"

set apkname=luohanqian
set jardir=C:\Program Files\Java\jdk1.8.0_341\bin
set certdir=C:\Users\onsite-235\WeChatProjects\certificate
set workddir=C:\Users\onsite-235\WeChatProjects\release
set targetdir=%workddir%

adb install -r -f %targetdir%\%apkname%-signed.apk"

pause