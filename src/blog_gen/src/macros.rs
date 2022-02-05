#[macro_export]
macro_rules! skip_fail {
    ($res:expr) => {
        match $res {
            Ok(v) => v,
            Err(_e) => {
                continue;
            }
        }
    };
}

#[macro_export]
macro_rules! skip_fail_opt {
    ($res:expr) => {
        match $res {
            Some(v) => v,
            None => {
                continue;
            }
        }
    };
}
