#!/bin/bash

project_dir="$HOME/Repositories/Market-to-Market-Chicago"

sass_input_home="$project_dir/home/static/home/sass/base.sass"
sass_output_home="$project_dir/home/static/home/css/home.css"
sass_output_home_compressed="$project_dir/home/static/home/css/home.min.css"

sass_input_events="$project_dir/events/static/events/sass/base.sass"
sass_output_events="$project_dir/events/static/events/css/events.css"
sass_output_events_compressed="$project_dir/events/static/events/css/events.min.css"

sass_input_users="$project_dir/users/static/users/sass/base.sass"
sass_output_users="$project_dir/users/static/users/css/users.css"
sass_output_users_compressed="$project_dir/users/static/users/css/users.min.css"

sass_input_locations="$project_dir/locations/static/locations/sass/base.sass"
sass_output_locations="$project_dir/locations/static/locations/css/locations.css"
sass_output_locations_compressed="$project_dir/locations/static/locations/css/locations.min.css"

sass_input_images="$project_dir/images/static/images/sass/base.sass"
sass_output_images="$project_dir/images/static/images/css/images.css"
sass_output_images_compressed="$project_dir/images/static/images/css/images.min.css"

sass_input_articles="$project_dir/articles/static/articles/sass/base.sass"
sass_output_articles="$project_dir/articles/static/articles/css/articles.css"
sass_output_articles_compressed="$project_dir/articles/static/articles/css/articles.min.css"

sass_input_tinyMCE="$project_dir/home/static/home/sass/tinyMCE.sass"
sass_output_tinyMCE="$project_dir/home/static/home/css/tinyMCE.css"
sass_output_tinyMCE_compressed="$project_dir/home/static/home/css/tinyMCE.min.css"

declare -a args=(
  "$sass_input_home:$sass_output_home"
  "--style=compressed $sass_input_home:$sass_output_home_compressed"
  "$sass_input_events:$sass_output_events"
  "--style=compressed $sass_input_events:$sass_output_events_compressed"
  "$sass_input_users:$sass_output_users"
  "--style=compressed $sass_input_users:$sass_output_users_compressed"
  "$sass_input_locations:$sass_output_locations"
  "--style=compressed $sass_input_locations:$sass_output_locations_compressed"
  "$sass_input_images:$sass_output_images"
  "--style=compressed $sass_input_images:$sass_output_images_compressed"
  "$sass_input_articles:$sass_output_articles"
  "--style=compressed $sass_input_articles:$sass_output_articles_compressed"
  "$sass_input_tinyMCE:$sass_output_tinyMCE"
  "--style=compressed $sass_input_tinyMCE:$sass_output_tinyMCE_compressed"
)

for i in "${args[@]}"; do
  sass --watch -I $project_dir/home/static/home/sass $i &
done

clear
