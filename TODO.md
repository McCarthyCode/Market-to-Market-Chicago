# To Do

## High Priorities

- Change path to static files in staging/production
- Readjust positioning of alert contents
- Truncate slug to 80 characters
- Move libraries to lib directory
- Events forms
  - Change All-day to holiday
  - Allow holiday edit
  - Add all-day field
  - Delete RepeatInfo along with RecurringEvent

## Medium Priorities

- Take update author redirect to author page
- Autocorrect bugs
  - Double text on enter
  - Double selection on hover
- Events
  - Home page news feed item
  - Individual location page
    - Make pretty
      - Add visual month and dates
      - Weekly view
  - Neighborhood page
    - Make pretty
      - Add visual month and dates
      - Weekly view
        - View only first event per weekday
- Neighborhood page
  - Divide locations by category
- Category page
  - Locations
    - Search
    - Filters
      - Alphabetical
      - By neighborhood
- Scroll to top button
- Add sidebar to dashboard
- Add icons to input fields

## Low Priorities

- Change title variables to title template blocks
- Events
  - All events page
    - Add search/filters
    - Empty responses
      - Handle with proper status code (204)
  - Individual event page
    - Update event
      - Add repeat options
  - Weekly updates (commands/crontab)
    - Delete past events
    - Create future events
    - Add fields to RecurringEvent model
      - Weekly list
- Locations
  - Individual location page
    - Events
      - Add pagination
        - Front end (see more link)
        - Back end
  - Neighborhood page
    - Events
      - Add pagination
        - Front end (see more link)
        - Back end
- Move CATEGORIES to Location model
- Backup external libraries
- Migrate users.js to add_event.js
- Migrate #content rules to base.sass
  - Home
  - Users
  - Locations
  - Events
- Change forms to Django forms
- Move global/grid Sass to separate files
- Change generated ID's to lower camelcase
- Add modals to delete forms
- Restructure CATEGORY_CHOICES object
- Drink specials
- Test for autocomplete bugs
- Add optional location field to articles (ask Bill)
- Consolidate duplicate entries
  - Neighborhood
  - Location
