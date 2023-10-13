from django.shortcuts import render, HttpResponse,HttpResponseRedirect,redirect,get_object_or_404
# importing datetime
from datetime import datetime
# importing modeles
from home.models import Contact,customuser,ProfPic,postInfo,postImages
# django messaging framework
from django.contrib import messages
# importing variables from variables.py
from home import variables
# importing forms
from .forms import ProfPicForm,postInfoForm
# django default authentication system
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.views.decorators.csrf import csrf_exempt
# image api
import requests
from django.http import JsonResponse
# decorators
from django.contrib.auth.decorators import login_required
# some important modules
import random
import json
from django.utils import timezone
# for post view counter
from django.views.decorators.http import require_GET
# for extracting the text form the html
from bs4 import BeautifulSoup

# context for views
variablesViews = {
  "blogName":variables.blogName,
  # navbar options
  "navops1":variables.navops1,
  "navops2":variables.navops2,
  "navops3":variables.navops3,
  "navops4":variables.navops4,
  "navops5":variables.navops5,
  "navops6":variables.navops6,
  "navops7":variables.navops7,
  # footer
  "aboutFooter":variables.aboutFooter,
  # footer headings
  "footerH1":variables.footerH1,
  "footerH2":variables.footerH2,
  # categories
  "category1":variables.category1,
  "category2":variables.category2,
  "category3":variables.category3,
  "category4":variables.category4,
  "category5":variables.category5,
  "category6":variables.category6,
  "category7":variables.category7,
  "category8":variables.category8,
  # social media links
  "twitter":variables.twitter,
  "facebook":variables.facebook,
  "instagram":variables.instagram,
  "skype":variables.skype,
  "linkedin":variables.linkedin,
  # designed by
  "designedBy":variables.designedBy,
}

# home page
def index(request):
    # displaying the profile picture of the user if user is authenticated
    if request.user.is_authenticated:
        img = ProfPic.objects.all()
        variablesViews["img"] = img 

    today = timezone.now().date()
    top_4_models = postInfo.objects.filter(date=today).order_by('-post_views')[:4]
    top_4_models = list(top_4_models)
    
    i=1
    for topPost in range(len(top_4_models)):
        variablesViews[f"post{i}"] = {
            "slug":top_4_models[topPost].slug,
            "thumbnail":top_4_models[topPost].thumbnail.url,
            "title":top_4_models[topPost].title
        }
        i=i+1
    
    return render(request, 'index.html', variablesViews)

# signup page
def signup(request):
    # sending the ProfPicForm to the /signup page
    form = ProfPicForm()
    variablesViews["form"] = form
    return render(request, 'signup.html' ,variablesViews)

# login page
def login(request):
    return render(request, 'login.html', variablesViews)

# post content page
def single_post(request):
    return render(request, 'single-post.html', variablesViews)

# about page
def about(request):
    return render(request, 'about.html', variablesViews)

# handeling the submisson of contact form
def contact_submit(request):
    if request.method == "POST":
        # getting the info from the user
        name = request.POST.get("name")
        email = request.POST.get("email")
        subj = request.POST.get("subject")
        msg = request.POST.get("message")
        # saving the message to the database
        contact = Contact(name=name, email=email, subj=subj, msg=msg, date=datetime.today())
        contact.save()
        
        
        messages.success(request, "Your message has been sent.")
        
    return render(request, 'contact.html', variablesViews)

# contact page
def contact(request):
    if request.user.is_authenticated:
        return render(request, 'contact.html', variablesViews)
    else:
        messages.error(request,"Please login to contact us.")
        return redirect("/")

# category page
def category(request):
    return render(request, 'category.html', variablesViews)

# handeling the signup
def handleSignup(request):
    if request.method == "POST":
        # getting the info from the user
        name = request.POST["name"]
        email = request.POST["email"]
        password = request.POST["password"]
        cpassword = request.POST["c-password"]
        
        # checking for duplicate email
        if customuser.objects.filter(email=email).exists():
            messages.error(request,"This email already exists.")
            return redirect("/signup")
        else:
            UniqueEmail = True
        
        # checking for length of the password
        if len(password)>7:
            GoodPass = True
        else:
            messages.error(request,"Password length should be more then 8 characters.")
            return redirect("/signup")
        # checking for equal Passwords
        if password==cpassword:
            equalPass = True
        else:
            messages.error(request,"Passwords must be equal")
            return redirect("/signup")
        
        # if form is valid
        if UniqueEmail==True and GoodPass == True and equalPass == True:
            # creating the user
            user = customuser.objects.create_user(username=name,email=email,password=password)
            user.save()
            
            # getting the files
            form = ProfPicForm(request.POST,request.FILES)
            
            # saving the info to the database
            if form.is_valid():
                profile = form.save(commit=False)
                profile.user = user
                profile.save()
            
            messages.success(request,"You account has been successfully created login now!")
            return redirect("/login")
    else:
        return HttpResponse("404 - Not Found")

