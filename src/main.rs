use rand::Rng;
use std::path::Path;

fn get_config(cfgpath: &str) {
    let cfgpath = cfgpath;
}

fn login() {

    // grab login deets as struct
    // maybe fix and turn this into json later
    struct LoginData {
        login: String,
        password: String
    }

    let jwt: &str = "";
}

fn update_data() {

}

fn check_data() {

}

fn update_data_file() {

}

fn main() {

    let config_path: &str = "";
    /*
    The config loader thing
    */

    get_config(config_path);

    login();

    update_data();

    /*
    get streak data
    */

    if !Path::new("streak_data.json").exists() {
        // check the data in the file
        println!("failed to retrieve streak data");
    } else {
        check_data();
    }

    update_data_file();
    
}