$(document).ready(function () {
  // Update category in dropdown list
  let category = $('#categoryHidden').val();

  $('#category').val(category).change();

  // Search for existing neighborhoods;
  // select from autocomplete list on arrow key event
  let $neighborhoodId = $('#neighborhoodId');
  let $neighborhoodName = $('#neighborhoodName');
  let $neighborhoodAutocomplete = $('#neighborhoodAutocomplete');

  let position = -1;
  let length = 0;

  $neighborhoodName.on('input', function (event) {
    $('#neighborhoodAutocomplete ul').remove();

    $neighborhoodId.val(0);

    let text = $(this).val();
    if (text !== '') {
      $.get('/neighborhoods/autocomplete', {'q': text}, function (response) {
        $neighborhoodAutocomplete.append(response);

        position = -1;
        length = $('#neighborhoodAutocomplete li').length;
      });
    }
  });

  // Select from autocomplete from arrow or enter key event
  $neighborhoodName.keydown(function (event) {
    switch (event.keyCode) {
      case 13: // enter
        event.preventDefault();
        let $active = $('#neighborhoodAutocomplete li.active');
        if ($('#neighborhoodAutocomplete li').length === 1) {
          $active = $('#neighborhoodAutocomplete li:first-child');
        }
        $neighborhoodId.val($active.data('id'));
        $neighborhoodName.val($active.text());

        $('#neighborhoodAutocomplete ul').remove();
        break;

      case 38: // arrow up
        position = position === -1 ? length - 1 : (position + 1) % length;
        $('#neighborhoodAutocomplete li').removeClass('active');
        $(`#neighborhoodAutocomplete li:nth-child(${position + 1})`).addClass('active');
        break;

      case 40: // arrow down
        position = position === -1 ? 0 : (position + length - 1) % length;
        $('#neighborhoodAutocomplete li').removeClass('active');
        $(`#neighborhoodAutocomplete li:nth-child(${position + 1})`).addClass('active');
        break;
    }
  });

  // Select from autocomplete from click event
  $neighborhoodAutocomplete.on('click', 'ul li', function () {
    $neighborhoodId.val($(this).data('id'));
    $neighborhoodName.val($(this).text());

    $('#neighborhoodAutocomplete ul').fadeOut(500, function () {
      $(this).remove();
    });
  });

  // Remove autocomplete list on focusout
  $neighborhoodName.focusout(function () {
    $('#neighborhoodAutocomplete ul').fadeOut(500, function () {
      $(this).remove();
    });
  });
});
