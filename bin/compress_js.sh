#!/bin/bash

closure_compiler="bin/closure-compiler-v20200504.jar"

declare -a files=(
  "home/static/home/js/global"
  "home/static/home/js/infinite_scroll_home"
  "home/static/home/js/infinite_scroll_category"
  "home/static/home/js/create_person"
  "users/static/users/js/create_view_invites"
  "events/static/events/js/events"
  "events/static/events/js/create_event"
  "events/static/events/js/update_event"
  "locations/static/locations/js/create_location"
  "locations/static/locations/js/update_location"
  "images/static/images/js/create_album"
  "images/static/images/js/update_album"
  "articles/static/articles/js/create_author"
  "articles/static/articles/js/create_article"
  "articles/static/articles/js/update_article"
  "articles/static/articles/js/article_autocomplete"
)

for i in "${files[@]}" ; do
  input="$i.js"
  output="$i.min.js"

  cmd="java -jar $closure_compiler --js $input --js_output_file $output"

  if [ $input -nt $output ] ; then
    echo "$cmd"
    $cmd
  fi
done
