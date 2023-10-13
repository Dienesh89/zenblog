let searchForm = document.getElementById("searchForm");
let form = document.getElementsByClassName("search-form")[0];
let ShownPosts = [];
let animation = document.getElementById("posts-animation")
let posts_container = document.getElementById("posts-container")
   

searchForm.addEventListener("keypress",(e)=>{
    e.preventDefault();
    if (e.key == "Enter"){
        ShownPosts = []
        searchPost(searchForm.value)
        posts_container.innerHTML = ""
        // window.removeEventListener("scroll",scrollFunc)
    }
})

const searchNotFound = (searchProblem)=>{
    not_found_html = `
	<div class="container mt-5">
		<div class="jumbotron text-center">
			<h1 class="display-4">No Results Found</h1>
			<p class="lead">${searchProblem}</p>
			<hr class="my-4">
			<p>Try modifying your search query or check back later for updated content.</p>
			<a class="btn btn-primary btn-lg mt-3" href="/" role="button">Go Back Home</a>
		</div>
	</div>
    `
    
    posts_container.innerHTML = ""
    posts_container.innerHTML = not_found_html
}

const scrollFunc = (e)=>{
        e.preventDefault();
        let scrollPosition = window.pageYOffset;
        let pageHeight = document.documentElement.scrollHeight;
        let viewportHeight = window.innerHeight;
        let threshold = pageHeight - viewportHeight // - beforeHeight;
    
        if (scrollPosition >= threshold && !functionHasRun) {
            searchPost(searchForm.value)
            // beforeHeight = beforeHeight + 100
            functionHasRun = true;
        }

        if (scrollPosition < threshold) {
            functionHasRun = false;
        }
            
           
}

const searchPost = (q)=>{
    let Addanimation = `
    <div class="text-center" id="posts-animation">
        <div class="spinner-border" role="status"></div>
    </div>
    `
    
    const formData = new FormData();
    let usedPosts = ShownPosts
    
    formData.append("shown_posts", JSON.stringify(usedPosts));
    formData.append("query",q)
    
    let search = fetch("/search/",{method:"POST",body:formData})
    search.then(response => response.json())
    .then(data => {
        if (data.posts_not_found){
            animation = document.getElementById("posts-animation")
            if (animation == null){}
            else{
                animation.remove()
            }
            
            if (ShownPosts.length<1){
                if (searchForm.value.length>99){
                    searchNotFound(`we're sorry,but your search query <b>${searchForm.value.split(" ")[0]}...</b> exceeds the limit of 99 characters.`)
                }
                else{
                    searchNotFound("Sorry, we couldn't find any documents that match your search.")
                }
            }
        }
        else{
            
            window.addEventListener("scroll",scrollFunc)
            
            animation = document.getElementById("posts-animation")
            if (animation == null){
                posts_container.parentNode.insertAdjacentHTML("beforeend",Addanimation)
            }
            for (let i = 0; i < Object.keys(data).length; i++) {
                ShownPosts.push(data[`post${i+1}`].slug)
            }
            showPost(data)
        }
    })
}

// views formatter

const formatView = (num)=>{
    let formattedNum;

    if (num < 1000) {
        formattedNum = num.toString();
    } else if (num < 1000000) {
        formattedNum = (num / 1000).toFixed(1) + "K";
    } else {
        formattedNum = (num / 1000000).toFixed(1) + "M";
    }

    return formattedNum
}


// format the date which is come from the server
const formatDate = (dateString) => {
  const date = new Date(dateString);
  const monthNames = [
    "Jan", "Feb", "Mar",
    "Apr", "May", "Jun", "Jul",
    "Aug", "Sep", "Oct",
    "Nov", "Dec"
  ];

  const day = date.getDate();
  let daySuffix;
  switch (day) {
    case 1:
    case 21:
    case 31:
      daySuffix = 'ST';
      break;
    case 2:
    case 22:
      daySuffix = 'ND';
      break;
    case 3:
    case 23:
      daySuffix = 'RD';
      break;
    default:
      daySuffix = 'TH';
      break;
  }

  const monthIndex = date.getMonth();
  const monthName = monthNames[monthIndex];

  const year = date.getFullYear().toString().substr(-2);

  return `${monthName} ${day}${daySuffix} '${year}`;
}

// show the posts on the page
const showPost = (postsData) => {
    for (post in postsData) {
        let date = formatDate(postsData[post].date)
        
        post_html = `
        
	    <div class="col-lg-4">
	        <div class="post-entry-1 lg">
	            <a href="/post/${postsData[post].slug}"><img src="${postsData[post].thumbnail}" alt="" class="img-fluid w-100">
	            <div class="post-meta">
	                <span class="date">${postsData[post].category}</span> 
	                <span class="mx-1">&bullet;</span> 
	                <span>${date}</span>
	                <span id="post-date">(${formatView(postsData[post].views)} views)</span>
	            </div>
	            <h2>${postsData[post].title}</h2>
	            <p class="mb-4 d-block">${postsData[post].desc}</p></a>
	            <div class="d-flex align-items-center author">
	                <div class="photo"><img src="${postsData[post].user_pic}" alt="" class="w-2 h-2"></div>
	                <div class="name">
	                    <h3 class="m-0 p-0">${postsData[post].user}</h3>
	                </div>
	            </div>
	        </div>
	    </div>`
	    
	    posts_container.insertAdjacentHTML("beforeend",post_html)
	    
    
	    
    }
}


