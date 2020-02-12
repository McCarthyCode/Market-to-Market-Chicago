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

  // infinite scrolling and scroll to top
  let $content = $('#content');
  let $articles = $('#articles');
  let $lastArticle = $articles.find('article:last-of-type');

  let categorySlug = $('input[name="category-slug"]').val();
  let articlesEmpty = false;
  let ajaxInProgress = false;
  let page = 2;

  $content.on('scroll', function () {
    // infinite scrolling
    $lastArticle = $articles.find('article:last-of-type');

    if (!ajaxInProgress && !articlesEmpty && $lastArticle.isInViewport()) {
      ajaxInProgress = true;

      $.ajax('/articles/by-page/', {
        'data': {
          'page': page,
          'category': categorySlug,
        },
        'success': function (response) {
          $articles.append(response);
          page++;
          ajaxInProgress = false;
        },
        'statusCode': {
          204: function () {
            $articles.append('<p class="empty-card">No more articles to display.</p>');
            articlesEmpty = true;
            ajaxInProgress = false;
          }
        }
      });
    }

    // // scroll to top display
    // let $scrollToTop = $('#scrollToTop');

    // if ($content.scrollTop() >= 160) {
    //   $scrollToTop.slideDown();
    // } else {
    //   $scrollToTop.slideUp();
    // }
  });
});