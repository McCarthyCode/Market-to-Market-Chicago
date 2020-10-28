$(() => {
  // Initialize datetime picker
  $("#dateStart").datetimepicker();
  $("#dateEnd").datetimepicker();
  $("#endsOn").datetimepicker();

  // Hide End Date/Time on All Day checked
  $('#allDay').change(() => $('#dateEndInputGroup').slideToggle(500));

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
