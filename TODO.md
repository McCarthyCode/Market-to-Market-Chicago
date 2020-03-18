# To Do

## High Priorities

- user-select: none on topics
- Events
  - Event model
    - Album
  - Remove location from event form
    - Dashboard
    - EventManager
    - JS
  - Individual event page
    - Images
    - Update event
      - Add repeat options
- About/Contact
  - Bio (pending)
- Site Tour
  - Schedule
  - Remote desktop install
  - Walkthrough
- Invoice

## Medium Priorities

- Delete expired invites
  - Custom management command
    - https://docs.djangoproject.com/en/3.0/howto/custom-management-commands/#howto-custom-management-commands
  - cron job
- Test for autocomplete bugs
- Rename colors
- Divide locations by category on neighborhood page
- Add optional location field to articles
- Events
  - All events page
    - Add search/filters
- Category page
  - Locations
    - Search
    - Filters
      - Alphabetical
      - By neighborhood
- Consolidate duplicate entries
  - Neighborhood
  - Location
- Scroll to top button
- Add sidebar to dashboard

## Low Priorities

- Events
  - Add holiday field
  - All events page
    - Empty responses
      - Handle with proper status code
- Move CATEGORIES to Location model
- Backup external libraries
- Migrate users.js to add_event.js
- Migrate #content rules to base.sass
  - Home
  - Users
  - Locations
  - Events
- Events
  - All events page (read event)
    - Prevent scroll to top on tab selection
    - Fix bug where tapping a link scrolls to top and doesn't follow link
  - Delete event
    - Delete info along with RecurringEvent
  - Weekly updates (commands/crontab)
    - Delete past events
    - Create future events
    - Add fields to RecurringEvent model
      - Weekly list
  - DST bug
- Locations
  - Individual location page
    - Events
      - Make pretty
        - Add no wrap
        - Add visual month and dates
      - Weekly view
        - View only first event per weekday
      - Add paginiation
        - Front end (see more link)
        - Back end
- Change mtm.settings to django.conf.settings
- Change forms to Django forms
- Move global/grid Sass to separate files
- Change generated ID's to lower camelcase
- Add modals to delete forms
- Change title regex names to slug
- Restructure CATEGORY_CHOICES object
- Change grayscale colors to sensible names
- Individual category page
  - Hide locations with certain categories?
- Drink specials
