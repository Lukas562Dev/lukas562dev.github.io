use std::{
    fs::{self, DirEntry},
    path::PathBuf,
};

use crate::{
    generate_html::{generate_html, twitter_logo},
    parse_md::{parse_article_front_matter, parse_md_to_html},
};

pub fn process_article(
    article_md_file: DirEntry,
    new_day_dir: &PathBuf,
    base_url: String,
    date_str: String,
) -> Option<()> {
    let md_path = article_md_file.path();
    let content = fs::read_to_string(&md_path).ok()?;
    let article_meta = parse_article_front_matter(&content).ok()?;
    let slug = md_path.file_stem()?.to_str()?;
    let url = format!("{}/{}", base_url, slug);

    let html = parse_md_to_html(&content)?;
    let html = format!(
        r#"
    
<article itemscope="" itemtype="http://schema.org/BlogPosting">
<header>
    <h1 class="blogpost-title" itemprop="name headline">{title}</h1>
    <div class="blogpost-header-below">
        <div class="blogpost-meta">
            <span class="author" itemprop="author" itemscope="" itemtype="http://schema.org/Person">
                <span itemprop="name">{author}</span>
            </span>
            <span class="blogpost-date">
                <time datetime="{date_str}T00:00:00.000Z" itemprop="datePublished">{date_str}</time>
            </span>
            <span class="blogpost-tags">
                | Tags: {tags}
            </span>
        </div>
        <span class="blogpost-share">
            <a rel="noopener noreferrer nofollow" target="_blank" href="https://twitter.com/share?url={twitter_url}">{twitter_logo}</a>
        </span>
    </div>
</header>
<div class="markdown-body">
{content}
</div>
<script src="https://giscus.app/client.js"
    data-repo="LukasDoesDev/lukasdoesdev.github.io"
    data-repo-id="MDEwOlJlcG9zaXRvcnkxOTIxOTg0NzU="
    data-category="Announcements"
    data-category-id="DIC_kwDOC3S3S84CBB4s"
    data-mapping="pathname"
    data-reactions-enabled="1"
    data-emit-metadata="0"
    data-input-position="top"
    data-theme="dark"
    data-lang="en"
    crossorigin="anonymous"
    async>
</script>
"#,
        title = article_meta.title,
        author = article_meta.author,
        date_str = date_str,
        tags = article_meta.tags.join(", "),
        twitter_url = urlparse::quote(&url, b"").ok()?,
        twitter_logo = twitter_logo("#1DA1F2"),
        content = html,
    );
    let html = generate_html(
        article_meta.title,
        vec![],
        url,
        article_meta.author,
        article_meta.tags,
        html,
        article_meta.short_description,
    );

    fs::create_dir(new_day_dir.join(slug)).ok()?;

    fs::write(new_day_dir.join(slug).join("index.html"), html.as_bytes()).ok()?;

    Some(())
}
