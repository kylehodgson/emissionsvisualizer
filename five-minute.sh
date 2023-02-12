#!/bin/bash
 cd ~/projects/grafana
 . ./.env
 . venv/bin/activate
 python moer.py
 python grid.py
 python purple.py
 python juicy.py
 