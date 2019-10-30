$(document).ready(() => {
  console.log('This site brought to you by McCarthy Web Design.');
  console.log('https://mccarthywebdesign.com/');

  var breakpointMd = 768;

  $('#navbarMenuButton').click(() => {
    $('#navbarCollapse').slideToggle();
  });

  let hidden = false;
  function showHideFooter() {
    let $footer = $('footer.footer');
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
          'bottom': '-62px',
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
});
