@echo off
echo "生成APK发布用的签名key"

set alias=android
set targetdir=C:\Users\onsite-235\WeChatProjects\certificate

rem C:\Users\onsite-235>where keytool.exe
rem C:\Program Files\Java\jdk1.8.0_341\bin\keytool.exe

keytool.exe -genkey -alias %alias% -keyalg RSA -keysize 2048 -validity 36500 -keystore %targetdir%\%alias%.keystore
pause

rem Austin_Japan
rem 
rem 爱行天下行者无疆
rem 爱行天下行者无疆
rem 深圳
rem 广东
rem CN




