$(document).ready(function () {
  // determine if element is in viewport
  $.fn.isInViewport = function () {
    if (!$(this).is(':visible')) {
      return false;
    }

    let elementTop = $(this).offset().top;
    let elementBottom = elementTop + $(this).outerHeight();
    let viewportTop = $(window).scrollTop();
    let viewportBottom = viewportTop + $(window).height();

    return elementBottom >= viewportTop && elementTop <= viewportBottom;
  };

  // infinite scrolling
  let $content = $('#content');
  let $newsFeed = $('#newsFeed');
  let $lastItem = $('#newsFeed > li:last-of-type');

  let newsFeedEmpty = false;
  let ajaxInProgress = false;
  let page = 2;

  $content.on('scroll', function () {
    let $lastItem = $('#newsFeed > li:last-of-type');

    if (!ajaxInProgress && !newsFeedEmpty && $lastItem.isInViewport()) {
      ajaxInProgress = true;

      $.ajax('/news-feed/', {
        'data': {
          'page': page,
        },
        'success': function (response) {
          $newsFeed.append(response);
          page++;
          ajaxInProgress = false;
        },
        'statusCode': {
          204: function () {
            $newsFeed.append('<li class="empty-card">No more items to display.</li>');
            newsFeedEmpty = true;
            ajaxInProgress = false;
          }
        }
      });
    }
  });
});
