$(document).ready(() => {
  // Initialize datetime picker
  $("#dateStart").datetimepicker();
  $("#dateEnd").datetimepicker();
  // $("#endsOn").datetimepicker();

  // Hide End Date/Time on All Day checked
  $('#allDay').change(() => $('#dateEndInputGroup').slideToggle(500));

  // // Show/hide advanced repeat options
  // $('#advancedRepeatToggle').click((event) => {
  //   event.preventDefault();
  //   event.stopPropagation();

  //   $('#advancedRepeatCollapse').slideToggle(500);

  //   setTimeout(() => {
  //     $('#advancedRepeatToggle i')
  //       .toggleClass('fa-chevron-down').toggleClass('fa-chevron-up');
  //   }, 500);
  // });

  // // Simulate hover on mouseenter/mouseleave
  // let $weekdayListLabel = $('#weekdayList label');
  // $weekdayListLabel.on('mouseenter mouseleave', function (event) {
  //   switch (event.type) {
  //     case 'mouseenter':
  //       $(this).addClass('hover');
  //       break;

  //     case 'mouseleave':
  //       $(this).removeClass('hover');
  //       break;
  //   }
  // });

  // // Make labels active when corresponding checkbox is checked
  // $('#weekdayList label').click(function (event) {
  //   event.stopPropagation();

  //   $(this).toggleClass('active');
  // });

  // // Show appropriate input based on #ends dropdown
  // let $ends = $('#ends');
  // $ends.change(() => {
  //   let value = Number($ends.val());
  //   let $endsOnContainer = $('#endsOnContainer');
  //   let $endsOnInput = $('#endsOnInput');
  //   let $endsAfter = $('#endsAfter');

  //   switch (value) {
  //     default:
  //     case 0:
  //       $endsOnInput.prop('required', false);
  //       $endsAfter.prop('required', false);

  //       $endsOnContainer.slideUp(500);
  //       $endsAfter.slideUp(500);
  //       break;

  //     case 1:
  //       $endsOnInput.prop('required', true);
  //       $endsAfter.prop('required', false);

  //       if ($endsAfter.is(':visible')) {
  //         $endsAfter.slideUp(500);
  //         setTimeout(() => {
  //           $endsOnContainer.slideDown(500);
  //         }, 500);
  //       } else {
  //         $endsOnContainer.slideDown(500);
  //       }
  //       break;

  //     case 2:
  //       $endsOnInput.prop('required', false);
  //       $endsAfter.prop('required', true);

  //       if ($endsOnContainer.is(':visible')) {
  //         $endsOnContainer.slideUp();
  //         setTimeout(() => {
  //           $endsAfter.slideDown(500);
  //         }, 500);
  //       } else {
  //         $endsAfter.slideDown(500);
  //       }
  //       break;
  //   }
  // });

  // // Show/hide new location input
  // let $locationId = $('#locationId');
  // let $locationName = $('#locationName');
  // let $locationCategory = $('#locationCategory');
  // let $neighborhoodId = $('#neighborhoodId');
  // let $neighborhoodName = $('#neighborhoodName');
  // let $locationCollapse = $('#locationCollapse');
  // let $locationAddress1 = $('#locationCollapse input[name="address1"]');
  // let $locationCity = $('#locationCollapse input[name="city"]');
  // let $locationState = $('#locationCollapse input[name="state"]');

  // function locationExpand() {
  //   $locationCollapse.slideDown(500);

  //   $neighborhoodName.prop('required', true);
  //   $locationCategory.prop('required', true);
  //   $locationAddress1.prop('required', true);
  //   $locationCity.prop('required', true);
  //   $locationState.prop('required', true);
  // }

  // function locationContract() {
  //   $locationCollapse.slideUp(500);

  //   $neighborhoodName.prop('required', false);
  //   $locationCategory.prop('required', false);
  //   $locationAddress1.prop('required', false);
  //   $locationCity.prop('required', false);
  //   $locationState.prop('required', false);
  // }

  // function locationToggle() {
  //   if ($locationCollapse.is(':visible')) {
  //     locationContract();
  //   } else {
  //     locationExpand();
  //   }
  // }

  // $('#locationToggle').click(locationToggle);

  // Search for existing locations;
  // select from autocomplete list on arrow key event
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
        locationContract();
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
    locationContract();
  });

  // Remove autocomplete list on focusout
  $locationName.focusout(function () {
    $('#locationAutocomplete ul').fadeOut(500, function () {
      $(this).remove();
    });
  });

  // // Search for existing neighborhoods;
  // // select from autocomplete list on arrow key event
  // let neighborhoodPosition = -1;
  // let neighborhoodLength = 0;
  // let $neighborhoodAutocomplete = $('#neighborhoodAutocomplete');

  // $neighborhoodName.on('input', function (event) {
  //   $('#neighborhoodAutocomplete ul').remove();

  //   $neighborhoodId.val(0);

  //   let text = $(this).val();
  //   if (text !== '') {
  //     $.get('/neighborhoods/autocomplete', {'q': text}, function (response) {
  //       $neighborhoodAutocomplete.append(response);

  //       neighborhoodPosition = -1;
  //       neighborhoodLength = $('#neighborhoodAutocomplete li').length;
  //     });
  //   }
  // });

  // // Select from autocomplete from arrow or enter key event
  // $neighborhoodName.keydown(function (event) {
  //   switch (event.keyCode) {
  //     case 13: // enter
  //       event.preventDefault();
  //       let $active = $('#neighborhoodAutocomplete li.active');
  //       if ($('#neighborhoodAutocomplete li').length === 1) {
  //         $active = $('#neighborhoodAutocomplete li:first-child');
  //       }
  //       $neighborhoodId.val($active.data('id'));
  //       $neighborhoodName.val($active.text());

  //       $('#neighborhoodAutocomplete ul').remove();
  //       break;

  //     case 38: // arrow up
  //       neighborhoodPosition = neighborhoodPosition === -1 ? neighborhoodLength - 1 : (neighborhoodPosition - 1 + neighborhoodLength) % neighborhoodLength;
  //       $('#neighborhoodAutocomplete li').removeClass('active');
  //       $(`#neighborhoodAutocomplete li:nth-child(${neighborhoodPosition + 1})`).addClass('active');
  //       break;

  //     case 40: // arrow down
  //       neighborhoodPosition = neighborhoodPosition === -1 ? 0 : (neighborhoodPosition + 1) % neighborhoodLength;
  //       $('#neighborhoodAutocomplete li').removeClass('active');
  //       $(`#neighborhoodAutocomplete li:nth-child(${neighborhoodPosition + 1})`).addClass('active');
  //       break;
  //   }
  // });

  // // Select from autocomplete from click event
  // $neighborhoodAutocomplete.on('click', 'ul li', function () {
  //   $neighborhoodId.val($(this).data('id'));
  //   $neighborhoodName.val($(this).text());

  //   $('#neighborhoodAutocomplete ul').fadeOut(500, function () {
  //     $(this).remove();
  //   });
  // });

  // // Remove autocomplete list on focusout
  // $neighborhoodName.focusout(function () {
  //   $('#neighborhoodAutocomplete ul').fadeOut(500, function () {
  //     $(this).remove();
  //   });
  // });
});
