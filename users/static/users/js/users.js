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
  let $locationCollapse = $('#locationCollapse');
  $('#locationToggle').click(() => $locationCollapse.slideToggle(500));

  // Search for existing locations;
  // select from autocomplete list on arrow key event
  let $locationId = $('#locationId');
  let $locationName = $('#locationName');

  let position = -1;
  let length = 0;
  let $locationAutocomplete = $('#locationAutocomplete');

  $locationName.on('input', function (event) {
    $('#locationAutocomplete ul').remove();

    let text = $(this).val();
    if (text === '') {
      $locationId.val(0);
    } else {
      $.get('/events/locations', {'q': text}, function (response) {
        $locationAutocomplete.append(response);

        length = $('#locationAutocomplete li').length;
        position = -1;
      });
    }
  });

  // Select from autocomplete from arrow or enter key event
  $locationName.keydown(function (event) {
    switch (event.keyCode) {
      case 13: // enter
        event.preventDefault();
        console.log('enter');
        let $active = $('#locationAutocomplete li.active');
        if ($('#locationAutocomplete li').length === 1) {
          $active = $('#locationAutocomplete li:first-child');
        }
        $locationId.val($active.data('id'));
        $locationName.val($active.text());

        $('#locationAutocomplete ul').remove();
        $locationCollapse.slideUp();
        break;

      case 38: // arrow up
        console.log('arrow up');
        position = position === -1 ? length - 1 : (position + 1) % length;
        $('#locationAutocomplete li').removeClass('active');
        $(`#locationAutocomplete li:nth-child(${position + 1})`).addClass('active');
        break;

      case 40: // arrow down
        console.log('arrow down');
        position = position === -1 ? 0 : (position + length - 1) % length;
        $('#locationAutocomplete li').removeClass('active');
        $(`#locationAutocomplete li:nth-child(${position + 1})`).addClass('active');
        break;
    }
  });

  // Select from autocomplete from click event
  $locationAutocomplete.on('click', 'ul li', function () {
    $locationId.val($(this).data('id'));
    $locationName.val($(this).text());

    $('#locationAutocomplete ul').remove();
  });

  // Show new location form if existing location is not selected
  $locationName.focusout(function () {
    if (Number($locationId.val()) === 0) {
      $locationCollapse.slideDown();
    }
  });
});
