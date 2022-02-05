// TODO! Make a CLI thing for these
const DEFAULT_TAGS: [&str; 5] = [
    "blog",
    "lukas",
    "lukasdoesdev",
    "thatonelukas",
    "programmer",
];
const LOGO_URL: &str = "https://thatonelukas.tk/pictureLogo.png";

pub fn generate_html_raw(head: String, content: String) -> String {
    return format!(
        r#"
<!DOCTYPE html>
<!-- index.html -->
<html lang="en">
    <head>
        {head}
    </head>
    <body>
        <div id="content">
            <section class="top-section">
                <header id="header">
                    <a href="/en"><h1>Lukas's Blog</h1></a>
                    <nav id="nav">
                        <a href="/en">Home</a>
                        <a href="/en/about">About</a>
                        <a href="/en/blog">Articles</a>
                    </nav>
                </header>
                <main id="main">
                    {content}
                </main>
            </section>
            <footer id="footer">
                <div class="footer-left">Copyright © 2021 ThatOneLukas</div>
                <div class="footer-right"><a href="/">Home</a></div>
            </footer>
        </div>
    </body>
</html>"#,
        head = head,
        content = content
    )
    .trim()
    .to_string();
}

pub fn twitter_logo(color: &str) -> String {
    return format!(r#"
<svg version="1.1" height="25px" viewBox="0 0 231.104 231.104">
    <g><path style="fill: {color};" d="M4.453,173.33c9.763-1.192,19.663,0.092,29.426-1.512c4.904-0.779,9.396-2.429,13.842-4.171
    c-11-7.058-20.901-15.125-30.113-24.796c-3.3-3.438-0.917-9.213,3.896-9.35c3.942,0.183,7.792-0.137,11.55-0.917
    c-9.58-12.146-17.005-25.209-22.78-39.876c-1.558-3.942,3.025-7.929,6.738-6.738c2.154,0.871,4.354,1.467,6.6,1.925
    c-6.829-16.409-8.25-32.955-4.446-51.106c0.871-4.171,6.371-5.179,9.167-2.429c21.909,21.541,49.593,31.9,79.202,36.85
    c-2.613-20.259,11.78-41.801,30.663-48.86c15.676-5.821,36.714-1.833,47.256,11.367c7.059-4.446,16.821-5.913,24.659-7.288
    c4.125-0.688,8.113,3.346,5.684,7.425c-2.842,4.767-5.546,9.854-8.525,14.713c6.05-1.788,12.284-2.888,18.517-3.667
    c4.492-0.596,7.196,6.325,3.759,9.075c-7.288,5.821-14.53,12.467-22.276,17.784c-0.229,51.472-15.263,94.649-61.235,123.937
    c-38.319,24.477-109.546,20.352-142.867-12.97H3.124c-1.467-0.367-2.246-1.467-2.521-2.658c-1.283-1.925-0.367-4.308,1.329-5.225
    C2.574,174.063,3.399,173.467,4.453,173.33z"/></g>
</svg>
    "#, color=color).trim().to_string();
}

pub fn generate_html(
    title: String,
    stylesheets: Vec<String>,
    url: String,
    author: String,
    tags: Vec<String>,
    content: String,
    description: String,
) -> String {
    generate_html_raw(
        generate_head_html(title, stylesheets, url, author, tags, description),
        content,
    )
}

pub fn generate_head_html(
    title: String,
    stylesheets: Vec<String>,
    url: String,
    author: String,
    custom_tags: Vec<String>,
    description: String,
) -> String {
    let stylesheets_html = stylesheets
        .iter()
        .map(|x| format!(r#"<link rel="stylesheet" href="/static/css/{}" />"#, x))
        .collect::<Vec<String>>()
        .join("\n");
    let tags: Vec<String> = DEFAULT_TAGS.iter().map(|x| x.to_string()).collect();
    let tags: Vec<String> = tags
        .iter()
        .cloned()
        .chain(custom_tags.iter().cloned())
        .collect();
    let (twitter_description, og_description, html_description) = if !description.is_empty() {
        (
            format!(
                r#"<meta property="twitter:description" content="{}">"#,
                description
            ),
            format!(
                r#"<meta property="og:description" content="{}">"#,
                description
            ),
            format!(r#"<meta property="description" content="{}">"#, description),
        )
    } else {
        ("".to_string(), "".to_string(), "".to_string())
    };

    return format!(
        r#"
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

<!-- HTML Meta Tags -->
{html_description}
<meta name="keywords" content="{tags}"/>
<meta name="copyright" content="ThatOneLukas">
<meta name="author" content="{author}">
<meta name="designer" content="ThatOneLukas">
<meta name="owner" content="ThatOneLukas">
<meta name="url" content="{url}">
<meta name="identifier-URL" content="{url}">

<!-- OpenGraph Meta Tags -->
<meta property="og:type" content="website">
<meta property="og:title" content="{title} | Lukas's Blog!">
<meta property="og:site_name" content="Lukas's Blog!">
{og_description}
<meta property="og:url" content="{url}">
<meta property="og:image" content="{logo}">
<meta property="og:image:secure_url" content="{logo}" />
<meta property="og:image:type" content="image/png" />
<meta property="og:image:width" content="400" />
<meta property="og:image:height" content="400" />
<meta property="og:image:alt" content="Lukas's Logo" />

<!-- Twitter Meta Tags -->
<meta name="twitter:card" content="summary">
<meta property="twitter:domain" content="{website_domain}">
<meta property="twitter:url" content="{url}">
<meta name="twitter:title" content="{title} | Lukas's Blog!">
{twitter_description}
<meta name="twitter:image" content="{logo}">"#,
        website_domain = "thatonelukas.tk",
        url = url,
        title = title,
        author = author,
        twitter_description = twitter_description,
        og_description = og_description,
        html_description = html_description,
        logo = LOGO_URL,
        stylesheets_html = stylesheets_html,
        tags = tags.join("\n"),
    )
    .trim()
    .to_string();
}
