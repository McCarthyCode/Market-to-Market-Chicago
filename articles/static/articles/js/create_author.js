$(document).ready(() => {
  // Show/hide Create Author form
  $('#createAuthor .h3').click(function () {
    $('#createAuthorForm').slideToggle(500, function () {
      $('#createAuthor .h3 i')
        .toggleClass('fa-chevron-up').toggleClass('fa-chevron-down');
    });
  });
});
