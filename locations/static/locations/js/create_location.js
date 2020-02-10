$(document).ready(() => {
  // Show/hide Create Location form
  $('#createLocation .h3').click(function () {
    $('#createLocationForm').slideToggle(500, function () {
      $('#createLocation .h3 i')
        .toggleClass('fa-chevron-up').toggleClass('fa-chevron-down');
    });
  });
});
