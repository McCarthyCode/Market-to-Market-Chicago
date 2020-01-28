$(document).ready(() => {
  // Show/hide Create Article form
  $('#createArticle .h3').click(function () {
    $('#createArticleForm').slideToggle(500, function () {
      $('#createArticle .h3 i')
        .toggleClass('fa-chevron-up').toggleClass('fa-chevron-down');
    });
  });
});
