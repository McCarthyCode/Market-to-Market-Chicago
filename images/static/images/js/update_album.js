$(document).ready(() => {
  // Buttons
  let $updateTitleButton = $('#updateTitleButton');
  let $addImagesButton = $('#addImagesButton');
  let $deleteImagesButton = $('#deleteImagesButton');

  // Cards
  let $updateTitle = $('#updateTitle');
  let $addImages = $('#addImages');
  let $deleteImages = $('#deleteImages');

  // Pre-populate title form
  $('#id_title').val($('.h1').text());

  // Show/hide forms on button click
  $updateTitleButton.click(() => {
    if ($updateTitle.is(':visible')) {
      $updateTitle.slideUp(500);
    } else if ($addImages.is(':visible')) {
      $addImages.slideUp(500, () => $updateTitle.slideDown(500));
    } else if ($deleteImages.is(':visible')) {
      $deleteImages.slideUp(500, () => $updateTitle.slideDown(500));
    } else {
      $updateTitle.slideDown(500);
    }
  });
  $addImagesButton.click(() => {
    if ($updateTitle.is(':visible')) {
      $updateTitle.slideUp(500, () => $addImages.slideDown(500));
    } else if ($addImages.is(':visible')) {
      $addImages.slideUp(500);
    } else if ($deleteImages.is(':visible')) {
      $deleteImages.slideUp(500, () => $addImages.slideDown(500));
    } else {
      $addImages.slideDown(500);
    }
  });
  $deleteImagesButton.click(() => {
    if ($updateTitle.is(':visible')) {
      $updateTitle.slideUp(500, () => $deleteImages.slideDown(500));
    } else if ($addImages.is(':visible')) {
      $addImages.slideUp(500, () => $deleteImages.slideDown(500));
    } else if ($deleteImages.is(':visible')) {
      $deleteImages.slideUp(500);
    } else {
      $deleteImages.slideDown(500);
    }
  });
});
