$(document).ready(() => {
  // show appropriate view based on document hash
  let $calendar = $('#calendarView');
  let $byDate = $('#byDateView');
  let $byLocation = $('#byLocationView');

  if (document.location.hash === '' ||
    document.location.hash === '#' ||
    document.location.hash === '#calendar') {
    $calendar.show();
    $('#tabsCalendar').addClass('active');
  } else if (document.location.hash === '#byDate') {
    $byDate.show();
    $('#tabsByDate').addClass('active');
  } else if (document.location.hash === '#byLocation') {
    $byLocation.show();
    $('#tabsByLocation').addClass('active');
  }

  // define tabs behavior
  var $tabs = $('#tabs');
  var $tabsChildren = $('#tabs > li');
  var $activeTab = $('#tabs > li.active');

  $($activeTab.data('href') + 'View').show();

  function tabsChildrenClick($tab) {
    $activeTab.addClass('active');
    galleryPage = archivePage = 1;
    galleryEmpty = archiveEmpty = false;

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
    var changes = event.changedTouches[0];
    var $endElement = $(document.elementFromPoint(changes.pageX, changes.pageY));

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
  $tabs.mouseleave(function () {
    $activeTab.addClass('active');
  });

  $(window).on('touchstart', function () {
    $activeTab.addClass('active');
  });
  $(window).on('touchend', function () {
    $tabsChildren.removeClass('active');
    $activeTab.addClass('active');
  });

  // show month and year in header and populate calendar with slots
  // for that month
  function displayMonth(context) {
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

  function displayByDate(context) {
    $.get('/events/by-date/', context, function (response) {
      $byDate.empty();
      $byDate.append(response);
    });
  }

  function displayByLocation(context) {
    $.get('/events/by-location/', context, function (response) {
      $byLocation.empty();
      $byLocation.append(response);
    });
  }

  function showLoadingIcon() {
    // loading...
  }

  // update prev/next buttons
  function updatePrev(context) {
    showLoadingIcon();

    $.get('/events/prev/', context, function (response) {
      // debugger;
      let $prev = $('#prev');
      let date = response['date'];

      console.log(response);

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
    showLoadingIcon();

    $.get('/events/next/', context, function (response) {
      let $next = $('#next');
      let date = response['date'];

      console.log(response);

      $next.data('year', date['year']);
      $next.data('month', date['month']);

      $next.attr('data-year', date['year']);
      $next.attr('data-month', date['month']);

      $next.removeClass('disabled');
    });
  }

  // navigate to previous/next day
  let $navButtons = $('#prev, #next');
  $navButtons.click(function () {
    let $button = $(this);

    if ($button.hasClass('disabled')) {
      return;
    }

    let year = $button.data('year');
    let month = $button.data('month');

    $navButtons.removeClass('disabled');

    let context = {
      'year': year,
      'month': month,
    };

    displayMonth(context);
    displayByDate(context);
    displayByLocation(context);

    updatePrev(context);
    updateNext(context);
  });
});
