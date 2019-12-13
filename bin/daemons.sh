#!/bin/bash

sass_input_home="home/static/home/sass/base.sass"
sass_output_home="home/static/home/css/home.css"
sass_output_home_compressed="home/static/home/css/home.min.css"

sass_input_events="events/static/events/sass/base.sass"
sass_output_events="events/static/events/css/events.css"
sass_output_events_compressed="events/static/events/css/events.min.css"

sass_input_users="users/static/users/sass/base.sass"
sass_output_users="users/static/users/css/users.css"
sass_output_users_compressed="users/static/users/css/users.min.css"

declare -a foo=()
declare -a daemons=(
  "source env/bin/activate; python manage.py runserver 10.0.0.100:8000"
  "sass --watch $sass_input_home:$sass_output_home"
  "sass --watch --style=compressed $sass_input_home:$sass_output_home_compressed"
  "sass --watch $sass_input_events:$sass_output_events"
  "sass --watch --style=compressed $sass_input_events:$sass_output_events_compressed"
  "sass --watch $sass_input_users:$sass_output_users"
  "sass --watch --style=compressed $sass_input_users:$sass_output_users_compressed"
)

for i in "${daemons[@]}"; do
  foo+=(--tab -e "bash -c '$i; exec bash'")
done

gnome-terminal "${foo[@]}"
