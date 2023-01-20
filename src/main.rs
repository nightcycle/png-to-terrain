use std::fs::File;
use std::io::Read;
use rbx_dom_weak::WeakDom;
use rbx_dom_weak::Instance;
use std::path::Path;
use std::io::BufReader;
use serde_json::{Map, Value};

// Get the terrain from the dom
fn get_terrain(dom: &WeakDom) -> Result<&Instance, ()> {
	let root = dom.root();
	for child_ref in root.children(){
	    let inst = dom.get_by_ref(*child_ref).unwrap();
	    if *&inst.class == "Workspace" {
		   for work_child_ref in inst.children(){
			  let work_inst = dom.get_by_ref(*work_child_ref).unwrap();
			  if *&work_inst.class == "Terrain" {
				 return Ok(&work_inst);
			  }
		   }
	    }
	}
	return Err(());
}

fn parse_json_string(json_string: &str) -> Result<Map<String, Value>, serde_json::Error> {
    let json_value: Value = serde_json::from_str(json_string)?;
    let json_map = json_value.as_object().unwrap().clone();
    Ok(json_map)
}

fn get_bin_str_from_property(inst: &Instance, prop_name: &str) -> Result<String, ()> {
	let prop_variant = inst.properties.get(prop_name).unwrap();
	let prop_str = serde_json::to_string(prop_variant).unwrap();
	let json_value = match parse_json_string(&prop_str){
		Ok(map) => map,
		Err(_) => {
			println!("Error getting json");
			return Err(());
		}
	};
	let val_str = serde_json::to_string(json_value.get("BinaryString").unwrap()).unwrap();
	return Ok(val_str);
}

// Get the dom from the path
fn get_dom(rbx_path: &str) -> Result<WeakDom, ()> {
	// Reads xml file
	let file_path = Path::new(rbx_path);
	let file_extension = file_path.extension().unwrap().to_str().unwrap();
	
	let mut file = match File::open(rbx_path) {
		Ok(file) => file,
		Err(e) => {
			println!("Error opening file: {}", e);
			return Err(());
		}
	};

	if file_extension == "rbxlx" {	
		// Gets content of file
		let mut contents = String::new();
		match file.read_to_string(&mut contents) {
			Ok(_) => println!("File contents"),
			Err(e) => println!("Error reading file: {}", e),
		};
	
		// Imports xml str to rbx_xml
		let dom = match rbx_xml::from_str_default(contents) {
			Ok(dom) => dom,
			Err(e) => {
				println!("Error building model: {}", e);
				return Err(());
			}
		};
		return Ok(dom);
	}else if file_extension == "rbxl" {
		let reader: BufReader<File> = BufReader::new(file);

		// Imports xml str to rbx_xml
		let dom = match rbx_binary::from_reader(reader){
			Ok(dom) => dom,
			Err(e) => {
				println!("Error building model: {}", e);
				return Err(());
			}
		};
		return Ok(dom);
	}
	return Err(());
}

fn main() {
	let rbx_path = "./test/input.rbxl";

	// get place dom
	let dom = match get_dom(rbx_path){
		Ok(dom) => dom,
		Err(_) => {
			println!("Error finding dom");
			return;
		}
	};

	// Gets Terrain instance
	let terrain = match get_terrain(&dom){
		Ok(terrain) => terrain,
		Err(_) => {
			println!("Error finding terrain");
			return;
		}
	};
	println!("Instance:- {}", terrain.name);

	// Get the smooth grid
	let smooth_grid_str: String = match get_bin_str_from_property(terrain, "SmoothGrid"){
		Ok(val_str) => val_str,
		Err(_) => {
			println!("Error getting binary string");
			return;
		}
	};
	println!("smooth_grid: {}", &smooth_grid_str);

}
