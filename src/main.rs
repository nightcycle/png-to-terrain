use std::fs::File;
use std::io::Read;
use serde_json::to_string;

fn main() {
	// Reads xml file
	let mut file = match File::open("./test/out.xml") {
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
	println!("Class name {}", terrain.class);

	// Get physics properties
	let physics_grid = match terrain.properties.get("PhysicsGrid") {
		Some(physics_grid) => {
		    let physics_grid_json = to_string(physics_grid).unwrap();
		    let physics_grid_bytes = physics_grid_json.as_bytes();
		//     println!("PhysicsGrid {}", physics_grid_bytes);
		},
		None => {
		    println!("PhysicsGrid not found in properties");
		}
	};

	for name in terrain.properties.keys() {
	//     let value = properties.get(name).unwrap();
	    println!("{}", name);
	}
	

}
