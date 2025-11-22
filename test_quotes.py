#!/usr/bin/env python3

curly_open = '"'
curly_close = '"'
straight = '"'

print(f"Curly open: {curly_open} Unicode: {hex(ord(curly_open))}")
print(f"Curly close: {curly_close} Unicode: {hex(ord(curly_close))}")
print(f"Straight: {straight} Unicode: {hex(ord(straight))}")
print(f"\nVisual comparison:")
print(f"Straight: {straight}Hello{straight}")
print(f"Curly: {curly_open}Hello{curly_close}")
