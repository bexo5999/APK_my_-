[app]
title = VideoToAudio
package.name = videotoaudio
package.domain = com.bexo
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,ttf
version = 1.0.0
requirements = python3==3.11, kivy, ffpyplayer
orientation = portrait
fullscreen = 1

# استخدام API 28 لتجنب مشاكل build-tools
android.api = 28
android.minapi = 21
android.ndk = 21e
android.sdk = 28
android.build_tools = 28.0.3

android.permissions = INTERNET, READ_EXTERNAL_STORAGE, WRITE_EXTERNAL_STORAGE, FOREGROUND_SERVICE
android.allow_background_service = True
android.entrypoint = main.py

[buildozer]
log_level = 2
warn_on_root = 1
