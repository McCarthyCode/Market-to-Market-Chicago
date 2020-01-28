$(document).ready(() => {
  // Populate hidden input with album value
  let $id_album = $('#id_album');
  let $id_album_id = $('#id_album_id');

  let id = Number($id_album.val());
  $id_album_id.val(id);

  // Populate album title with hidden value, or empty string if none
  if (id === 0) {
    $id_album.val('');
  } else {
    let $albumTitle = $('#albumTitle')
    $id_album.val($albumTitle.val());
  }
});
