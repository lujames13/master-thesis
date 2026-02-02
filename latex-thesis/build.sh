#!/bin/bash
# 使用 latexmk 自動處理編譯次數與 biber
# -xelatex: 使用 xelatex 編譯
# -interaction=nonstopmode: 遇到錯誤不卡住
# -f: 強制編譯
latexmk -xelatex -interaction=nonstopmode main
