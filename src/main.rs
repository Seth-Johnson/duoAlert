extern crate serde_json;
extern crate serde;
extern crate serde_derive;
extern crate reqwest;

use rand::Rng;
use std::path::Path;
//use error_chain::error_chain;
use std::io::Read;
use serde::{Deserialize, Serialize};
use serde_json::Result;
//use reqwest::Client;

// global structure definitions

    // Holds the config data
    struct Config {
        duo_username: String,
        duo_password: String
    }

fn get_config(cfg_path: String) {
    //
}

fn login(logindata: Config) {

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

    let config_path: String = String::from("config.json");
    /*
    The config loader thing
    */
    let my_login = Config {
        duo_username: String::from("myUserName"),
        duo_password: String::from("myPassword")
    };

    get_config(String::from(config_path));

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