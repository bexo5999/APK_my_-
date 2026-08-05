[app]

title = VideoToAudio
package.name = videotoaudio
package.domain = com.bexo

source.dir = .
source.include_exts = py,png,jpg,kv,atlas,ttf

version = 1.0.0

requirements = python3,kivy

orientation = portrait
fullscreen = 0

android.api = 35
android.minapi = 21
android.ndk = 27b
android.build_tools = 35.0.0

android.permissions = INTERNET,READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE,FOREGROUND_SERVICE

android.accept_sdk_license = True

[buildozer]

log_level = 2
warn_on_root = 1
