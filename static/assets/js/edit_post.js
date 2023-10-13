// tiny mc editor for editing blog content 

tinymce.init({
  selector: 'textarea',
  plugins: 'anchor autolink charmap codesample emoticons image link lists media searchreplace table visualblocks wordcount checklist mediaembed casechange export formatpainter pageembed linkchecker a11ychecker tinymcespellchecker permanentpen powerpaste advtable advcode editimage tinycomments tableofcontents footnotes mergetags autocorrect typography inlinecss',
  toolbar: 'undo redo | blocks fontfamily fontsize | bold italic underline strikethrough | link image media table mergetags | addcomment showcomments | spellcheckdialog a11ycheck typography | align lineheight | checklist numlist bullist indent outdent | emoticons charmap | removeformat',
  tinycomments_mode: 'embedded',
  tinycomments_author: 'Author name',
  mergetags_list: [
    { value: 'First.Name', title: 'First Name' },
    { value: 'Email', title: 'Email' },
  ],
});


let uploadPost = document.getElementById("upload-post")
// sending the data to the server when upload-ppst btn is clicked
document.getElementById("upload-post").addEventListener("click", (e) => {
    e.preventDefault();
    
    content = tinymce.activeEditor.getContent()
    
    const formData = new FormData();
    formData.append('code', content);

    fetch(window.location.pathname, {
            method: "POST",
            body: formData
        }).then(response => response.json())
        .then(data => {
            alert("Your post has been uploaded.")
            location.href = window.location.origin
        })
})
