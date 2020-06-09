$(document).ready(() => {
  // Show/hide Dashboard items
  $('.container > div > .h3').click(function () {
    let $h3 = $(this);

    $h3.siblings(':not(:first-child)').slideToggle(500, function () {
      $h3.find('i')
        .toggleClass('fa-chevron-up').toggleClass('fa-chevron-down');
    });
  });
});
