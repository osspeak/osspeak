@echo off
scripts\activate && cd osspeak && python main.py %* & cd .. && deactivate && pause