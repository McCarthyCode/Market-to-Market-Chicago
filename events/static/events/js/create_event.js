$(document).ready(() => {
  // Initialize datetime picker
  $("#dateStart").datetimepicker();
  $("#dateEnd").datetimepicker();
  $("#endsOn").datetimepicker();

  // Show/hide Create Event form
  $('#createEvent .h3').click(function () {
    $('#createEventForm').slideToggle(500, function () {
      $('#createEvent .h3 i')
        .toggleClass('fa-chevron-up').toggleClass('fa-chevron-down');
    });
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

  // Simulate hover on mouseenter/mouseleave
  let $weekdayListLabel = $('#weekdayList label');
  $weekdayListLabel.on('mouseenter mouseleave', function (event) {
    switch (event.type) {
      case 'mouseenter':
        $(this).addClass('hover');
        break;

      case 'mouseleave':
        $(this).removeClass('hover');
        break;
    }
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

  // Search for existing locations;
  // select from autocomplete list on arrow key event
  let $locationId = $('#locationId');
  let $locationName = $('#locationName');
  let locationPosition = -1;
  let locationLength = 0;
  let $locationAutocomplete = $('#locationAutocomplete');

  $locationName.on('input', function (event) {
    $('#locationAutocomplete ul').remove();

    $locationId.val(0);

    let text = $(this).val();
    if (text !== '') {
      $.get('/locations/autocomplete', {'q': text}, function (response) {
        $locationAutocomplete.append(response);

        locationPosition = -1;
        locationLength = $('#locationAutocomplete li').length;
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
        break;

      case 38: // arrow up
        locationPosition = locationPosition === -1 ? locationLength - 1 : (locationPosition - 1 + locationLength) % locationLength;
        $('#locationAutocomplete li').removeClass('active');
        $(`#locationAutocomplete li:nth-child(${locationPosition + 1})`).addClass('active');
        break;

      case 40: // arrow down
        locationPosition = locationPosition === -1 ? 0 : (locationPosition + 1) % locationLength;
        $('#locationAutocomplete li').removeClass('active');
        $(`#locationAutocomplete li:nth-child(${locationPosition + 1})`).addClass('active');
        break;
    }
  });

  // Select from autocomplete from click event
  $locationAutocomplete.on('click', 'ul li', function () {
    $locationId.val($(this).data('id'));
    $locationName.val($(this).text());

    $('#locationAutocomplete ul').fadeOut(500, function () {
      $(this).remove();
    });
  });

  // Remove autocomplete list on focusout
  $locationName.focusout(function () {
    $('#locationAutocomplete ul').fadeOut(500, function () {
      $(this).remove();
    });
  });

  // Search for existing albums;
  // select from autocomplete list on arrow key event
  let $albumId = $('#albumId');
  let $albumName = $('#albumName');
  let albumPosition = -1;
  let albumLength = 0;
  let $albumAutocompleteEvent = $('#albumAutocompleteEvent');

  $albumName.on('input', function (event) {
    $('#albumAutocompleteEvent ul').remove();

    $albumId.val(0);

    let text = $(this).val();
    if (text !== '') {
      $.get('/images/autocomplete', {'q': text}, function (response) {
        $albumAutocompleteEvent.append(response);

        albumPosition = -1;
        albumLength = $('#albumAutocompleteEvent li').length;
      });
    }
  });

  // Select from autocomplete from arrow or enter key event
  $albumName.keydown(function (event) {
    switch (event.keyCode) {
      case 13: // enter
        event.preventDefault();
        let $active = $('#albumAutocompleteEvent li.active');
        if ($('#albumAutocompleteEvent li').length === 1) {
          $active = $('#albumAutocompleteEvent li:first-child');
        }
        $albumId.val($active.data('id'));
        $albumName.val($active.text());

        $('#albumAutocompleteEvent ul').remove();
        break;

      case 38: // arrow up
        albumPosition = albumPosition === -1 ? albumLength - 1 : (albumPosition - 1 + albumLength) % albumLength;
        $('#albumAutocompleteEvent li').removeClass('active');
        $(`#albumAutocompleteEvent li:nth-child(${albumPosition + 1})`).addClass('active');
        break;

      case 40: // arrow down
        albumPosition = albumPosition === -1 ? 0 : (albumPosition + 1) % albumLength;
        $('#albumAutocompleteEvent li').removeClass('active');
        $(`#albumAutocompleteEvent li:nth-child(${albumPosition + 1})`).addClass('active');
        break;
    }
  });

  // Select from autocomplete from click event
  $albumAutocompleteEvent.on('click', 'ul li', function () {
    $albumId.val($(this).data('id'));
    $albumName.val($(this).text());

    $('#albumAutocompleteEvent ul').fadeOut(500, function () {
      $(this).remove();
    });
  });

  // Remove autocomplete list on focusout
  $albumName.focusout(function () {
    $('#albumAutocompleteEvent ul').fadeOut(500, function () {
      $(this).remove();
    });
  });
});
