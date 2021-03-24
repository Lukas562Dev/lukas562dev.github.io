#!/usr/bin/python
import inspect
import shutil
import json
import os
import sys

import urllib.parse
from bloghelpers import generate_opengraph_meta, generate_html_meta, generate_twitter_meta, generate_head_html, twitter_logo, generate_html
from blogconfig import logo, website_domain, blog_location
from mdtohtml import md_to_html

"""
try:
    import markdown as md
except ImportError:
    print('The "markdown" pip package is needed')
    sys.exit(1)
"""

script_path = inspect.getfile(inspect.currentframe())             # src/buildblog.py
src_directory = os.path.dirname(os.path.abspath(script_path))     # src
blogs_src_directory = os.path.join(src_directory, 'blogs')        # src/blogs
blogs_directory = os.path.join(src_directory, os.pardir, 'blog')  # src/../blog || blog
blog_list_file_path = os.path.join(blogs_directory, 'index.html') # src/../blog/index.html || blog/index.html

shutil.rmtree(os.path.abspath(blogs_directory))
os.makedirs(os.path.abspath(blogs_directory))
dirs = os.listdir(blogs_src_directory)

def generate_blog_html(blog):
    blog_meta = blog.meta_data
    blog_url = f'{blog_location}/{blog.blog_id}'
    blog_author_data = blog_meta['authorData']
    head = f'''
{generate_head_html(blog.title, ['blog.css', 'markdown.css'])}

{generate_html_meta(blog_url, blog.author, blog_meta['tags'])}

{generate_opengraph_meta(blog.title, blog_url)}

{generate_twitter_meta(blog.title, blog_url)}
'''.strip()

    # blog_html = md.markdown(blog.markdown_data, output_format='html5')
    blog_html = md_to_html(blog.markdown_data)

    return generate_html(head, f'''
<article class="blog container">
    <div class="blogContent">
        <h2>{blog.title}</h2>
        <div class="markdown-body">
            {blog_html}
        </div>
    </div>
    <div class="below-post">
        <div class="tags">
            {''.join(map(lambda x: f'<div>{x}</div>', blog_meta['tags']))}
        </div>
        <div class="share">
            <a href="https://twitter.com/intent/tweet?text=Just%20read%20{blog_meta['author']}%27s%20blog%20article&url={urllib.parse.quote(blog_url)}" class="share-twitter">
                {twitter_logo('#1DA1F2')}
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
                    {twitter_logo('#ffffff')}
                    <span>Follow <strong>@{blog_author_data['twitter']}</strong></span>
                </a>
            </div>
        </div>
    </footer>
</article>
    '''.strip())

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

for blog in blogs:
    blog_path = os.path.join(blogs_directory, blog.blog_id) # blog/XXXX-XX-XX
    blog_index_path = os.path.join(blog_path, 'index.html') # blog/XXXX-XX-XX/index.html
    os.makedirs(blog_path)

    with open(blog_index_path, 'x') as index_file: 
        index_file.write(generate_blog_html(blog))


def generate_list_item_html(post):
    blog_meta = post.meta_data
    blog_url = f'{blog_location}/{post.blog_id}'
    blog_author_data = blog_meta['authorData']
    return f'''
<article class="blog-list-item">
    <a href="{blog_url}" style="text-decoration: none; color: unset;">
        <h2 style="margin: 0px;">{post.title}</h2>
    </a>
    by <address style="display: inline;"><a href="{blog_author_data['github']}" style="text-decoration: none; color: unset;"><h3 style="margin: 0px; display: inline;">{post.author}</h3></a></address>
    
    <div class="below-post">
        <div class="tags">
            {''.join(map(lambda x: f'<div class="tag">{x}</div>', blog_meta['tags']))}
        </div>
        <div class="share">
            <a href="https://twitter.com/intent/tweet?text=Just%20read%20{post.author}%27s%20blog%20article&url={urllib.parse.quote(blog_url)}" class="share-twitter">
                {twitter_logo('#1DA1F2')}
            </a>
        </div>
    </div>
</article>
    '''.strip()

def generate_list_html(posts):
    list_items_html = ''
    for post in posts:
        list_items_html = list_items_html + generate_list_item_html(post) + '\n'
    
    head = f'''
{generate_head_html('Blog List', ['blogList.css'])}

{generate_html_meta(blog_location, 'ThatOneLukas', ['lukas', 'thatonelukas', 'programmer', 'programming', 'projects'])}

{generate_opengraph_meta('Blog List', blog_location)}

{generate_twitter_meta('Blog List', blog_location)}
'''.strip()

    return generate_html(head, f'''
<div class="blog-list container">
    {list_items_html}
</div>
    '''.strip())

with open(blog_list_file_path, 'x') as blog_list_file: 
    blog_list_file.write(generate_list_html(blogs))