[app]
title = Calculadora de Compras
package.name = calculadoracompras
package.domain = org.valdeci
source.dir = .
source.include_exts = py,png,jpg,jpeg,kv,atlas,txt
source.exclude_dirs = venv,build,dist,__pycache__
source.exclude_exts = spec
version = 1.0.0
requirements = python3,kivy==2.3.1
orientation = portrait
fullscreen = 0

[buildozer]
log_level = 2
warn_on_root = 1
bin_dir = ./bin

[android]
android.api = 35
android.minapi = 21
android.archs = arm64-v8a
android.accept_sdk_license = True