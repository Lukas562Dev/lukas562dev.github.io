use clap::Parser;
#[derive(Parser, Debug)]
#[clap(author, version, about, long_about = None)]
pub struct Cli {
    /// The input directory to get the blog markdown from
    #[clap(long, default_value = "../en/blog")]
    pub blog_input: String,
    /// The output directory to put the blog markdown's html files to
    #[clap(long, default_value = "../../en/blog")]
    pub blog_output: String,
    /// The input directory to get the custom markdown from
    #[clap(long, default_value = "../en/custom")]
    pub custom_input: String,
    /// The output directory to put the custom markdown's html files to
    #[clap(long, default_value = "../../en/")]
    pub custom_output: String,
    // TODO: Thread pool :)
    /// Whether to run the program multi-threaded
    #[clap(long)]
    pub multi_threaded: bool,
    /// The base URL (no trailing slash)
    #[clap(long, default_value = "https://thatonelukas.tk/en")]
    pub base_url: String,
    /// The blog base URL (no trailing slash)
    #[clap(long, default_value = "https://thatonelukas.tk/en/blog")]
    pub blog_base_url: String,
    /// The base pathname (no trailing slash)
    #[clap(long, default_value = "/en")]
    pub base_pathname: String,
    /// The blog base pathname (no trailing slash)
    #[clap(long, default_value = "/en/blog")]
    pub blog_base_pathname: String,
}
