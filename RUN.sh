#!/bin/bash
echo " [VOID] Mobile Bootloader..."
echo " Checking Dependencies..."
pkg install -y python llama-cpp > /dev/null 2>&1
echo " Launching Core..."
python void.py
