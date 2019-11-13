$(document).ready(() => {
  let breakpointMd = 768;

  let hidden = false;
  function showHideFooter() {
    let $footer = $('#footer');
    let width = $(window).width();
    let position = $('#content').scrollTop();

    if (width < breakpointMd) {
      if (position === 0 && hidden) {
        // similar to $footer.show();
        $footer.animate({
          'bottom': '0px',
        }, 500);

        hidden = !hidden;
      } else if (position !== 0 && !hidden) {
        // similar to $footer.hide();
        $footer.animate({
          'bottom': '-49px',
        }, 500);

        hidden = !hidden;
      }
    } else {
      $footer.css('bottom', '0px');
      $footer.show();
    }
  }

  $(window).on('scroll resize orientationchange', showHideFooter);
  $('#content').scroll(showHideFooter);

  $(window).on('resize orientationchange', () => {
    if ($(this).width() >= breakpointMd) {
      $('#navbarCollapse').css('display', 'inline');
    } else {
      $('#navbarCollapse').hide();
    }
  });
});
