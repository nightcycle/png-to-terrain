use std::fs::File;
use std::io::Read;

fn main() {
	let mut file = match File::open("./test/out.xml") {
		Ok(file) => file,
		Err(e) => {
			println!("Error opening file: {}", e);
			return;
		}
	};

	let mut contents = String::new();
	match file.read_to_string(&mut contents) {
		Ok(_) => println!("File contents"),
		Err(e) => println!("Error reading file: {}", e),
	};
	
	let model = match rbx_xml::from_str_default(contents) {
		Ok(model) => model,
		Err(e) => {
			println!("Error building model: {}", e);
			return;
		}
	};
	let root = model.root();
	let terrain_ref = root.children()[0];
	let terrain = model.get_by_ref(terrain_ref).unwrap();
	println!("Class name {}", terrain.class);
	let physicsGrid = terrain.properties.get("PhysicsGrid");
	
	// println!("PhysicsGrid {}", physicsGrid);
}
