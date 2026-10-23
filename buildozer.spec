[app]
title = Nova Calculator
package.name = novacalculator
package.domain = org.amirprojects
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,ttf,txt
version = 1.0.0
requirements = python3,kivy==2.3.0,kivymd==1.2.0
orientation = portrait
fullscreen = 0

# Android settings
android.api = 35
android.minapi = 23
android.archs = arm64-v8a
android.accept_sdk_license = True

# Permissions: this calculator does not need any.
# android.permissions =

[buildozer]
log_level = 2
warn_on_root = 1
