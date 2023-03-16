import hashlib
import toml
import base64
import json

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

def extract_6bit_number(byte_value: bytes):
    mask = 0x3F  # Lower 6 bits are set to 1
    six_bit_number = byte_value & mask
    return six_bit_number

def get_bytes_from_binary_str(bin_str: str) -> bytes:
	clean_data = bin_str.replace('![CDATA[', '').replace(']]', '').replace('\n', '').strip()
	return base64.b64decode(clean_data)

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
		"_0",
		"_1",
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

smooth_grid_runs = []

def extract_6bits(index: int, input_bytes: bytes):
    first_byte = input_bytes[index]
    first_6bits = first_byte >> 2
    return bytes([first_6bits])

def extract_byte(index: int, input_bytes: bytes):
    first_byte = input_bytes[index]
    return bytes([first_byte])

def extract_bit_val(index: int, byte_value: bytes) -> int:
    if isinstance(byte_value, bytes):
        byte_value = byte_value[0]

    if 0 <= index < 8:
        mask = 1 << index
        return (byte_value & mask) >> index
    else:
        raise ValueError("Index must be between 0 and 7")

def byte_to_binary(byte: bytes) -> str:
	return bin(int.from_bytes(byte, 'big'))[2:]

def binary_to_bytes(s: bytes):
    v = int(s, 2)
    b = bytearray()
    while v:
        b.append(v & 0xff)
        v >>= 8
    return bytes(b[::-1])

smooth_grid_bytes = get_bytes_from_binary_str(smooth_grid_bin_str)
def get_byte_run_info(index: int):

	lead_byte = extract_byte(index, smooth_grid_bytes)
	lead_binary = byte_to_binary(lead_byte)
	index += 1

	if len(lead_binary) < 8:
		print(index, " unknown: ", int.from_bytes(lead_byte, 'big'))
		return index


	print("\nLEAD", index-1, ": ", lead_byte, " = ", byte_to_binary(lead_byte))
	material_byte = binary_to_bytes(lead_binary[2:])
	print(material_byte)
	material = int.from_bytes(material_byte, 'big')

	print("MATERIAL", material)
	has_occupancy_byte = int(lead_binary[0])
	has_run_len_byte = int(lead_binary[1])

	occupancy = 0 # Occupancy value for the voxel run
	run_len = 0 # Run length of the voxel run minus one

	if has_occupancy_byte == 1:
		occupancy_byte = smooth_grid_bytes[index]
		if type(occupancy_byte) == bytes:
			occupancy = int.from_bytes(occupancy_byte, 'big')
		else:
			occupancy = occupancy_byte
		index += 1

	if has_run_len_byte == 1:
		run_len_byte = smooth_grid_bytes[index]
		if type(run_len_byte) == bytes:
			run_len = int.from_bytes(run_len_byte, 'big')
		else:
			run_len = run_len_byte

		index += 1
		
	print("OCCUPANCY", occupancy)
	print("RUN_LEN", run_len)

	return index + run_len

i = 0
while i < len(smooth_grid_bytes)-1:
	i = get_byte_run_info(i)

# def extract_bit(byte_value, index):
#     if isinstance(byte_value, bytes):
#         byte_value = byte_value[0]

#     if 0 <= index < 8:
#         mask = 1 << index
#         return (byte_value & mask) >> index
#     else:
#         raise ValueError("Index must be between 0 and 7")

# # Example usage:
# byte_value = b'\xd2'  # Just an example byte
# index = 2
# result = extract_bit(byte_value, index)
# print(result)  # Output: 1 (the bit at position 2 is 1)