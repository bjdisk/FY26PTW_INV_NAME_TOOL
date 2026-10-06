#!/bin/sh
# 把 src/app.html 包成可直接開啟／部署的 index.html
cd "$(dirname "$0")"
{ printf '<!doctype html>\n<html lang="zh-Hant">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">\n</head>\n<body>\n'; cat src/app.html; printf '\n</body>\n</html>\n'; } > index.html
