$(() => {
  const breakpointMd = 768;

  console.log('This site brought to you by McCarthy Code.');
  console.log('https://mccarthycode.com/');

  // external link icon
  $('a.external-link').after(
    ' <i class="fas fa-external-link-alt" title="External Link"></i>',
  );

  // navbar menu
  $('#navbarMenuButton').on('click', () => {
    $('#navbarCollapse').slideToggle();
  });
  $(window).on('resize orientationchange', () => {
    if ($(this).width() >= breakpointMd) {
      $('#navbarCollapse').css('display', 'inline');
    } else {
      $('#navbarCollapse').hide();
    }
  });

  // custom radios and checkboxes
  $('input[type="checkbox"], input[type="radio"]').each(function () {
    $(this)
      .after($(`<span class="${$(this).attr('type')}">`))
      .parent('.input-group-append')
      .css({ cursor: 'pointer' })
      .on('click', function (event) {
        const $element = $(this).children(':first-child');
        const type = $element.attr('type');

        if (type === 'checkbox') {
          $element.attr('checked', !$element.attr('checked'));
        } else if (type === 'radio') {
          $element.attr('checked', true);
        }
      });
  });

  // scrolling footer
  let hidden = false;
  function showHideFooter() {
    let $footer = $('#footer');
    let width = $(window).width();
    let position = $('#content').scrollTop();

    if (width < breakpointMd) {
      if (position === 0 && hidden) {
        // similar to $footer.show();
        $footer.animate({ bottom: '0px' }, 500);
        hidden = false;
      } else if (position !== 0 && !hidden) {
        // similar to $footer.hide();
        $footer.animate({ bottom: '-49px' }, 500);
        hidden = true;
      }
    } else {
      hidden = false;
      $footer.css('bottom', '0px');
      $footer.show();
    }
  }

  $(window).on('scroll resize orientationchange', showHideFooter);
  $('#content').scroll(showHideFooter);
});
