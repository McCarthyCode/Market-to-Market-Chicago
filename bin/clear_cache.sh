#!/bin/bash

declare -a apps=(
  "mtm"
  "home"
  "users"
  "locations"
  "events"
  "images"
  "articles"
)

for i in "${apps[@]}"; do
  echo "rm ./$i/__pycache__/*.pyc"
  rm ./$i/__pycache__/*.pyc
done
