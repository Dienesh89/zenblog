let usedPosts = []
let postsData = {}
let footerAdded = false
// get the posts from the server and store the posts in postsData
const getPost = async () => {
    const formData = new FormData();
    formData.append('used_posts', JSON.stringify(usedPosts));

    fetch("/get-post", {
            method: "POST",
            body: formData
        }).then(response => response.json())
        .then(data => {
            postsData = data
            if (data.slug == "false") {
                if (footerAdded == false) {
                    // removing yhe loading animation
                    let animation = document.getElementById("posts-animation")
                    animation.remove()
                    
                    postNotFound()
                    
                    // footer is dedined in html file to load django variables
                    document.body.insertAdjacentHTML("beforeend",footer)
                    footerAdded = true
                }
            } else {
                for (let i = 0; i < Object.keys(data).length; i++) {
                    usedPosts.push(data[`post${i+1}`].slug)
                }
                showPost(data) 
            
            }
        }) 
    
        return true
} 

const postNotFound = ()=>{
    not_found_html = `
	<div class="container mt-5">
		<div class="jumbotron text-center">
			<h1 class="display-4">No Posts Found</h1>
			<p class="lead">Please come beck later.</p>
			<hr class="my-4">
    	</div>
	</div>
    `
    
    let post_cont = document.getElementById("show-posts")
    post_cont.insertAdjacentHTML("beforebegin",not_found_html)
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
    let animation = document.getElementById("posts-animation")
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
	    
	    animation.insertAdjacentHTML("beforebegin", post_html);
    }
}

var functionHasRun = false;

const infScroll = async () => {
    let getPostRunned = await getPost()

    if (getPostRunned) {
        window.addEventListener("scroll", (e) => {
            e.preventDefault();


            let scrollPosition = window.pageYOffset;
            let pageHeight = document.documentElement.scrollHeight;
            let viewportHeight = window.innerHeight;
            let threshold = pageHeight - viewportHeight // - beforeHeight;

            if (scrollPosition >= threshold && !functionHasRun) {
                getPost();
                // beforeHeight = beforeHeight + 100
                functionHasRun = true;
            }

            if (scrollPosition < threshold) {
                functionHasRun = false;
            }
            
        })
    }
}

infScroll()



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
