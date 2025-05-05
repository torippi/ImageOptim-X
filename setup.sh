#!/bin/bash
# setup.sh

# 必要なディレクトリを作成
mkdir -p raw_files
mkdir -p optimized_files
mkdir -p tests/data

# ディレクトリ構造を表示
echo "ディレクトリ構造を作成しました:"
find . -type d -not -path "*/\.*" | sort