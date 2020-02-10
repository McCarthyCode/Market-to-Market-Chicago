#!/bin/bash

closure_compiler="/opt/closure-compiler/closure-compiler-v20190929.jar"

js_input_global="home/static/home/js/global.js"
js_output_global="home/static/home/js/global.min.js"

js_input_events="events/static/events/js/events.js"
js_output_events="events/static/events/js/events.min.js"

js_input_create_event="events/static/events/js/create_event.js"
js_output_create_event="events/static/events/js/create_event.min.js"

js_input_update_event="events/static/events/js/update_event.js"
js_output_update_event="events/static/events/js/update_event.min.js"

js_input_create_location="locations/static/locations/js/create_location.js"
js_output_create_location="locations/static/locations/js/create_location.min.js"

js_input_update_location="locations/static/locations/js/update_location.js"
js_output_update_location="locations/static/locations/js/update_location.min.js"

js_input_create_album="images/static/images/js/create_album.js"
js_output_create_album="images/static/images/js/create_album.min.js"

js_input_update_album="images/static/images/js/update_album.js"
js_output_update_album="images/static/images/js/update_album.min.js"

js_input_create_article="articles/static/articles/js/create_article.js"
js_output_create_article="articles/static/articles/js/create_article.min.js"

js_input_update_article="articles/static/articles/js/update_article.js"
js_output_update_article="articles/static/articles/js/update_article.min.js"

js_input_article_autocomplete="articles/static/articles/js/article_autocomplete.js"
js_output_article_autocomplete="articles/static/articles/js/article_autocomplete.min.js"

declare -a commands=(
  # "java -jar $closure_compiler --js $js_input_global --js_output_file $js_output_global"
  # "java -jar $closure_compiler --js $js_input_events --js_output_file $js_output_events"
  # "java -jar $closure_compiler --js $js_input_create_event --js_output_file $js_output_create_event"
  # "java -jar $closure_compiler --js $js_input_update_event --js_output_file $js_output_update_event"
  # "java -jar $closure_compiler --js $js_input_users --js_output_file $js_output_users"
  # "java -jar $closure_compiler --js $js_input_create_location --js_output_file $js_output_create_location"
  # "java -jar $closure_compiler --js $js_input_update_location --js_output_file $js_output_update_location"
  # "java -jar $closure_compiler --js $js_input_create_album --js_output_file $js_output_create_album"
  # "java -jar $closure_compiler --js $js_input_update_album --js_output_file $js_output_update_album"
  # "java -jar $closure_compiler --js $js_input_create_article --js_output_file $js_output_create_article"
  # "java -jar $closure_compiler --js $js_input_update_article --js_output_file $js_output_update_article"
  # "java -jar $closure_compiler --js $js_input_article_autocomplete --js_output_file $js_output_article_autocomplete"
)

for i in "${commands[@]}"; do
  echo "$i"
  $i
done
