tinymce.init({
  selector: '#id_body',
  mobile: {theme: 'mobile'},
  themes: 'modern',
  height: 480,
  menubar: false,
  plugins: [
    'advlist autolink autosave fullscreen help link lists paste preview searchreplace spellchecker table visualblocks wordcount'
  ],
  toolbar: 'fullscreen | undo redo | formatselect | spellchecker | bold italic underline | strikethrough  subscript superscript blockquote | link | forecolor backcolor | alignleft aligncenter alignright alignjustify | bullist numlist outdent indent | removeformat help',
  skin: 'mwd-dark',
  skin_url: '/static/lib/tinymce/skins/mwd-dark',
  content_css: [
    '/static/home/css/reset.min.css',
    '/static/home/css/tinyMCE.min.css',
  ],
});