# handeling the login
def handleLogin(request):
    if request.method == "POST":
        # getting info from the user
        email = request.POST["email"]
        password = request.POST["password"]
        
        # authenticating the user
        user = authenticate(email=email, password=password)
        
        # if login info is correct
        if user is not None:
            # logging the user
            auth_login(request,user)
            messages.success(request,"You are successfully loggedin.")
            return redirect("/")
        else:
            messages.error(request,"Invalid email or password please try again.")
            return redirect("/login")
    else:
        return HttpResponse("404 - Not Found")

# for logout
def logout(request):
    if request.user.is_authenticated:
        auth_logout(request)
        messages.success(request,"You are successfully loggedout.")
        
    return redirect("/login")


# form uploading the post
@login_required(login_url="/login")
def upload_post(request):
    if request.method == "POST":
        # getting the info from the user
        # NOTE => this info is only the info of the post cover
        title = request.POST["title"]
        desc = request.POST["desc"]
        category = request.POST["category"]
        
        # getting the files from the form
        form = postInfoForm(request.POST,request.FILES)
        
        # saving the form to the database
        if form.is_valid():
            thumb = form.save(commit=False)
            thumb.title = title
            thumb.desc = desc
            thumb.category = category
            thumb.user = request.user
            thumb.save()
        
        return redirect(f"/edit-post/{thumb.slug}")
    else:
        form = postInfoForm()
        variablesViews["form"] = form
        
        if request.user.is_authenticated:
            img = ProfPic.objects.all()
            variablesViews["img"] = img 
        
        return render(request,"upload_post.html",variablesViews)

@csrf_exempt
def edit_post(request, slug):
    # checking the slug is come from the upload-post page or Not
    # if valid slug is come from the upload-post
    try:
        slugInModel = postInfo.objects.get(slug=slug)
        slugModel = postInfo.objects.get(slug=slug)
        if(request.user == slugModel.user):
            if request.method == 'POST':
              htmlCode = request.POST["code"]
              slugModel.htmlCode = htmlCode
              slugModel.save()
              return JsonResponse({'status':'ok'})
            else:
                return render(request,"edit_post.html",variablesViews)
        else:
            return HttpResponse("You are not authenticated to access this page")
        
    except:
        return HttpResponse("404 - Not Found")
        
    
# this is the api which takes image and gives url of the image from javascript
# NOTE => Created by chatGPT
@csrf_exempt
def post_images(request):
    if request.method == 'POST':
        image_file = request.FILES.get('image')
        caption = request.POST.get('caption')
        if image_file:
            # Save the image to the database
            image_model = postImages(image=image_file, caption=caption)
            image_model.save()
            
            return JsonResponse({'success': True,"image_url":image_model.image.url,"caption":image_model.caption})
            
        else:
            return JsonResponse({'success': False, 'error': 'No image file'})
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request method'})

# get post api
@csrf_exempt
def get_post(request):
    if request.method == "POST":
        # getting the array which contains the slug of the objects which is shown on the page
        used_posts_slugs_json = request.POST['used_posts']
        used_posts_slugs = json.loads(used_posts_slugs_json)
        
        # list of shown posts
        used_posts = []
        
        posts = []
        
        # allPosts = postInfo.objects.filter(category=request.POST['postCategory'])
        
        try:
            allPosts = postInfo.objects.filter(category=request.POST["postCategory"])
        except:
            allPosts = postInfo.objects.all()
        
        
        
        
        # adding and shuffling the posts in posts lisf
        for i in allPosts:
            posts.append(i)
            random.shuffle(posts)
            
        # removing the shown posts from the posts list
        
        try:
            if len(used_posts_slugs)>0:
                for i in used_posts_slugs:
                    usedObj = postInfo.objects.filter(slug = i)
                    posts.remove(usedObj.first())
        except:
            pass
        
        
        postsDict = {}
        
        # if all posts is shown on the page
        if len(posts)<1:
            postsDict = {
                "status":"ok",
                "slug":"false",
                "posts_ended":"true"
            }
        # if remaining posts is less than 6
        elif len(posts)<6:
            for i in range(len(posts)):
                userProfPic = ProfPic.objects.get(user = posts[i].user).pic.url
                postsDict[f"post{i+1}"] = {
                    "title":posts[i].title,
                    "desc":posts[i].desc,
                    "thumbnail":posts[i].thumbnail.url,
                    "user":posts[i].user.username,
                    "date":posts[i].date,
                    "user_pic":userProfPic,
                    "content":posts[i].htmlCode,
                    "slug":posts[i].slug,
                    "category":posts[i].category,
                    "views":posts[i].post_views
                }
        else:
            for i in range(6):
                userProfPic = ProfPic.objects.get(user = posts[i].user).pic.url
                postsDict[f"post{i+1}"] = {
                    "title":posts[i].title,
                    "desc":posts[i].desc,
                    "thumbnail":posts[i].thumbnail.url,
                    "user":posts[i].user.username,
                    "user_pic":userProfPic,
                    "date":posts[i].date,
                    "content":posts[i].htmlCode,
                    "slug":posts[i].slug,
                    "category":posts[i].category,
                    "views":posts[i].post_views
                }
            
        return JsonResponse(postsDict)
    else:
        return HttpResponse("404 - Not Found")


