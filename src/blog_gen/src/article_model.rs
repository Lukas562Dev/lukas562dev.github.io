use serde::{Deserialize, Serialize};

#[derive(Serialize, Deserialize, Debug)]
pub struct ArticleAuthorData {
    pub description: String,
    pub image: String,
    pub github: Option<String>,
    pub twitter: Option<String>,
}

#[derive(Serialize, Deserialize, Debug)]
#[serde(rename_all = "camelCase")]
pub struct ArticleMeta {
    pub title: String,
    pub short_description: String,
    pub tags: Vec<String>,
    pub created: String,
    pub author: String,
    pub author_data: ArticleAuthorData,
}
