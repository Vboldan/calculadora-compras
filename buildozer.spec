[app]
title = Calculadora de Compras
package.name = calculadoracompras
package.domain = org.valdeci
source.dir = .
source.include_exts = py,png,jpg,jpeg,kv,atlas,txt
source.exclude_dirs = venv,build,dist,__pycache__
source.exclude_exts = spec
version = 1.0.0
icon.filename = %(source.dir)s/icone.png
requirements = python3,kivy==2.3.1,filetype==1.2.0
orientation = portrait
fullscreen = 0
android.archs = arm64-v8a
android.accept_sdk_license = True
p4a.commit = 957a3e5f8c270f7aa648ba185e5a68c1077a798d
p4a.local_recipes = ./p4a-recipes

[buildozer]
log_level = 2
warn_on_root = 1
bin_dir = ./bin

[android]
android.api = 35
android.minapi = 21