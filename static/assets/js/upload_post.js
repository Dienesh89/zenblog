// getting the elements in which i have to take the live Preview
let thumbnail = document.getElementById("post-thumbnail")
let title = document.getElementById("title")
let desc = document.getElementById("desc")
let category = document.getElementById("category")

// getting the elements in which i have to show the live Preview
let prevThumbnail = document.getElementById("prevThumbnail")
let prevTitle = document.getElementById("prevTitle")
let prevDesc = document.getElementById("prevDesc")
let prevCategory = document.getElementById("prevCategory")

// thumbnail
thumbnail.addEventListener("change",(e)=>{
    e.preventDefault();
    image = document.getElementById("post-thumbnail").files[0];
    
    const formData = new FormData();
    formData.append('image', image);
    
    fetch('/post-images/', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            // Handle the response from the server
            if (data.success) {
                prevThumbnail.innerHTML = `
                <img src="${window.location.origin + data.image_url}" class="img-fluid">
                `
            } else {
                console.log(data.error);
            }
        })
        .catch(error => {
            console.log(error);
        });
})
// title
title.addEventListener("input",()=>{
    prevTitle.innerHTML = title.value
})

// Desc
desc.addEventListener("input",()=>{
    prevDesc.innerHTML = desc.value
})

// Category
category.addEventListener("change",()=>{
    prevCategory.innerHTML = category.value
})

// displaying the date
const months = ["JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"];
const date = new Date();
const month = months[date.getMonth()];
const day = date.getDate();
const year = date.getFullYear().toString().slice(-2);
let suffix = "TH";

if (day === 1 || day === 21 || day === 31) {
  suffix = "ST";
} else if (day === 2 || day === 22) {
  suffix = "ND";
} else if (day === 3 || day === 23) {
  suffix = "RD";
}

const formattedDate = `${month} ${day}${suffix} '${year}`;
document.getElementById("date").innerHTML = formattedDate
