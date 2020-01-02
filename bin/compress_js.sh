#!/bin/bash

closure_compiler="/opt/closure-compiler/closure-compiler-v20190929.jar"

js_input_global="home/static/home/js/global.js"
js_output_global="home/static/home/js/global.min.js"

js_input_events="events/static/events/js/events.js"
js_output_events="events/static/events/js/events.min.js"

js_input_users="users/static/users/js/users.js"
js_output_users="users/static/users/js/users.min.js"

declare -a commands=(
  "java -jar $closure_compiler --js $js_input_global --js_output_file $js_output_global"
#   "java -jar $closure_compiler --js $js_input_events --js_output_file $js_output_events"
#   "java -jar $closure_compiler --js $js_input_users --js_output_file $js_output_users"
)

for i in "${commands[@]}"; do
  echo "$i"
  $i
done
