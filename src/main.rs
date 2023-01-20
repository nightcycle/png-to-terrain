use std::fs::File;
use std::io::Read;
use rbx_types::Variant;

fn main() {
	// Reads xml file
	let mut file = match File::open("./test/input.xml") {
		Ok(file) => file,
		Err(e) => {
			println!("Error opening file: {}", e);
			return;
		}
	};

	// Gets content of file
	let mut contents = String::new();
	match file.read_to_string(&mut contents) {
		Ok(_) => println!("File contents"),
		Err(e) => println!("Error reading file: {}", e),
	};
	
	// Imports xml str to rbx_xml
	let model = match rbx_xml::from_str_default(contents) {
		Ok(model) => model,
		Err(e) => {
			println!("Error building model: {}", e);
			return;
		}
	};

	// Gets Terrain instance
	let root = model.root();
	let terrain_ref = root.children()[0];
	let terrain = model.get_by_ref(terrain_ref).unwrap();
	// println!("Class name {}", terrain.class);

	// Get physics properties
	for name in terrain.properties.keys() {
	    let val_ref = match terrain.properties.get(name){
		Some(val_ref) => {
			if matches!(val_ref, Variant::BinaryString(_)) {
				println!("{} = BinaryString", name);
			};
	
		},
		None => {
		    println!("{} could not be opened", name);
		}
	};
}
	

}
