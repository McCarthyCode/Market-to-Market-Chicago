tinymce.init({
  selector: '#id_body',
  mobile: { theme: 'mobile' },
  themes: 'modern',
  height: 480,
  menubar: false,
  plugins: [
    'advlist autolink autosave fullscreen help link lists paste preview searchreplace table visualblocks wordcount',
  ],
  toolbar:
    'fullscreen | undo redo | formatselect | bold italic underline | strikethrough  subscript superscript blockquote | link | forecolor backcolor | alignleft aligncenter alignright alignjustify | bullist numlist outdent indent | removeformat help',
  skin: 'mwd-dark',
  skin_url: '/static/lib/tinymce/skins/mwd-dark',
  content_css: [
    '/static/lib/reset/reset.min.css',
    '/static/global/css/tinyMCE.min.css',
  ],
});
