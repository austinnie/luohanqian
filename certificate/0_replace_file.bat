@echo off
setlocal enabledelayedexpansion

:: ===== Configuration =====
set "work_dir=..\release"
set "apk_path=%work_dir%\com.tencent.weauth-0.0.1.apk.aligned"
set "readme_src=C:\Users\onsite-235\WeChatProjects\luohanqian\assets\SaaA_embed\README.md"
set "temp_dir=%work_dir%\temp_apk_%random%"
set "repacked_file=%work_dir%\temp_repacked_%random%.apk"

:: ===== Initial Checks =====
echo [INIT] Verifying files in %work_dir%...
if not exist "%apk_path%" (
    echo [ERROR] APK not found: %apk_path%
    pause
    exit /b 1
)

if not exist "%readme_src%" (
    echo [ERROR] README.md not found: %readme_src%
    pause
    exit /b 1
)

:: ===== Backup =====
echo [BACKUP] Creating backup...
copy "%apk_path%" "%apk_path%.backup" >nul && (
    echo [OK] Backup created: %apk_path%.backup
) || (
    echo [WARNING] Backup failed (continuing anyway)
)

:: ===== Main Process =====
echo [PROCESS] Starting APK processing...

:: 1. Extract APK
echo [EXTRACT] Unpacking APK...
7z x "%apk_path%" -o"%temp_dir%" -y >nul
if errorlevel 1 (
    echo [ERROR] Extraction failed
    goto cleanup
)
echo [OK] Extracted to: %temp_dir%

:: 2. Add README.md
if not exist "%temp_dir%\assets\SaaA_embed\" (
    mkdir "%temp_dir%\assets\SaaA_embed"
)
copy "%readme_src%" "%temp_dir%\assets\SaaA_embed\" >nul
if errorlevel 1 (
    echo [ERROR] File copy failed
    goto cleanup
)
echo [OK] README.md added

:: 3. Repack with optimal compression
echo [REPACK] Compressing APK...
pushd "%temp_dir%"
7z a -tzip -mx5 -r "%repacked_file%" * >nul
if errorlevel 1 (
    echo [ERROR] Compression failed
    popd
    goto cleanup
)
popd

:: Verify repacked file exists in correct location
if not exist "%repacked_file%" (
    echo [ERROR] Repacked file not created in correct location
    echo [DEBUG] Expected: %repacked_file%
    echo [DEBUG] Current directory: %cd%
    dir "%work_dir%\temp_repacked_*.apk" 2>nul
    goto cleanup
)
echo [OK] Repack complete (optimized size)

:: 4. Replace original with correct naming
echo [REPLACE] Updating original APK...
del "%apk_path%" 2>nul
move /y "%repacked_file%" "%apk_path%" >nul
if errorlevel 1 (
    echo [ERROR] File replacement failed - trying copy...
    copy "%repacked_file%" "%apk_path%" >nul
    if errorlevel 1 (
        echo [ERROR] Both move and copy operations failed
        goto cleanup
    )
)
echo [OK] Original APK updated with correct naming: com.tencent.weauth-0.0.1.apk.aligned

:: 5. Verify result
echo [VERIFY] Checking results...
7z l "%apk_path%" | findstr /i "assets/SaaA_embed/README.md" >nul
if errorlevel 1 (
    echo [ERROR] Verification failed: README.md missing
) else (
    echo [SUCCESS] Operation completed!
    for %%F in ("%apk_path%") do echo [INFO] Final APK: %%~nxF (%%~zF bytes)
)

:: ===== Cleanup =====
:cleanup
echo [CLEANUP] Removing temp files...
if exist "%temp_dir%" rmdir /s /q "%temp_dir%"
if exist "%repacked_file%" del "%repacked_file%"

:: 清理可能错误创建的多余release目录
if exist "%work_dir%\release\" (
    echo [CLEANUP] Removing duplicate release directory...
    rmdir /s /q "%work_dir%\release\"
)

pause