use std::{
    io::Write,
    process::{Command, Stdio},
};

use crate::{blog_model::ArticleMeta, custom_page_model::CustomPageMeta};

pub fn read_front_matter(contents: &str) -> Vec<&str> {
    let mut is_front_matter: bool = false;
    let mut counter_meet_delimiter: u8 = 0;
    let mut front_matter = Vec::new();

    for (line_number, line) in contents.lines().enumerate() {
        if (line_number == 0) & (line != "---") {
            // break the loop, if first line is not "---"
            break;
        } else if (line_number == 0) & (line == "---") {
            // if first line is "---", increase counter_meet_delimiter and set is_front_matter = true
            counter_meet_delimiter += 1;
            is_front_matter = true;
            continue;
        }

        if is_front_matter & (line == "---") {
            // if encounter the second delimiter "---", then break the loop and increase counter_meet_delimiter
            counter_meet_delimiter += 1;
            break;
        }

        if is_front_matter & ((line != "---") | (line != "")) {
            front_matter.push(line);
        }
    }

    if counter_meet_delimiter == 1 {
        // if there are not the closed delimiter
        front_matter = Vec::new();
    }

    front_matter
}

pub fn parse_article_front_matter(contents: &str) -> serde_yaml::Result<ArticleMeta> {
    let front_matter = read_front_matter(contents);
    serde_yaml::from_str::<ArticleMeta>(&front_matter.join("\n"))
}

pub fn parse_custom_front_matter(contents: &str) -> serde_yaml::Result<CustomPageMeta> {
    let front_matter = read_front_matter(contents);
    serde_yaml::from_str::<CustomPageMeta>(&front_matter.join("\n"))
}

pub fn parse_md_to_html(md: &str) -> Option<String> {
    let mut child = Command::new("pandoc")
        .stdout(Stdio::piped())
        .stdin(Stdio::piped())
        .args(&["-f", "gfm", "-t", "html"])
        .spawn()
        .ok()?;

    let stdin = child.stdin.as_mut().unwrap();

    stdin.write(md.as_bytes()).ok()?;

    let stdout = child.wait_with_output().ok()?.stdout;
    Some(String::from_utf8(stdout).ok()?)
}
