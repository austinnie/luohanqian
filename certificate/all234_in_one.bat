@echo off
set APK_NAME=luohanqian
set JAVA_HOME="C:\Program Files\Java\jdk1.8.0_341"
set KEYSTORE="C:\Users\onsite-235\WeChatProjects\certificate\android.keystore"
set workddir=C:\Users\onsite-235\WeChatProjects\release

mv %workddir%\com.tencent.weauth-0.0.1.apk.aligned %workddir%%APK_NAME%-unsigned.apk

:: 1. 签名
%JAVA_HOME%\bin\jarsigner -verbose -keystore %KEYSTORE% -storepass 123456 -keypass 123456 -signedjar %workddir%\%APK_NAME%-signed.apk %workddir%\%APK_NAME%-unsigned.apk android

:: 2. 验证
%JAVA_HOME%\bin\jarsigner -verify -verbose %workddir%\%APK_NAME%-signed.apk

:: 3. 安装
adb install %workddir%\%APK_NAME%-signed.apk