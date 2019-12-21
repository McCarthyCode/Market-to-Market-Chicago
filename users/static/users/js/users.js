$(document).ready(() => {
  // Initialize datetime picker
  $("#dateStart").datetimepicker();
  $("#dateEnd").datetimepicker();
  $("#endsOn").datetimepicker();

  // Show/hide Create Event form
  $('#addEvent .h3').click(function () {
    $('#addEventForm').slideToggle(500);

    setTimeout(() => {
      $('#addEvent .h3 i')
        .toggleClass('fa-chevron-up').toggleClass('fa-chevron-down');
    }, 500);
  });

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
    let $endsOnContainer = $('#endsOnContainer');
    let $endsOnInput = $('#endsOnInput');
    let $endsAfter = $('#endsAfter');

    switch (value) {
      default:
      case 0:
        $endsOnInput.prop('required', false);
        $endsAfter.prop('required', false);

        $endsOnContainer.slideUp(500);
        $endsAfter.slideUp(500);
        break;

      case 1:
        $endsOnInput.prop('required', true);
        $endsAfter.prop('required', false);

        if ($endsAfter.is(':visible')) {
          $endsAfter.slideUp(500);
          setTimeout(() => {
            $endsOnContainer.slideDown(500);
          }, 500);
        } else {
          $endsOnContainer.slideDown(500);
        }
        break;

      case 2:
        $endsOnInput.prop('required', false);
        $endsAfter.prop('required', true);

        if ($endsOnContainer.is(':visible')) {
          $endsOnContainer.slideUp();
          setTimeout(() => {
            $endsAfter.slideDown(500);
          }, 500);
        } else {
          $endsAfter.slideDown(500);
        }
        break;
    }
  });

  // Show/hide new location input
  let $locationId = $('#locationId');
  let $locationName = $('#locationName');
  let $locationCollapse = $('#locationCollapse');
  let $locationAddress1 = $('#locationCollapse input[name="address1"]');
  let $locationCity = $('#locationCollapse input[name="city"]');
  let $locationState = $('#locationCollapse input[name="state"]');

  function locationExpand() {
    $locationCollapse.slideDown(500);

    $locationName.prop('required', true);
    $locationAddress1.prop('required', true);
    $locationCity.prop('required', true);
    $locationState.prop('required', true);
  }

  function locationContract() {
    $locationCollapse.slideUp(500);

    $locationName.prop('required', false);
    $locationAddress1.prop('required', false);
    $locationCity.prop('required', false);
    $locationState.prop('required', false);
  }

  function locationToggle() {
    if ($locationCollapse.is(':visible')) {
      locationContract();
    } else {
      locationExpand();
    }
  }

  $('#locationToggle').click(locationToggle);

  // Search for existing locations;
  // select from autocomplete list on arrow key event
  let position = -1;
  let length = 0;
  let $locationAutocomplete = $('#locationAutocomplete');

  $locationName.on('input', function (event) {
    $('#locationAutocomplete ul').remove();

    $locationId.val(0);

    let text = $(this).val();
    if (text !== '') {
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
        let $active = $('#locationAutocomplete li.active');
        if ($('#locationAutocomplete li').length === 1) {
          $active = $('#locationAutocomplete li:first-child');
        }
        $locationId.val($active.data('id'));
        $locationName.val($active.text());

        $('#locationAutocomplete ul').remove();
        locationContract();
        break;

      case 38: // arrow up
        position = position === -1 ? length - 1 : (position + 1) % length;
        $('#locationAutocomplete li').removeClass('active');
        $(`#locationAutocomplete li:nth-child(${position + 1})`).addClass('active');
        break;

      case 40: // arrow down
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
    locationContract();
  });
});
