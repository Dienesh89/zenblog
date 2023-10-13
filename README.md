# ZenBlog
This Blogging web application project is purely made with Django as the backend and Bootstrap as the frontend.

## Screenshots
![Screenshot](https://Dienesh89.github.io/zenblog/screenshots/1.jpg)

![Screenshot](https://Dienesh89.github.io/zenblog/screenshots/2.jpg)

![Screenshot](https://Dienesh89.github.io/zenblog/screenshots/3.jpg)

![Screenshot](https://Dienesh89.github.io/zenblog/screenshots/4.jpg)

## Installation Instructions

If you want to work with this project or create a version of it make sure to follow the steps below!

0. Make sure to install ` Python` and ` pip ` 
1. Download project and install git
   
    ```bash
apt install git -y
git clone https://github.com/Dienesh89/zenblog
cd zenblog
    ```
2. Install requirements.
    ```bash
pip install -r requirements.txt
    ``` 

You have now successfully set up the project on your environment.

## How to run  the project?

Make sure you are in `env` and then do the following each at a time.

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

## Features

### Blog list View
List all blog posts with Title, Tag, Author Name, Date Posted, Image, and some body part with Read More button.


### category list
List all the categories related to the posts with total number of posts each categories have.

### Search
List all blog posts with the search query that you enter.

### Pagination
To limit with a certain number of posts in each page.

### Blog Detail View
To view the complete blog post just click the blog post

## Features

### Login/Register
Users can Login/Register to the Blog App.


### Create Blog Post
Users can create blog posts from the front end and add for approval, by the admin.

## Tech Stacks

* **Language:**  Python 3.11
* **Framework:** Django 

## Latest Fixes

1. Added Unique Slug Generator based on Title
2. Infinite scroll until posts ends

## How you can contribute to this project?

1. Fork this project to your GitHub account
2. Clone the repository to your local machine and follow the above Installation instructions.
3. Find an issue or feature and work on it.
4. Make a pull request.
