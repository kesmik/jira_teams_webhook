#!/bin/bash

echo "Creating symlinks"
ln -s cfg/configuration.py configuration.py
echo "Starting server"
python srv.py
