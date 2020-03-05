$(document).ready(() => {
  // Show/hide Create Invites form
  $('#createInvites .h3').click(function () {
    $('#createInvitesForm').slideToggle(500, function () {
      $('#createInvites .h3 i')
        .toggleClass('fa-chevron-up').toggleClass('fa-chevron-down');
    });
  });
});
