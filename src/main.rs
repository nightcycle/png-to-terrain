use std::fs;
use std::fs::File;
use std::io::Read;

fn main() {
	let mut file = match File::open("./test/Test.txt") {
		Ok(file) => file,
		Err(e) => {
		    println!("Error opening file: {}", e);
		    return;
		}
	 };

	 let mut contents = String::new();
	 match file.read_to_string(&mut contents) {
		Ok(_) => println!("File contents: {}", contents),
		Err(e) => println!("Error reading file: {}", e),
	 }
}
 
fn xml_encode_config() -> rbx_xml::EncodeOptions {
	rbx_xml::EncodeOptions::new().property_behavior(rbx_xml::EncodePropertyBehavior::WriteUnknown)
}
