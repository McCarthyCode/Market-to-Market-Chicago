$(document).ready(() => {
  // Populate hidden input with author value
  let $id_author = $('#id_author');
  let $id_author_id = $('#id_author_id');

  let id_author = Number($id_author.val());
  $id_author_id.val(id_author);

  // Populate author name with hidden value, or empty string if none
  if (id_author === 0) {
    $id_author.val('');
  } else {
    let $authorName = $('#authorName');
    $id_author.val($authorName.val());
  }

  // Populate hidden input with album value
  let $id_album = $('#id_album');
  let $id_album_id = $('#id_album_id');

  let id_album = Number($id_album.val());
  $id_album_id.val(id_album);

  // Populate album title with hidden value, or empty string if none
  if (id_album === 0) {
    $id_album.val('');
  } else {
    let $albumTitle = $('#albumTitle');
    $id_album.val($albumTitle.val());
  }
});
