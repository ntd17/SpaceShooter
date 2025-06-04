[app]
title = Space Shooter
package.name = spaceshooter
package.domain = org.spaceshooter
source.dir = .
source.include_exts = py,png,jpg,mp3,wav
source.include_patterns = imgs/*,sounds/*
version = 1.0

requirements = pygame==2.1.0
fullscreen = 0

android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,WAKE_LOCK

android.api = 33
android.minapi = 21
android.ndk = 25b
android.ndk_api = 21
android.accept_sdk_license = True

android.archs = arm64-v8a
android.python_version = 3
android.allow_backup = True
android.presplash_color = #000000
android.private_storage = True
android.copy_libs = 1
p4a.bootstrap = sdl2
android.entrypoint = app/main.py

[p4a]
git_ignore = True
# Descomente se realmente usar receitas customizadas
local_p4a = .buildozer/android/platform/python-for-android

android.gradle_dependencies = org.jetbrains.kotlin:kotlin-stdlib-jdk7:1.8.0
android.enable_androidx = True
android.build_mode = debug
android.release_artifact = apk
android.meta_data = android.max_aspect=2.1

[buildozer]
log_level = 2
warn_on_root = 1
build_dir = ./.buildozer
parallel_processes = 4
build_memory = 2048M
build_cache = 1
socket_timeout = 300
