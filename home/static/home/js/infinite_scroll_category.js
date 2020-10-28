$(() => {
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
  let $categoryFeed = $('#categoryFeed');
  let $lastItem = $categoryFeed.find('> li:last-of-type');

  let feedEmpty = false;
  let ajaxInProgress = false;
  let page = 2;

  $content.on('scroll', function () {
    $lastItem = $categoryFeed.find('> li:last-of-type');

    if (!ajaxInProgress && !feedEmpty && $lastItem.isInViewport()) {
      ajaxInProgress = true;

      $.ajax(`/${$('input[name="category-slug"]').val()}/${page}/`, {
        'success': function (response) {
          $categoryFeed.append(response);
          page++;
          ajaxInProgress = false;
        },
        'statusCode': {
          204: function () {
            $categoryFeed.append('<li class="empty-card">No more items to display.</li>');
            feedEmpty = true;
            ajaxInProgress = false;
          }
        }
      });
    }
  });
});