def show_post(request,slug):
    try:
        post_Model = postInfo.objects.get(slug=slug)
        html = post_Model.htmlCode
        title = post_Model.title
        category = post_Model.category
        date = post_Model.date
        
        if request.session.get('has_viewed_%s' % slug, False):
            # user has already viewed this post
            pass
        else:
            # user is viewing this post for the first time
            post_Model.post_views = post_Model.post_views+1
            post_Model.save()
            request.session['has_viewed_%s' % slug] = True
    
        variablesViews["content"] = html
        variablesViews["title"] = title
        variablesViews["views"] = post_Model.post_views
        variablesViews["post_category"] = category
        variablesViews["date"] = date
        return render(request,"post.html",variablesViews)
    except:
        return HttpResponse("404 - Not Found")

@csrf_exempt
def search(request):
    searchedPosts = postInfo.objects.none()
    if request.method == "POST":
        query = request.POST["query"]
        if len(query)<100:
            # getting the array which contains the slug of the objects which is shown on the page
            shown_posts_slugs_json = request.POST['shown_posts']
            
            shown_posts_slugs = json.loads(shown_posts_slugs_json)

            shown_posts = postInfo.objects.filter(slug=shown_posts_slugs)
            
            
            # Remove HTML markup from the field htmlCode in the model postInfo
            for post in shown_posts:
                htmlCode = post.htmlCode
                soup = BeautifulSoup(htmlCode, 'html.parser')
                post.htmlCode = soup.get_text()
            
            # searching for query in title,desc,content
            searchPostsTitle = postInfo.objects.filter(title__icontains=query)
            searchPostsDesc = postInfo.objects.filter(desc__icontains=query)
            searchPostsContent = postInfo.objects.filter(htmlCode__icontains=query)
            searchedPosts = searchPostsTitle.union(searchPostsDesc,searchPostsContent)
            searchedPosts = list(searchedPosts)
            
            try:
                if len(shown_posts_slugs)>0:
                    for i in shown_posts_slugs:
                        usedPostsObj = postInfo.objects.filter(slug = i)
                        searchedPosts.remove(usedPostsObj.first())
            except:
                pass
        
        

        
                   
        response = {}
                    
        if len(searchedPosts)<1:
            return JsonResponse(
                {
                    "status":"ok",
                    "posts_not_found":"true"
                    
                }
            )
        elif len(searchedPosts)<6:
            i=1
            for posts in searchedPosts:
                userProfPic = ProfPic.objects.get(user = posts.user).pic.url
                response[f"post{i}"] = {
                    "title":posts.title,
                    "desc":posts.desc,
                    "thumbnail":posts.thumbnail.url,
                    "user":posts.user.username,
                    "date":posts.date,
                    "user_pic":userProfPic,
                    "content":posts.htmlCode,
                    "slug":posts.slug,
                    "category":posts.category,
                    "views":posts.post_views,
                }
                i=i+1
            return JsonResponse(response)
        elif len(searchedPosts)>5:
            for i in range(6):
                userProfPic = ProfPic.objects.get(user = searchedPosts[i].user).pic.url
                response[f"post{i+1}"] = {
                    "title":searchedPosts[i].title,
                    "desc":searchedPosts[i].desc,
                    "thumbnail":searchedPosts[i].thumbnail.url,
                    "user":searchedPosts[i].user.username,
                    "date":searchedPosts[i].date,
                    "user_pic":"tatti",
                    "content":searchedPosts[i].htmlCode,
                    "slug":searchedPosts[i].slug,
                    "category":searchedPosts[i].category,
                    "views":searchedPosts[i].post_views,
                }
            return JsonResponse(response)
        
    else:
        return render(request,"search.html",variablesViews)


def category(request,category):
    return render(request,"category.html",variablesViews)


def handle_404(request, exception):
    return render(request, '404.html',variablesViews, status=404)
