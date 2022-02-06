use std::{
    fs::{self, DirEntry},
    path::Path,
};

use crate::{article_model::ArticleMeta, generate_html::generate_html};
use crate::{parse_md::parse_article_front_matter, process_custom_page::process_custom_page};
use clap::StructOpt;
use cli::Cli;

pub mod article_model;
pub mod cli;
pub mod custom_page_model;
pub mod generate_html;
pub mod macros;
pub mod parse_md;
pub mod process_article;
pub mod process_custom_page;

fn create_article_list(cli: &Cli) -> Option<()> {
    fn get_meta_from_entry(entry: &DirEntry) -> Option<ArticleMeta> {
        let content = fs::read_to_string(&entry.path()).ok()?;
        parse_article_front_matter(&content).ok()
    }
    fn list_posts_in_year(
        year_dir: &DirEntry,
    ) -> Vec<(ArticleMeta, String, String, String, String)> {
        let mut output: Vec<(ArticleMeta, String, String, String, String)> = vec![];
        for month_dir in fs::read_dir(year_dir.path()).unwrap().flatten() {
            for day_dir in skip_fail!(fs::read_dir(month_dir.path())).flatten() {
                for article_md_file in skip_fail!(fs::read_dir(day_dir.path())).flatten() {
                    if let Some(meta) = get_meta_from_entry(&article_md_file) {
                        output.push((
                            meta,
                            format!("{}", year_dir.file_name().to_string_lossy()),
                            format!("{}", month_dir.file_name().to_string_lossy()),
                            format!("{}", day_dir.file_name().to_string_lossy()),
                            format!(
                                "{}",
                                article_md_file
                                    .path()
                                    .file_stem()
                                    .unwrap()
                                    .to_string_lossy()
                            ),
                        ));
                    }
                }
            }
        }
        output.sort_by(|a, b| {
            format!("{}-{}-{}-{}", a.1, a.2, a.3, a.4)
                .partial_cmp(&format!("{}-{}-{}-{}", b.1, b.2, b.3, b.4))
                .unwrap()
        });
        output.reverse();
        output
    }
    let post_list = fs::read_dir(&cli.blog_input)
    .ok()?
    .collect::<Vec<Result<DirEntry, std::io::Error>>>()
    .iter()
    .rev()
    .flatten()
    .map(|year_dir: &DirEntry| {
        Some(format!(
            r#"
            <li class="post-list-year">
            <h2>{}</h2>
            </li>
            {}
            "#,
            year_dir.path().file_stem()?.to_string_lossy(),
            list_posts_in_year(year_dir)
                .iter()
                .map(|(article, year, month, day, slug)| {
                    Some(format!(
                        r#"
                        <li class="post-list-item">
                            <time datetime="{date_str}T00:00:00.000Z" itemprop="datePublished">{date_str}</time>
                            <a href="{post_url}">{title}</a>
                        </li>
                        "#,
                        date_str = format!(
                            "{}-{}-{}",
                            year,
                            month,
                            day
                        ),
                        post_url= format!(
                            "{}/{}/{}/{}/{}",
                            cli.blog_base_pathname,
                            year,
                            month,
                            day,
                            slug
                        ),
                        title = article.title
                    ))
                })
                .flatten()
                .collect::<Vec<String>>()
                .join("")
        ))
    })
    .flatten()
    .collect::<Vec<String>>()
    .join("");
    let html = format!(
        r#"
<ul class="post-list">
{}
</ul>
        "#,
        post_list,
    );
    let html = generate_html(
        "Article List".to_string(),
        vec![],
        cli.blog_base_url.clone(),
        "ThatOneLukas".to_string(),
        vec!["articles".to_string(), "list".to_string()],
        html,
        "Article List".to_string(),
    );

    fs::write(
        Path::new(&cli.blog_output).join("index.html"),
        html.as_bytes(),
    )
    .ok()?;
    Some(())
}

fn main() -> std::io::Result<()> {
    let cli = Cli::parse();
    println!("Hello, world! {:?}", cli);

    fs::remove_dir_all(&cli.custom_output).ok();
    fs::create_dir(&cli.custom_output).ok();

    fs::remove_dir_all(&cli.blog_output).ok();
    fs::create_dir(&cli.blog_output).ok();

    create_article_list(&cli);

    for input_entry in fs::read_dir(&cli.custom_input)?.flatten() {
        process_custom_page(input_entry, &cli);
    }

    for year_dir in fs::read_dir(&cli.blog_input)?.flatten() {
        let new_year_dir = Path::new(&cli.blog_output).join(year_dir.file_name());
        fs::create_dir(&new_year_dir).ok();
        for month_dir in skip_fail!(fs::read_dir(year_dir.path())).flatten() {
            let new_month_dir = new_year_dir.join(month_dir.file_name());
            fs::create_dir(&new_month_dir).ok();
            for day_dir in skip_fail!(fs::read_dir(month_dir.path())).flatten() {
                let new_day_dir = new_month_dir.join(day_dir.file_name());
                fs::create_dir(&new_day_dir).ok();
                for article_md_file in skip_fail!(fs::read_dir(day_dir.path())).flatten() {
                    skip_fail_opt!(process_article::process_article(
                        article_md_file,
                        &new_day_dir,
                        format!(
                            "{}/{}/{}/{}",
                            cli.blog_base_url,
                            year_dir.file_name().to_string_lossy(),
                            month_dir.file_name().to_string_lossy(),
                            day_dir.file_name().to_string_lossy()
                        ),
                        format!(
                            "{}-{}-{}",
                            year_dir.file_name().to_string_lossy(),
                            month_dir.file_name().to_string_lossy(),
                            day_dir.file_name().to_string_lossy()
                        )
                    ));
                }
            }
        }
    }
    Ok(())
}
