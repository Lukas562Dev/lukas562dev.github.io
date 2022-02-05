use serde::{Deserialize, Serialize};

#[derive(Serialize, Deserialize, Debug)]
#[serde(rename_all = "camelCase")]
pub struct CustomPageMeta {
    pub title: String,
    pub short_description: String,
    pub tags: Vec<String>,
    pub author: String,
}
