#!/usr/bin/python
import inspect
import shutil
import json
import os
import sys

import urllib.parse

try:
    import markdown as md
except ImportError:
    print('The "markdown" pip package is needed')
    sys.exit(1)

script_path = inspect.getfile(inspect.currentframe())             # src/buildblog.py
src_directory = os.path.dirname(os.path.abspath(script_path))     # src
blogs_src_directory = os.path.join(src_directory, 'blogs')        # src/blogs
blogs_directory = os.path.join(src_directory, os.pardir, 'blog')  # src/../blog || blog
blog_list_file_path = os.path.join(blogs_directory, 'index.html') # src/../blog/index.html || blog/index.html

shutil.rmtree(os.path.abspath(blogs_directory))
os.makedirs(os.path.abspath(blogs_directory))
dirs = os.listdir(blogs_src_directory)

def generate_opengraph_meta(title, url):
    return f'''
<!-- OpenGraph Meta Tags -->
<meta property="og:title" content="{title} | ThatOneLukas's Blog!">
<meta property="og:type" content="website">
<meta property="og:url" content="{url}">
<meta property="og:image" content="https://www.thatonelukas.tk/pictureLogo.png">
<meta property="og:image:secure_url" content="https://www.thatonelukas.tk/pictureLogo.png" />
<meta property="og:image:type" content="image/png" />
<meta property="og:image:width" content="400" />
<meta property="og:image:height" content="400" />
<meta property="og:image:alt" content="ThatOneLukas's Logo" />
<meta property="og:site_name" content="ThatOneLukas's Website!">
<meta property="og:description" content="Homemade programmer">
    '''.strip()

def generate_html_meta(url, author, tags):
    return f'''
<!-- HTML Meta Tags -->
<meta name="description" content="Homemade programmer">
<meta name="keywords" content="{', '.join(tags)}"/>
<meta name="copyright" content="ThatOneLukas">
<meta name="author" content="{author}">
<meta name="designer" content="ThatOneLukas">
<meta name="owner" content="ThatOneLukas">
<meta name="url" content="{url}">
<meta name="identifier-URL" content="{url}">
    '''.strip()

def generate_twitter_meta(title, url):
    return f'''
<!-- Twitter Meta Tags -->
<meta name="twitter:card" content="summary_large_image">
<meta property="twitter:domain" content="thatonelukas.tk">
<meta property="twitter:url" content="{url}">
<meta name="twitter:title" content="{title} | ThatOneLukas's Blog!">
<meta name="twitter:description" content="Homemade programmer">
<meta name="twitter:image" content="https://www.thatonelukas.tk/pictureLogo.png">
    '''.strip()

