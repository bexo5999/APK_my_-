[app]

title = VideoToAudio
package.name = videotoaudio
package.domain = com.bexo

source.dir = .
source.include_exts = py,png,jpg,kv,atlas,ttf

version = 1.0.0

requirements = python3,kivy,ffpyplayer

orientation = portrait
fullscreen = 0

android.api = 28
android.minapi = 21
android.ndk = 21e
android.build_tools = 28.0.3

android.permissions = INTERNET,READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE,FOREGROUND_SERVICE

[buildozer]

log_level = 2
warn_on_root = 1
