$(document).ready(() => {
  console.log('This site brought to you by McCarthy Web Design.');
  console.log('https://mccarthywebdesign.com/');

  $('a.external-link')
    .after(' <i class="fas fa-external-link-alt" title="External Link"></i>');
});