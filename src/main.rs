use std::fs::File;
use std::io::Read;
use rbx_dom_weak::WeakDom;
use rbx_dom_weak::Instance;

fn get_terrain(model: &WeakDom) -> Result<&Instance, ()> {
	let root = model.root();
	for child_ref in root.children(){
	    let inst = model.get_by_ref(*child_ref).unwrap();
	    if *&inst.class == "Workspace" {
		   for work_child_ref in inst.children(){
			  let work_inst = model.get_by_ref(*work_child_ref).unwrap();
			  if *&work_inst.class == "Terrain" {
				 return Ok(&work_inst);
			  }
		   }
	    }
	}
	return Err(());
 }
 

fn main() {
	// Reads xml file
	let mut file = match File::open("./test/input.rbxlx") {
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
	let terrain = match get_terrain(&model){
		Ok(terrain) => terrain,
		Err(_) => {
			println!("Error finding terrain");
			return;
		}
	};
	println!("Terrain {}", terrain.name)
}
