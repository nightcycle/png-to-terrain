import hashlib
import toml
import base64
import json
from typing import TypedDict
from bitstring import BitArray

material_color_bin_str = """![CDATA[AAAAAAAAan8/P39rf2Y/ilY+j35fi21PZmxvZbDqw8faiVpHOi4kHh4lZlw76JxKc3trhHta
gcLgc4RKxr21zq2UlJSM]]"""

phys_grid_bin_str = """![CDATA[AgMAAAAE//8A//8A//8A//8BAAAAAAAAAAAAAAEAAP8AAP8AAP8AAf8AAAAAAAAAAAAAAAEA
AAAAAAAAAAA="""

smooth_grid_bin_str = """![CDATA[AQUAAAAAAAAAAAAAAACA/4AfAoAJAkJNgBICQldCMoAHQplCgIASAkKegguA/4D/gP+AvMJN
AYAdQoBCmYAUQgSAB4IBgP+A/4D/gP+A/4D/gP+A/4D/gP+A/4D/gP+A/4D/gP+A/4D/gP+A
/4D/gP+A/4D/gP+A/4D/gP+A/4D/gP+A/4D/gP+A/4D/gP+A/4D/gP+A/4D/gP+A/4D/gP+A
/4D/gP+A/4D/gP+A/4D/gP+A/4D/gP+A/4D/gP+A/4D/gP+A/4D/gP+A/4D/gP+A/4D/gP+A
/4D/gP+A/4D/gP+A/4D/gP+A/4D/gP+A/4D/gP+A/4D/gP+A/4D/gP+A/4D/gP+A/4D/gP+A
/4D/gP+A/4D/gP+A/4D/gP+A/4D/gP+A/4D/gP+A/4D/gP+A/4D/gP+A/4CS]]"""

def get_bytes_from_binary_str(bin_str: str) -> bytes:
	clean_data = bin_str.replace('![CDATA[', '').replace(']]', '').replace('\n', '').strip()
	return base64.b64decode(clean_data)

def get_bits_from_bytes(b: bytes) -> str:
	return bin(b)[2:]

def decode_binary_string(bin_str: str) -> list[int]:
	# Remove the CDATA tag and any newlines/whitespace
	output = []
	for b in get_bytes_from_binary_str(bin_str):
		output.append(int.from_bytes(bytes([b]), 'big'))

	return output

def decode_material_colors(binary_str: str) -> dict[str: str]:
	colors = []
	color_values = decode_binary_string(binary_str)
	mat_order = [
		"Air",
		"Water",
		"Grass",
		"Slate",
		"Concrete",
		"Brick",
		"Sand",
		"WoodPlanks",
		"Rock",
		"Glacier",
		"Snow",
		"Sandstone",
		"Mud",
		"Basalt",
		"Ground",
		"CrackedLava",
		"Asphalt",
		"Cobblestone",
		"Ice",
		"LeafyGrass",
		"Salt",
		"Limestone",
		"Pavement",			
	]
	for i, val in enumerate(color_values):
		if round(i/3) == i/3 and i+2 <= len(color_values):
			r = val
			g = color_values[i+1]
			b = color_values[i+2]
			colors.append([r,g,b])

	def rgb_to_hex(rgb):
		return '%02x%02x%02x' % rgb

	color_registry = {}
	for i, color in enumerate(colors):
		if i > 1:
			key = mat_order[i]
			hex_val = rgb_to_hex((color[0], color[1], color[2]))
			color_registry[key] = hex_val

	return color_registry

# get material colors
# print(json.dumps(decode_material_colors(material_color_bin_str), indent=4))

# get smooth grid https://zeux.io/2017/03/27/voxel-terrain-storage/
smooth_grid_values = decode_binary_string(smooth_grid_bin_str)
print(smooth_grid_values)
