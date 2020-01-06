$(document).ready(function () {
  // show appropriate view based on document hash
  let $calendar = $('#calendarView');
  let $byDate = $('#byDateView');
  let $byLocation = $('#byLocationView');

  let $tabsCalendar = $('#tabsCalendar');
  let $tabsByDate = $('#tabsByDate');
  let $tabsByLocation = $('#tabsByLocation');

  if (document.location.hash === '#byDate') {
    $byDate.show();
    $tabsByDate.addClass('active');
  } else if (document.location.hash === '#byLocation') {
    $byLocation.show();
    $tabsByLocation.addClass('active');
  } else {
    $calendar.show();
    $tabsCalendar.addClass('active');
  }

  // define tabs behavior
  let $tabs = $('#tabs');
  let $tabsChildren = $('#tabs > li');
  let $activeTab = $('#tabs > li.active');

  $($activeTab.data('href') + 'View').show();

  function tabsChildrenClick($tab) {
    $tabsChildren.each(function () {
      $($(this).data('href') + 'View').hide();
      $(this).removeClass('active')
    });

    let view = $tab.data('href');
    document.location.hash = view;
    $(view + 'View').show();
  }

  $tabsChildren.on('click touchstart', function (event) {
    event.preventDefault();
    event.stopPropagation();

    $tabsChildren.removeClass('active');

    if (event.type === 'click') {
      tabsChildrenClick($(this));

      $tabsChildren.each(function () {
        $($(this).data('href') + 'View').hide();
      });

      $activeTab = $(this);
      $($(this).data('href') + 'View').show();
    } else {
      $(this).addClass('active');
    }
  });

  $tabsChildren.on('touchend', function (event) {
    let changes = event.changedTouches[0];
    let $endElement = $(document.elementFromPoint(changes.pageX, changes.pageY));

    if ($endElement.parent('#tabs').length) {
      tabsChildrenClick($(this));

      $tabsChildren
        .removeClass('active')
        .each(function () {
          $($(this).data('href') + 'View').hide();
        });

      $activeTab = $endElement;
      $endElement.addClass('active');
      $($endElement.data('href') + 'View').show();
      event.stopPropagation();
    }
  });

  $tabs.mouseenter(function () {
    $activeTab.removeClass('active');
  });
  $tabs.on('mouseleave touchstart', function () {
    $activeTab.addClass('active');
  });
  $tabs.on('touchend', function () {
    $tabsChildren.removeClass('active');
    $activeTab.addClass('active');
  });

  // show month and year in header and populate calendar with slots
  // for that month
  function updateMonth(context) {
    $('#month input[name="year"]').val(context['year']);
    $('#month input[name="month"]').val(context['month']);

    let date = new Date(context['year'], context['month'] - 1, 1);
    let fullMonth = '';

    switch (date.getMonth() + 1) {
      case 1:
        fullMonth = 'January';
        break;

      case 2:
        fullMonth = 'February';
        break;

      case 3:
        fullMonth = 'March';
        break;

      case 4:
        fullMonth = 'April';
        break;

      case 5:
        fullMonth = 'May';
        break;

      case 6:
        fullMonth = 'June';
        break;

      case 7:
        fullMonth = 'July';
        break;

      case 8:
        fullMonth = 'August';
        break;

      case 9:
        fullMonth = 'September';
        break;

      case 10:
        fullMonth = 'October';
        break;

      case 11:
        fullMonth = 'November';
        break;

      case 12:
        fullMonth = 'December';
        break;
    }

    $('#calendarControls h3').text(`${fullMonth} ${date.getFullYear()}`);

    $.get('/events/month/', context, function (response) {
      $calendar.empty();
      $calendar.append(response);
    });
  }

  function updateByDate(context) {
    $.get('/events/by-date/', context, function (response) {
      $byDate.empty();
      $byDate.append(response);
    });
  }

  function updateAndShowByDate(context) {
    $.get('/events/by-date/', context, function (response) {
      $byDate.empty();
      $byDate.append(response);

      $tabsChildren
        .removeClass('active')
        .each(function () {
          $($(this).data('href') + 'View').hide();
        });

      $activeTab = $tabsByDate;

      $byDate.show();
      $tabsByDate.addClass('active');

      document.location.href = '#' + context['day'];
    });
  }

  function updateByLocation(context) {
    $.get('/events/by-location/', context, function (response) {
      $byLocation.empty();
      $byLocation.append(response);
    });
  }

  // update prev/next buttons
  function updatePrev(context) {
    $.get('/events/prev/', context, function (response) {
      let $prev = $('#prev');
      let date = response['date'];

      if (response['disabled']) {
        $prev.addClass('disabled');
      } else {
        $prev.data('year', date['year']);
        $prev.data('month', date['month']);

        $prev.attr('data-year', date['year']);
        $prev.attr('data-month', date['month']);

        $prev.removeClass('disabled');
      }
    });
  }

  function updateNext(context) {
    $.get('/events/next/', context, function (response) {
      let $next = $('#next');
      let date = response['date'];

      $next.data('year', date['year']);
      $next.data('month', date['month']);

      $next.attr('data-year', date['year']);
      $next.attr('data-month', date['month']);

      $next.removeClass('disabled');
    });
  }

  function updateDate(context) {
    updateMonth(context);
    updateByDate(context);
    updateByLocation(context);

    updatePrev(context);
    updateNext(context);
  }

  function updateAndShowDate(context) {
    updateMonth(context);
    updateAndShowByDate(context);
    updateByLocation(context);

    updatePrev(context);
    updateNext(context);
  }

  // navigate to previous/next day
  let $navButtons = $('#prev, #next');
  $navButtons.click(function () {
    let $button = $(this);

    if ($button.hasClass('disabled')) {
      return;
    }

    $navButtons.removeClass('disabled');

    updateDate({
      'year': $button.data('year'),
      'month': $button.data('month'),
    });
  });

  // navigate to by date view on calendar cell click
  function showDate(context) {
    let currentYear = Number($('#month input[name="year"]').val());
    let currentMonth = Number($('#month input[name="month"]').val());

    if (currentYear !== context['year'] || currentMonth !== context['month']) {
      updateAndShowDate(context);
    } else {
      $tabsChildren
        .removeClass('active')
        .each(function () {
          $($(this).data('href') + 'View').hide();
        });

      $activeTab = $tabsByDate;

      $byDate.show();
      $tabsByDate.addClass('active');

      document.location.href = '#' + context['day'];
    }
  }

  $calendar.on('click', '#calendarGrid > div:not(.header)', function () {
    let year = $(this).data('year');
    let month = $(this).data('month');
    let day = $(this).data('day');

    let date = new Date(year, month - 1, day);
    let today = new Date();

    today.setHours(0)
    today.setMinutes(0)
    today.setSeconds(0)
    today.setMilliseconds(0);

    if (date < today) {
      return;
    }

    showDate({
      'year': year,
      'month': month,
      'day': day,
    });
  });
});
