#!/bin/bash

sass_input_home="home/static/home/sass/base.sass"
sass_output_home="home/static/home/css/style.css"
sass_output_home_compressed="home/static/home/css/style.min.css"

sass_input_users="users/static/users/sass/base.sass"
sass_output_users="users/static/users/css/style.css"
sass_output_users_compressed="users/static/users/css/style.min.css"

closure_compiler="/opt/closure-compiler/closure-compiler-v20190929.jar"

js_input_home="home/static/home/js/script.js"
js_output_home="home/static/home/js/script.min.js"

js_input_users="users/static/users/js/script.js"
js_output_users="users/static/users/js/script.min.js"

declare -a foo=()
declare -a daemons=(
  "source env/bin/activate; python manage.py runserver 10.0.0.100:8000"
  "sass --watch $sass_input_home:$sass_output_home"
  "sass --watch --style=compressed $sass_input_home:$sass_output_home_compressed"
  "sass --watch $sass_input_users:$sass_output_users"
  "sass --watch --style=compressed $sass_input_users:$sass_output_users_compressed"
  "watch java -jar $closure_compiler --js $js_input_home --js_output_file $js_output_home"
  "watch java -jar $closure_compiler --js $js_input_users --js_output_file $js_output_users"
)

for i in "${daemons[@]}"; do
  foo+=(--tab -e "bash -c '$i; exec bash'")
done

gnome-terminal "${foo[@]}"
