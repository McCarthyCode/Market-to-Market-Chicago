#!/bin/bash

declare -a apps=(
    "mtm"
    "users"
    "locations"
    "events"
)

for i in "${apps[@]}"; do
  echo "rm ./$i/__pycache__/*.pyc"
  rm ./$i/__pycache__/*.pyc
done