def generate_blog_html(blog):
    blog_meta = blog.meta_data
    blog_url = f'https://www.thatonelukas.tk/blog/{blog.blog_id}'
    blog_author_data = blog_meta['authorData']
    head = f'''
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>{blog_meta['title']} | ThatOneLukas's Blog!</title>

{generate_html_meta(blog_url, blog.author, blog_meta['tags'])}

{generate_opengraph_meta(blog.title, blog_url)}

{generate_twitter_meta(blog.title, blog_url)}

<!-- Apple Meta Tags -->
<meta name="apple-mobile-web-app-capable" content="yes">
<meta content="yes" name="apple-touch-fullscreen" />
<meta name="apple-mobile-web-app-status-bar-style" content="black">

<link rel="stylesheet" href="/static/styles.css" />
<link rel="stylesheet" href="/static/blog.css" />
'''.strip()

    blog_html = md.markdown(blog.markdown_data)

    body = f'''
<header class="header">
    <div class="innerHeader container">
    <h1><a href="/" class="lukas-header">Lukas's Website!</a></h1>
    <a href="/blog">Blogs</a>
    </div>
</header>
<main class="main content" style="padding-top: 7rem; padding-bottom: 7rem;">
    <article class="blog container">
        <div class="blogContent">
            <h2>{blog.title}</h2>
            {blog_html}
        </div>
        <div class="below-post">
            <div class="tags">
                {''.join(map(lambda x: f'<div>{x}</div>',blog_meta['tags']))}
            </div>
            <div class="share">
                <a href="https://twitter.com/intent/tweet?text=Just%20read%20{blog_meta['author']}%27s%20blog%20article&url={urllib.parse.quote(blog_url)}" class="share-twitter">
                    <svg version="1.1" height="25px" style="position:relative;top:2px;" viewBox="0 0 231.104 231.104">
                    <g><path style="fill:#1DA1F2;" d="M4.453,173.33c9.763-1.192,19.663,0.092,29.426-1.512c4.904-0.779,9.396-2.429,13.842-4.171
                        c-11-7.058-20.901-15.125-30.113-24.796c-3.3-3.438-0.917-9.213,3.896-9.35c3.942,0.183,7.792-0.137,11.55-0.917
                        c-9.58-12.146-17.005-25.209-22.78-39.876c-1.558-3.942,3.025-7.929,6.738-6.738c2.154,0.871,4.354,1.467,6.6,1.925
                        c-6.829-16.409-8.25-32.955-4.446-51.106c0.871-4.171,6.371-5.179,9.167-2.429c21.909,21.541,49.593,31.9,79.202,36.85
                        c-2.613-20.259,11.78-41.801,30.663-48.86c15.676-5.821,36.714-1.833,47.256,11.367c7.059-4.446,16.821-5.913,24.659-7.288
                        c4.125-0.688,8.113,3.346,5.684,7.425c-2.842,4.767-5.546,9.854-8.525,14.713c6.05-1.788,12.284-2.888,18.517-3.667
                        c4.492-0.596,7.196,6.325,3.759,9.075c-7.288,5.821-14.53,12.467-22.276,17.784c-0.229,51.472-15.263,94.649-61.235,123.937
                        c-38.319,24.477-109.546,20.352-142.867-12.97H3.124c-1.467-0.367-2.246-1.467-2.521-2.658c-1.283-1.925-0.367-4.308,1.329-5.225
                        C2.574,174.063,3.399,173.467,4.453,173.33z"/></g>
                    </svg>
                </a>
            </div>
        </div>
        <hr/>
        <footer>
            <div class="author">
                <div>
                    <a href="{blog_author_data['github']}" style="text-decoration: none; color: unset;">
                        <img src="{blog_author_data['image']}" height="75px" />
                    </a>
                    <div>
                        <span>Written By</span>
                        <address><a href="{blog_author_data['github']}" style="text-decoration: none; color: unset;"><h2 style="margin: 0px">{blog.author}</h2></a></address>
                        <em>{blog_author_data['description']}</em>
                    </div>
                </div>
                <div class="twitter-follow-button-parent">
                    <a href="https://twitter.com/intent/follow?screen_name={blog_author_data['twitter']}" class="twitter-follow-button">
                    <svg version="1.1" height="16px" style="position:relative;top:2px;" viewBox="0 0 231.104 231.104">
                        <g><path style="fill:#ffffff;" d="M4.453,173.33c9.763-1.192,19.663,0.092,29.426-1.512c4.904-0.779,9.396-2.429,13.842-4.171
                        c-11-7.058-20.901-15.125-30.113-24.796c-3.3-3.438-0.917-9.213,3.896-9.35c3.942,0.183,7.792-0.137,11.55-0.917
                        c-9.58-12.146-17.005-25.209-22.78-39.876c-1.558-3.942,3.025-7.929,6.738-6.738c2.154,0.871,4.354,1.467,6.6,1.925
                        c-6.829-16.409-8.25-32.955-4.446-51.106c0.871-4.171,6.371-5.179,9.167-2.429c21.909,21.541,49.593,31.9,79.202,36.85
                        c-2.613-20.259,11.78-41.801,30.663-48.86c15.676-5.821,36.714-1.833,47.256,11.367c7.059-4.446,16.821-5.913,24.659-7.288
                        c4.125-0.688,8.113,3.346,5.684,7.425c-2.842,4.767-5.546,9.854-8.525,14.713c6.05-1.788,12.284-2.888,18.517-3.667
                        c4.492-0.596,7.196,6.325,3.759,9.075c-7.288,5.821-14.53,12.467-22.276,17.784c-0.229,51.472-15.263,94.649-61.235,123.937
                        c-38.319,24.477-109.546,20.352-142.867-12.97H3.124c-1.467-0.367-2.246-1.467-2.521-2.658c-1.283-1.925-0.367-4.308,1.329-5.225
                        C2.574,174.063,3.399,173.467,4.453,173.33z"/></g>
                    </svg>
                    Follow <strong>@{blog_author_data['twitter']}</strong></a>
                </div>
            </div>
        </footer>
    </article>
</main>
<footer id="footer">
    <div class="container">
        <h2>(c) Copyright ThatOneLukas 2021</h2>
    </div>
</footer>
    '''.strip()



    return f'''
<!DOCTYPE html>
<!-- index.html -->
<html lang="en">
    <head>
        {head}
    </head>
    <body>
        {body}
    </body>
</html>
    '''.strip()

class Blog():
    def __init__(self, meta_data, markdown_data, blog_id):
        self.meta_data = meta_data
        self.markdown_data = markdown_data
        self.blog_id = blog_id
        self.title = meta_data['title']
        self.author = meta_data['author']
    
    def __repr__(self):
        return 'Blog(' + self.title + ')'

def dir_to_blog(dir_path):
    blog_path = os.path.join(blogs_src_directory, dir_path)
    meta_file_path = os.path.join(blog_path, 'meta.json')
    markdown_file_path = os.path.join(blog_path, 'markdown.md')


    with open(meta_file_path, 'r') as meta_file: 
        meta_data = json.load(meta_file)
    with open(markdown_file_path, 'r') as markdown_file: 
        markdown_data = markdown_file.read()
    
    return Blog(meta_data, markdown_data, dir_path)

blogs = list(map(dir_to_blog, dirs))

