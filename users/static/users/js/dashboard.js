$(() => {
  // Show/hide Dashboard items
  $("#content h2").click(function () {
    let $h2 = $(this);

    $h2.siblings(":not(:first-child)").slideToggle(500, function () {
      $h2.find("i").toggleClass("fa-chevron-up").toggleClass("fa-chevron-down");
    });
  });
});
