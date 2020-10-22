#!/bin/bash

closure_compiler="bin/closure-compiler-v20200504.jar"

declare -a files=(
  "home/static/global/js/tinymce_init"
  "home/static/global/js/global"
  "home/static/home/js/infinite_scroll_home"
  "home/static/home/js/infinite_scroll_category"
  "users/static/users/js/dashboard"
  "events/static/events/js/events"
  "events/static/events/js/create_event"
  "events/static/events/js/update_event"
  "locations/static/locations/js/create_location"
  "locations/static/locations/js/update_location"
  "images/static/images/js/update_album"
  "articles/static/articles/js/update_article"
  "articles/static/articles/js/article_autocomplete"
)

trap 'echo -e "\nExiting…" >&2; pkill $$; exit' SIGINT

while true; do
  for i in "${files[@]}"; do
    input="$i.js"
    output="$i.min.js"
    cmd="java -jar $closure_compiler --js $input --js_output_file $output"

    if [ $input -nt $output ]; then
      echo "[$(date -Iseconds)] $cmd" >&2
      $cmd
    fi
  done

  sleep 1
done
