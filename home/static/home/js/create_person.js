$(document).ready(() => {
  // Show/hide Create Person form
  $('#createPerson .h3').click(function () {
    $('#createPersonForm').slideToggle(500, function () {
      $('#createPerson .h3 i')
        .toggleClass('fa-chevron-up').toggleClass('fa-chevron-down');
    });
  });
});
