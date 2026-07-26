@echo off
echo "验证APK签名"

set apkname=luohanqian
set jardir="C:\Program Files\Java\jdk1.8.0_341\bin"
set signed_apk="C:\Users\onsite-235\WeChatProjects\release\%apkname%-signed.apk"

REM 验证签名
%jardir%\jarsigner.exe -verify -verbose -certs %signed_apk%

pause