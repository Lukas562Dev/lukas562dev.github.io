from config import logo, website_domain, blog_location, default_tags

# Private functions

def generate_opengraph_meta(title, url, description):
    return f'''
<!-- OpenGraph Meta Tags -->
<meta property="og:type" content="website">
<meta property="og:title" content="{title} | Lukas's Blog!">
<meta property="og:site_name" content="Lukas's Blog!">
{f'<meta property="og:description" content="{description}">' if description else ''} 
<meta property="og:url" content="{url}">
<meta property="og:image" content="{logo}">
<meta property="og:image:secure_url" content="{logo}" />
<meta property="og:image:type" content="image/png" />
<meta property="og:image:width" content="400" />
<meta property="og:image:height" content="400" />
<meta property="og:image:alt" content="Lukas's Logo" />
    '''.strip()

def generate_html_meta(url, author, tags, description):
    return f'''
<!-- HTML Meta Tags -->
{f'<meta property="description" content="{description}">' if description else ''} 
<meta name="keywords" content="{', '.join(tags)}"/>
<meta name="copyright" content="ThatOneLukas">
<meta name="author" content="{author}">
<meta name="designer" content="ThatOneLukas">
<meta name="owner" content="ThatOneLukas">
<meta name="url" content="{url}">
<meta name="identifier-URL" content="{url}">
    '''.strip()

def generate_twitter_meta(title, url, description):
    return f'''
<!-- Twitter Meta Tags -->
<meta name="twitter:card" content="summary">
<meta property="twitter:domain" content="{website_domain}">
<meta property="twitter:url" content="{url}">
<meta name="twitter:title" content="{title} | Lukas's Blog!">
{f'<meta property="twitter:description" content="{description}">' if description else ''} 
<meta name="twitter:image" content="{logo}">
    '''.strip()

def generate_basic_head_html(title, stylesheets):
    stylesheets_html = '\n'.join(map(lambda x: '<link rel="stylesheet" href="/static/css/' + x + '" />', stylesheets))
    return f'''
<meta charset="UTF-8" />
<meta name="X-UA-Compatible" content="IE=edge" />
<meta name="HandheldFriendly" content="True" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>{title} | Lukas's Blog!</title>

<!-- Apple Meta Tags -->
<meta name="apple-mobile-web-app-capable" content="yes">
<meta content="yes" name="apple-touch-fullscreen" />
<meta name="apple-mobile-web-app-status-bar-style" content="black">

<link rel="stylesheet" href="/static/css/styles.css" />
<link rel="stylesheet" href="/static/markdown/markdown.css" />
<link rel="stylesheet" href="/static/markdown/md-dark.css" />
<link rel="stylesheet" href="/static/markdown/pandoc-highlighting.css" />
{stylesheets_html}
    '''.strip()

# Public functions

def generate_head_html(title, stylesheets, url, author, tags, description):
    tags = default_tags + tags
    return f'''
{generate_basic_head_html(title, stylesheets)}

{generate_html_meta(url, author, tags, description)}

{generate_opengraph_meta(title, url, description)}

{generate_twitter_meta(title, url, description)}
    '''.strip()