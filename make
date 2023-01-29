#!/bin/bash

winPyinstallerPath="$HOME/Software/Python3.11/Scripts/pyinstaller.exe"

mkdir -p build/Linux/bin
mkdir -p build/Windows/bin

if [ "$1" == "clean" ]; then
    rm -r build
    rm CringeMidi.spec
    exit 0
fi

# Linux Version
pyinstaller --onedir --console -y\
            --name CringeMidi\
            --workpath build/Linux\
            --distpath build/Linux/bin\
            src/main.py

if [ "$?" == "0" ]; then
    cd build/Linux/bin
    tar -cpzvf CringeMidi.tar.xz CringeMidi/*
    cd ../../../

    # Windows Version
    wine "$winPyinstallerPath" --onedir --console -y\
                --name CringeMidi\
                --workpath build/Windows\
                --distpath build/Windows/bin\
                src/main.py
    
    cd build/Windows/bin
    zip -ur CringeMidi.zip CringeMidi/*
fi