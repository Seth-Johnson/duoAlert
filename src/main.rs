use rand::Rng;
use std::path::Path;
use error_chain::error_chain;
use std::io::Read;

// global structure definitions
    //    Holds Login Details
    struct LoginData { 
        username: String,
        password: String
    }

fn get_config(cfgpath: &str) {
    let cfgpath = cfgpath;
}

fn login(logindata: LoginData) {

    // grab login deets as struct
    // maybe fix and turn this into json later

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
    let my_login: LoginData = LoginData {username: String::from("myUserName"), password: String::from("myPassword")};

    get_config(config_path);

    login(my_login);

    update_data();

    /*
    get streak data
    */

    if !Path::new("streak_data.json").exists() {
        
        // cry about nonexistent path
        println!("failed to retrieve streak data");

    } else {
        
        // check the data in the file
        check_data();
        
    }

    update_data_file();
    
}