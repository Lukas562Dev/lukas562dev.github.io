#!/usr/bin/python

import sys

if __name__ == "__main__":
    sys.exit(1)

import inspect, os, shutil, json, urllib.parse, datetime

from mdtohtml import md_to_html
from config import blog_location, base_url
from helper import generate_html, twitter_logo

script_path = inspect.getfile(inspect.currentframe())                    # ./src/blog.py
src_dir = os.path.dirname(os.path.abspath(script_path))                  # ./src
blogpost_src_dir = os.path.join(src_dir, 'blogs')                        # ./src/blogs
blogpost_dst_dir = os.path.join(src_dir, os.pardir, 'blog')              # ./blog
blogpost_list_file_path = os.path.join(blogpost_dst_dir, 'index.html')   # ./blog/index.html

class BlogPost():
    def __init__(self, meta_data, markdown_data, post_id, year, month, day):
        self.meta_data = meta_data
        self.markdown_data = markdown_data
        self.post_id = post_id
        self.title = meta_data['title']
        self.author = meta_data['author']
        self.date_str = f'{year}-{month}-{day}'
        self.date = datetime.datetime.strptime(f'{year}-{month}-{day}', '%Y-%m-%d')
    
    def __repr__(self):
        return 'BlogPost(' + self.title + ')'

# Private functions

def dir_to_blogpost(dir_path):
    blog_path = os.path.join(blogpost_src_dir, dir_path)
    meta_file_path = os.path.join(blog_path, 'meta.json')
    markdown_file_path = os.path.join(blog_path, 'markdown.md')


    with open(meta_file_path, 'r') as meta_file: 
        meta_data = json.load(meta_file)
    with open(markdown_file_path, 'r') as markdown_file: 
        markdown_data = markdown_file.read()
    
    [year, month, day] = blog_path.split(os.path.sep)[-4:-1]

    post_id = '/'.join(blog_path.split(os.path.sep)[-4:])
    
    return BlogPost(meta_data, markdown_data, post_id, year, month, day)

def generate_blogpost_html(post):
    post_meta = post.meta_data
    post_author_data = post_meta['authorData']

    post_url = f'{blog_location}/{post.post_id}'

    post_html = f'''
<article itemscope="" itemtype="http://schema.org/BlogPosting">
    <header>
        <h1 class="blogpost-title" itemprop="name headline">{post.title}</h1>
        <div class="blogpost-header-below">
            <div class="blogpost-meta">
                <span class="author" itemprop="author" itemscope="" itemtype="http://schema.org/Person">
                    <span itemprop="name">{post.author}</span>
                </span>
                <span class="blogpost-date">
                    <time datetime="{post.date_str}T00:00:00.000Z" itemprop="datePublished">{post.date_str}</time>
                </span>
                <span class="blogpost-tags">
                    | Tags: {', '.join(post_meta['tags'])}
                </span>
            </div>
            <span class="blogpost-share">
                <a rel="noopener noreferrer nofollow" target="_blank" href="https://twitter.com/share?url={urllib.parse.quote(post_url)}">{twitter_logo('#1DA1F2')}</a>
            </span>
        </div>
    </header>
    <div class="markdown-body">
        {md_to_html(post.markdown_data)}
    </div>
</article>
    '''.strip()
    return generate_html(
            post.title, # title
            [], # stylesheets
            post_url, # url
            post.author, # author
            post.meta_data['tags'], # tags
            post_html, # content
            post.meta_data['shortDescription'] # description
        )

def blogpost_list_item(post):
    post_url = f'{blog_location}/{post.post_id}'

    return f'''
<li class="post-list-item">
    <time datetime="{post.date_str}T00:00:00.000Z" itemprop="datePublished">{post.date_str}</time>
    <a href="{post_url}">{post.title}</a>
</li>
    '''.strip()

def blogpost_list_year(year):
    posts = []
    post_year_dir = os.path.join(blogpost_src_dir, year)
    for post_month in os.listdir(post_year_dir):
        post_month_dir = os.path.join(post_year_dir, post_month)
        for post_day in os.listdir(post_month_dir):
            post_day_dir = os.path.join(post_month_dir, post_day)

            for post_id in os.listdir(post_day_dir):
                post_dir = os.path.join(post_day_dir, post_id)
                posts.append(dir_to_blogpost(post_dir))
    posts = sorted(posts, key=lambda post: post.date)
    return f'''
<li class="post-list-year">
    <h2>{year}</h2>
</li>
{''.join(map(blogpost_list_item, posts))}
    '''.strip()

# Public functions

def setup_blog_dir():
    if os.path.isdir(os.path.abspath(blogpost_dst_dir)):
        shutil.rmtree(os.path.abspath(blogpost_dst_dir))
    os.makedirs(os.path.abspath(blogpost_dst_dir))

def build_blogposts():
    for post_year in os.listdir(blogpost_src_dir):
        post_year_dir = os.path.join(blogpost_src_dir, post_year)

        for post_month in os.listdir(post_year_dir):
            post_month_dir = os.path.join(post_year_dir, post_month)

            for post_day in os.listdir(post_month_dir):
                post_day_dir = os.path.join(post_month_dir, post_day)

                for post_id in os.listdir(post_day_dir):
                    post_dir = os.path.join(post_day_dir, post_id)
                    post_path = os.path.join(blogpost_dst_dir, post_year, post_month, post_day, post_id)
                    post_index_path = os.path.join(post_path, 'index.html')

                    os.makedirs(post_path)
                    post = dir_to_blogpost(post_dir)

                    with open(post_index_path, 'x') as index_file: 
                        index_file.write(generate_blogpost_html(post))
                    
                    print(f'Wrote {post_day}.{post_month}.{post_year} {post_index_path}')

def build_blogpost_list():
    years = os.listdir(blogpost_src_dir)
    years = sorted(years, key=lambda year: int(year))
    blogpost_list_raw_html = f'''
<ul class="post-list">
    {''.join(map(blogpost_list_year, years))}
</ul>
    '''.strip()
    blogpost_list_html = generate_html(
            'Blog Posts', # title
            [], # stylesheets
            base_url + '/blog', # url
            'ThatOneLukas', # author
            ['articles', 'blogs'], # tags
            blogpost_list_raw_html, # content
            None # description
        )
    with open(blogpost_list_file_path, 'x') as blogs_file:
        blogs_file.write(blogpost_list_html)
    print('Wrote article list')