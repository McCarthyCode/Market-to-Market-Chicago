#!/bin/bash

sass_input_home="home/static/home/sass/base.sass"
sass_output_home="home/static/home/css/style.css"
sass_output_home_compressed="home/static/home/css/style.min.css"

sass_input_events="events/static/events/sass/base.sass"
sass_output_events="events/static/events/css/style.css"
sass_output_events_compressed="events/static/events/css/style.min.css"

closure_compiler="/opt/closure-compiler/closure-compiler-v20190929.jar"

js_input_global="home/static/home/js/global.js"
js_output_global="home/static/home/js/global.min.js"

js_input_home="home/static/home/js/script.js"
js_output_home="home/static/home/js/script.min.js"

js_input_events="events/static/events/js/script.js"
js_output_events="events/static/events/js/script.min.js"

declare -a foo=()
declare -a daemons=(
  "source env/bin/activate; python manage.py runserver 10.0.0.100:8000"
  "sass --watch $sass_input_home:$sass_output_home"
  "sass --watch --style=compressed $sass_input_home:$sass_output_home_compressed"
  "sass --watch $sass_input_events:$sass_output_events"
  "sass --watch --style=compressed $sass_input_events:$sass_output_events_compressed"
  "watch java -jar $closure_compiler --js $js_input_global --js_output_file $js_output_global"
  "watch java -jar $closure_compiler --js $js_input_home --js_output_file $js_output_home"
  "watch java -jar $closure_compiler --js $js_input_events --js_output_file $js_output_events"
)

for i in "${daemons[@]}"; do
  foo+=(--tab -e "bash -c '$i; exec bash'")
done

gnome-terminal "${foo[@]}"
