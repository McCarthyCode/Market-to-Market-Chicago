$(document).ready(() => {
  // Show/hide Create Invites form
  $('#createInvites .h3').click(function () {
    $('#createInvitesForm').slideToggle(500, function () {
      $('#createInvites .h3 i')
        .toggleClass('fa-chevron-up').toggleClass('fa-chevron-down');
    });
  });

  // Show/hide View Invites table
  $('#viewInvites .h3').click(function () {
    $('#viewInvitesTable').slideToggle(500, function () {
      $('#viewInvites .h3 i')
        .toggleClass('fa-chevron-up').toggleClass('fa-chevron-down');
    });
  });
});
