@echo off
echo "用生成的key对APK签名"

set apkname=luohanqian
set jardir=C:\Program Files\Java\jdk1.8.0_341\bin
set certdir=C:\Users\onsite-235\WeChatProjects\certificate
set workddir=C:\Users\onsite-235\WeChatProjects\release
set targetdir=%workddir%

"%jardir%\jarsigner.exe" -verbose -keystore "%certdir%\android.keystore" -storepass 123456 -keypass 123456 -signedjar "%targetdir%\%apkname%-signed.apk" "%workddir%\com.tencent.weauth-0.0.1.apk.aligned" android

echo "签名完成！输出文件: %targetdir%\%apkname%-signed.apk"

pause