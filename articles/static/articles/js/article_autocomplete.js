$(document).ready(() => {
  // Search for existing authors;
  // select from autocomplete list on arrow key event
  let authorPosition = -1;
  let authorLength = 0;
  let $authorAutocomplete = $('#authorAutocomplete');
  let $authorName = $('#id_author');
  let $authorId = $('#id_author_id');

  $authorName.on('input', function (event) {
    $('#authorAutocomplete ul').remove();

    $authorId.val(0);

    let text = $(this).val();
    if (text !== '') {
      $.get('/authors/autocomplete', {'q': text}, function (response) {
        $authorAutocomplete.append(response);

        authorPosition = -1;
        authorLength = $('#authorAutocomplete li').length;
      });
    }
  });

  // Select from autocomplete from arrow or enter key event
  $authorName.keydown(function (event) {
    switch (event.keyCode) {
      case 13: // enter
        event.preventDefault();
        let $active = $('#authorAutocomplete li.active');
        if ($('#authorAutocomplete li').length === 1) {
          $active = $('#authorAutocomplete li:first-child');
        }
        $authorId.val($active.data('id'));
        $authorName.val($active.text());

        $('#authorAutocomplete ul').remove();
        break;

      case 38: // arrow up
        authorPosition = authorPosition === -1 ? authorLength - 1 : (authorPosition - 1 + authorLength) % authorLength;
        $('#authorAutocomplete li').removeClass('active');
        $(`#authorAutocomplete li:nth-child(${authorPosition + 1})`).addClass('active');
        break;

      case 40: // arrow down
        authorPosition = authorPosition === -1 ? 0 : (authorPosition + 1) % authorLength;
        $('#authorAutocomplete li').removeClass('active');
        $(`#authorAutocomplete li:nth-child(${authorPosition + 1})`).addClass('active');
        break;
    }
  });

  // Select from autocomplete from click event
  $authorAutocomplete.on('click', 'ul li', function () {
    $authorId.val($(this).data('id'));
    $authorName.val($(this).text());

    $('#authorAutocomplete ul').fadeOut(500, function () {
      $(this).remove();
    });
  });

  // Remove autocomplete list on focusout
  $authorName.focusout(function () {
    $('#authorAutocomplete ul').fadeOut(500, function () {
      $(this).remove();
    });
  });

  // Search for existing albums;
  // select from autocomplete list on arrow key event
  let albumPosition = -1;
  let albumLength = 0;
  let $albumAutocomplete = $('#albumAutocomplete');
  let $albumTitle = $('#id_album');
  let $albumId = $('#id_album_id');

  $albumTitle.on('input', function (event) {
    $('#albumAutocomplete ul').remove();

    $albumId.val(0);

    let text = $(this).val();
    if (text !== '') {
      $.get('/images/autocomplete', {'q': text}, function (response) {
        $albumAutocomplete.append(response);

        albumPosition = -1;
        albumLength = $('#albumAutocomplete li').length;
      });
    }
  });

  // Select from autocomplete from arrow or enter key event
  $albumTitle.keydown(function (event) {
    switch (event.keyCode) {
      case 13: // enter
        event.preventDefault();
        let $active = $('#albumAutocomplete li.active');
        if ($('#albumAutocomplete li').length === 1) {
          $active = $('#albumAutocomplete li:first-child');
        }
        $albumId.val($active.data('id'));
        $albumTitle.val($active.text());

        $('#albumAutocomplete ul').remove();
        break;

      case 38: // arrow up
        albumPosition = albumPosition === -1 ? albumLength - 1 : (albumPosition - 1 + albumLength) % albumLength;
        $('#albumAutocomplete li').removeClass('active');
        $(`#albumAutocomplete li:nth-child(${albumPosition + 1})`).addClass('active');
        break;

      case 40: // arrow down
        albumPosition = albumPosition === -1 ? 0 : (albumPosition + 1) % albumLength;
        $('#albumAutocomplete li').removeClass('active');
        $(`#albumAutocomplete li:nth-child(${albumPosition + 1})`).addClass('active');
        break;
    }
  });

  // Select from autocomplete from click event
  $albumAutocomplete.on('click', 'ul li', function () {
    $albumId.val($(this).data('id'));
    $albumTitle.val($(this).text());

    $('#albumAutocomplete ul').fadeOut(500, function () {
      $(this).remove();
    });
  });

  // Remove autocomplete list on focusout
  $albumTitle.focusout(function () {
    $('#albumAutocomplete ul').fadeOut(500, function () {
      $(this).remove();
    });
  });
});
