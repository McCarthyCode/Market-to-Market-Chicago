$(document).ready(() => {
  // Initialize datetime picker
  $("#dateStart").datetimepicker();
  $("#dateEnd").datetimepicker();
  $("#endsOn").datetimepicker();

  // Hide End Date/Time on All Day checked
  $('#allDay').change(() => $('#dateEndInputGroup').slideToggle(500));

  // Show/hide advanced repeat options
  $('#advancedRepeatToggle').click((event) => {
    event.preventDefault();
    event.stopPropagation();

    $('#advancedRepeatCollapse').slideToggle(500);

    setTimeout(() => {
      $('#advancedRepeatToggle i')
        .toggleClass('fa-chevron-down').toggleClass('fa-chevron-up');
    }, 500);
  });

  // Make labels active when corresponding checkbox is checked
  $('#weekdayList label').click(function (event) {
    event.stopPropagation();

    console.log($(this));
    $(this).toggleClass('active');
  });

  // Show appropriate input based on #ends dropdown
  let $ends = $('#ends');
  $ends.change(() => {
    let value = Number($ends.val());
    let $endsOn = $('#endsOn');
    let $endsAfter = $('#endsAfter');

    switch (value) {
      default:
      case 0:
        $endsOn.hide();
        $endsAfter.hide();
        break;
      case 1:
        $endsOn.css('display', 'flex');
        $endsAfter.hide();
        break;
      case 2:
        $endsOn.hide();
        $endsAfter.show();
        break;
    }
  });

  // Show/hide new location input
  $('#locationToggle').click(() => $('#locationCollapse').slideToggle(500));

  // Search for existing locations
  $('#locationName').on('input', () => {
    let text = $('#locationName').val();
    console.log(text);

    // $.get('/events/locations', {'q': text}, () => {

    // });
  });
});

// Make labels active when corresponding checkbox is checked
$('#weekdayList li label').click((event) => {
  event.stopPropagation();

  console.log($(this));
  $(this).children('label').toggleClass('active');
});
