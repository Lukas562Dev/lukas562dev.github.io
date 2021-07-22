#!/usr/bin/python
import inspect, os, shutil

from helper import generate_html
from config import base_url
from blog import build_blogposts, setup_blog_dir, build_blogpost_list
from mdtohtml import md_to_html

script_path = inspect.getfile(inspect.currentframe())   # ./src/build.py
src_dir = os.path.dirname(os.path.abspath(script_path)) # ./src
par_dir = os.path.join(src_dir, os.path.pardir)         # .
index_file_path = os.path.join(par_dir, 'index.html')   # ./index.html
about_dir_path = os.path.join(par_dir, 'about')         # ./about/
about_file_path = os.path.join(about_dir_path, 'index.html') # ./about/index.html
about_src_file_path = os.path.join(src_dir, 'about.md') # ./src/about.md

def main():
    setup_blog_dir()
    build_blogposts()
    build_blogpost_list()

    create_index_page()
    
    create_about_page()

def create_index_page():
    with open(index_file_path, 'w') as index_file: 
        index_file.write(generate_html(
            'About', # title
            [], # stylesheets
            base_url, # url
            'ThatOneLukas', # author
            ['blog', 'programming'], # tags
            'TODO', # content
            'Lukas\'s Blog' # description
        ))
    
    print('Written home page')

def create_about_page():
    if os.path.isdir(os.path.abspath(about_dir_path)):
        shutil.rmtree(os.path.abspath(about_dir_path))
    os.makedirs(os.path.abspath(about_dir_path))

    with open(about_file_path, 'w') as index_file:
        with open(about_src_file_path, 'r') as about_src_file:
            about_page_md = about_src_file.read()
        about_page_html = f'''
        <div class="markdown-body">
            {md_to_html(about_page_md)}
        </div>
        '''.strip()
        index_file.write(generate_html(
            'Home', # title
            [], # stylesheets
            base_url + '/about', # url
            'ThatOneLukas', # author
            ['about', 'programmer'], # tags
            about_page_html, # content
            'About Lukas' # description
        ))
    
    print('Written about page')

if __name__ == "__main__":
    main()