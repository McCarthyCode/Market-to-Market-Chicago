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
  let deleteFormActive = false;
  $updateTitleButton.click(() => {
    deleteFormActive = false;

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
    deleteFormActive = false;

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
    deleteFormActive = true;

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

  // Toggle checkboxes on image click when delete form is active
  $('#album a').click(function (event) {
    if (deleteFormActive) {
      event.preventDefault();

      let $element = $(this);
      let id = $element.data('id');
      let $checkbox = $(`#deleteImagesForm input[name="images"][value="${id}"]`);

      $element.toggleClass('active');
      $checkbox.prop('checked', !$checkbox.prop('checked'));
    }
  });
});
