#!/bin/bash

if [ ! -f "babel.cfg" ]; then
  echo "babel.cfg not found aborted!"
  exit 1
fi

pybabel extract -F babel.cfg -o messages.pot .
pybabel update -i messages.pot -d app/translations