print(blogs)
print()
print()
print(dirs)

for blog in blogs:
    blog_path = os.path.join(blogs_directory, blog.blog_id) # blog/XXXX-XX-XX
    blog_index_path = os.path.join(blog_path, 'index.html') # blog/XXXX-XX-XX/index.html
    os.makedirs(blog_path)

    with open(blog_index_path, 'x') as index_file: 
        index_file.write(generate_blog_html(blog))


def generate_list_item_html(post):
    blog_meta = blog.meta_data
    blog_url = f'https://www.thatonelukas.tk/blog/{blog.blog_id}'
    blog_author_data = blog_meta['authorData']
    return f'''
<article class="blog-list-item">
    <a href="{blog_url}" style="text-decoration: none; color: unset;">
        <h2 style="margin: 0px;">{post.title}</h2>
    </a>
    by <address style="display: inline;"><a href="{blog_author_data['github']}" style="text-decoration: none; color: unset;"><h3 style="margin: 0px; display: inline;">{blog.author}</h3></a></address>
    
    <div class="below-post">
        <div class="tags">
            {''.join(map(lambda x: f'<div class="tag">{x}</div>',blog_meta['tags']))}
        </div>
        <div class="share">
            <a href="https://twitter.com/intent/tweet?text=Just%20read%20{blog.author}%27s%20blog%20article&url={urllib.parse.quote(blog_url)}" class="share-twitter">
                <svg version="1.1" height="25px" style="position:relative;top:2px;" viewBox="0 0 231.104 231.104">
                    <g><path style="fill:#1DA1F2;" d="M4.453,173.33c9.763-1.192,19.663,0.092,29.426-1.512c4.904-0.779,9.396-2.429,13.842-4.171
                    c-11-7.058-20.901-15.125-30.113-24.796c-3.3-3.438-0.917-9.213,3.896-9.35c3.942,0.183,7.792-0.137,11.55-0.917
                    c-9.58-12.146-17.005-25.209-22.78-39.876c-1.558-3.942,3.025-7.929,6.738-6.738c2.154,0.871,4.354,1.467,6.6,1.925
                    c-6.829-16.409-8.25-32.955-4.446-51.106c0.871-4.171,6.371-5.179,9.167-2.429c21.909,21.541,49.593,31.9,79.202,36.85
                    c-2.613-20.259,11.78-41.801,30.663-48.86c15.676-5.821,36.714-1.833,47.256,11.367c7.059-4.446,16.821-5.913,24.659-7.288
                    c4.125-0.688,8.113,3.346,5.684,7.425c-2.842,4.767-5.546,9.854-8.525,14.713c6.05-1.788,12.284-2.888,18.517-3.667
                    c4.492-0.596,7.196,6.325,3.759,9.075c-7.288,5.821-14.53,12.467-22.276,17.784c-0.229,51.472-15.263,94.649-61.235,123.937
                    c-38.319,24.477-109.546,20.352-142.867-12.97H3.124c-1.467-0.367-2.246-1.467-2.521-2.658c-1.283-1.925-0.367-4.308,1.329-5.225
                    C2.574,174.063,3.399,173.467,4.453,173.33z"/></g>
                </svg>
            </a>
        </div>
    </div>
</article>
    '''.strip()

def generate_list_html(posts):
    list_items_html = ''
    for post in posts:
        list_items_html = list_items_html + generate_list_item_html(post) + '\n'
    
    url = f'https://www.thatonelukas.tk/blog'
    
    head = f'''
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>Blog List | ThatOneLukas's Blog!</title>

{generate_html_meta(url, 'ThatOneLukas', ['lukas', 'thatonelukas', 'programmer', 'programming', 'projects'])}

{generate_opengraph_meta('Blog List', url)}

{generate_twitter_meta('Blog List', url)}

<!-- Apple Meta Tags -->
<meta name="apple-mobile-web-app-capable" content="yes">
<meta content="yes" name="apple-touch-fullscreen" />
<meta name="apple-mobile-web-app-status-bar-style" content="black">

<link rel="stylesheet" href="/static/styles.css" />
<link rel="stylesheet" href="/static/blogList.css" />
'''.strip()

    body = f'''
<header class="header">
    <div class="innerHeader container">
    <h1><a href="/" class="lukas-header">Lukas's Website!</a></h1>
    <a href="/blog">Blogs</a>
    </div>
</header>
<main class="main content" style="padding-top: 7rem; padding-bottom: 7rem;">
    <div class="blog-list container">
        {list_items_html}
    </div>
</main>
<footer id="footer">
    <div class="container">
        <h2>(c) Copyright ThatOneLukas 2021</h2>
    </div>
</footer>
    '''.strip()



    return f'''
<!DOCTYPE html>
<!-- index.html -->
<html lang="en">
    <head>
        {head}
    </head>
    <body>
        {body}
    </body>
</html>
    '''.strip()

with open(blog_list_file_path, 'x') as blog_list_file: 
    blog_list_file.write(generate_list_html(blogs))