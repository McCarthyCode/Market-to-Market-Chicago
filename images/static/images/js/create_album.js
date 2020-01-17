$(document).ready(() => {
  // Show/hide Create Album form
  $('#createAlbum .h3').click(function () {
    $('#createAlbumForm').slideToggle(500, function () {
      $('#createAlbum .h3 i')
        .toggleClass('fa-chevron-up').toggleClass('fa-chevron-down');
    });
  });
});
