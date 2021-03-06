$(() => {
  // Search for existing neighborhoods;
  // select from autocomplete list on arrow key event
  let neighborhoodPosition = -1;
  let neighborhoodLength = 0;
  let $neighborhoodName = $('#id_neighborhood');
  let $neighborhoodId = $('#id_neighborhood_id');
  let $neighborhoodAutocomplete = $('#neighborhoodAutocompleteLocation');

  $neighborhoodName.on('input', function (event) {
    $('#neighborhoodAutocompleteLocation ul').remove();

    $neighborhoodId.val(0);

    let text = $(this).val();
    if (text !== '') {
      $.get('/neighborhoods/autocomplete', {'q': text}, function (response) {
        $neighborhoodAutocomplete.append(response);

        neighborhoodPosition = -1;
        neighborhoodLength = $('#neighborhoodAutocompleteLocation li').length;
      });
    }
  });

  // Select from autocomplete from arrow or enter key event
  $neighborhoodName.keydown(function (event) {
    switch (event.keyCode) {
      case 13: // enter
        event.preventDefault();
        let $active = $('#neighborhoodAutocompleteLocation li.active');
        if ($('#neighborhoodAutocompleteLocation li').length === 1) {
          $active = $('#neighborhoodAutocompleteLocation li:first-child');
        }
        $neighborhoodId.val($active.data('id'));
        $neighborhoodName.val($active.text());

        $('#neighborhoodAutocompleteLocation ul').remove();
        break;

      case 38: // arrow up
        neighborhoodPosition = neighborhoodPosition === -1 ? neighborhoodLength - 1 : (neighborhoodPosition - 1 + neighborhoodLength) % neighborhoodLength;
        $('#neighborhoodAutocompleteLocation li').removeClass('active');
        $(`#neighborhoodAutocompleteLocation li:nth-child(${neighborhoodPosition + 1})`).addClass('active');
        break;

      case 40: // arrow down
        neighborhoodPosition = neighborhoodPosition === -1 ? 0 : (neighborhoodPosition + 1) % neighborhoodLength;
        $('#neighborhoodAutocompleteLocation li').removeClass('active');
        $(`#neighborhoodAutocompleteLocation li:nth-child(${neighborhoodPosition + 1})`).addClass('active');
        break;
    }
  });

  // Select from autocomplete from click event
  $neighborhoodAutocomplete.on('click', 'ul li', function () {
    $neighborhoodId.val($(this).data('id'));
    $neighborhoodName.val($(this).text());

    $('#neighborhoodAutocompleteLocation ul').fadeOut(500, function () {
      $(this).remove();
    });
  });

  // Remove autocomplete list on focusout
  $neighborhoodName.focusout(function () {
    $('#neighborhoodAutocompleteLocation ul').fadeOut(500, function () {
      $(this).remove();
    });
  });

  // Hide no kitchen option for choices other than Nightlife & Restaurants
  let $category = $('select#id_category');
  let $noKitchenContainer = $('#noKitchenContainer');
  let $noKitchen = $('#id_no_kitchen');
  let checked = false;

  $category.on('change', function () {
    let value = Number(this.value);

    if (value === 0 || value === 2) {
      if (checked) {
        $noKitchen.prop('checked', true);
      }
      $noKitchenContainer.slideDown();
      $noKitchen.prop('disabled', false);
    } else {
      checked = $noKitchen.is(':checked');
      $noKitchenContainer.slideUp();
      $noKitchen.prop('disabled', true);
      $noKitchen.prop('checked', false);
    }
  });
});
