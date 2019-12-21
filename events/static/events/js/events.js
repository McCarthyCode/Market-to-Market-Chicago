$(document).ready(() => {
  // prevent page from scrolling to document hash
  if (document.location.hash) {
    setTimeout(function () {
      window.scrollTo(0, 0);
    }, 1);
  }

  // show appropriate view based on document hash
  if (document.location.hash === '' ||
      document.location.hash === '#' ||
      document.location.hash === '#calendar') {
      $('#calendar').show();
      $('#tabsCalendar').addClass('active');
  } else if (document.location.hash === '#byDate') {
      $('#byDate').show();
      $('#tabsByDate').addClass('active');
  } else if (document.location.hash === '#byLocation') {
      $('#byLocation').show();
      $('#tabsByLocation').addClass('active');
  }

  // define tabs behavior
  var $tabs = $('#tabs');
  var $tabsChildren = $('#tabs > li');
  var $activeTab = $('#tabs > li.active');

  $($activeTab.data('href')).show();

  function tabsChildrenClick($tab) {
    $activeTab.addClass('active');
    galleryPage = archivePage = 1;
    galleryEmpty = archiveEmpty = false;

    $tabsChildren.each(function () {
      $($(this).data('href')).hide();
      $(this).removeClass('active')
    });

    let view = $tab.data('href');
    document.location.hash = view;
    $(view).show();
  }

  $tabsChildren.on('click touchstart', function (event) {
    event.preventDefault();
    event.stopPropagation();

    $tabsChildren.removeClass('active');

    if (event.type === 'click') {
      tabsChildrenClick($(this));

      $tabsChildren.each(function () {
        $($(this).data('href')).hide();
      });

      $activeTab = $(this);
      $($(this).data('href')).show();
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
          $($(this).data('href')).hide();
        });

      $activeTab = $endElement;
      $endElement.addClass('active');
      $($endElement.data('href')).show();
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
});
