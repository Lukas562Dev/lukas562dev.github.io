use std::{
    fs::{self, DirEntry},
    path::Path,
};

use crate::{
    cli::Cli,
    generate_html::generate_html,
    parse_md::{parse_custom_front_matter, parse_md_to_html},
};

pub fn process_custom_page(input_entry: DirEntry, cli: &Cli) -> Option<()> {
    let md_path = input_entry.path();
    let content = fs::read_to_string(&md_path).ok()?;
    let page_meta = parse_custom_front_matter(&content).ok()?;
    let path = md_path.strip_prefix(&cli.custom_input).ok()?;
    let url = format!("{}/{}", &cli.blog_base_url, path.to_string_lossy());

    let html = parse_md_to_html(&content)?;
    let html = generate_html(
        page_meta.title,
        vec![],
        url,
        page_meta.author,
        page_meta.tags,
        html,
        page_meta.short_description,
    );

    if input_entry.metadata().ok()?.is_dir() {
        // TODO: Recursion!
        todo!();
    } else {
        if input_entry.file_name() == "index.md" {
            let new_file = Path::new(&cli.custom_output).join("index.html");
            fs::write(new_file, html).ok()?;
        } else {
            let new_dir = Path::new(&cli.custom_output).join(md_path.file_stem()?);
            fs::create_dir(&new_dir).ok();
            let new_file = new_dir.join("index.html");
            fs::write(new_file, html).ok()?;
        }
    }
    Some(())
}
