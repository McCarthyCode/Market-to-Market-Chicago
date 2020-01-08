# To Do

## High Priorities

- Dashboard
  - Add neighborhood autocomplete
  - Fix autocomplete on click bug
- Home page
  - News Feed
    - Articles
    - Locations
    - Events
    - Albums
  - Infinite scrolling
- Events
  - All events page
    - Prevent scroll to top on tab selection
    - Fix bug where tapping a link scrolls to top and doesn't follow link
  - Individual event page
    - Update events front end (event page)
    - Update events back end
    - Delete events front end (event page)
    - Delete events back end
  - Weekly updates (commands/crontab)
    - Delete past events
    - Create future events
    - Add fields to RecurringEvent model
      - Weekly list
- Locations
  - Individual category page
    - Locations
    - Articles
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
    - Update location front end (location page)
    - Update location back end
    - Delete location front end (location page)
    - Delete location back end
- People to Know
- Articles
  - Title
  - Author
  - Date
  - Body
  - Images
- Images
  - Resize on input
  - Image model
  - Album model
    - One album to many images
  - Gallery view
- Ads
  - Leaderboard (top)
  - 3 Leaderboard/mobile leaderboard (between news items)
  - Medium rectangle (sidebar)
  - Skyscraper (sidebar)

## Medium Priorities

- Custom error pages
  - 404
  - 500
- Events
  - All events page
    - Add search/filters
    - Navigation
      - Disabled next button
  - Individual event page
    - Images
- Locations
  - Individual category page
    - Locations
      - Search
      - Filters
        - Alphabetical
        - By neighborhood
- Drink specials

## Low Priorities

- Dashboard
  - Handle focusout of text input and click on autocomplete properly
- Events
  - All events page
    - Empty responses
      - Handle with proper status code
- Move CATEGORIES to Location model
- Strip periods from addresses on input
