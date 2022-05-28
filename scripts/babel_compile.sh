#!/bin/bash

if [ ! -f "babel.cfg" ]; then
  echo "babel.cfg not found aborted!"
  exit 1
fi

pybabel compile -d app/translations
