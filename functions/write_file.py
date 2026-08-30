import os
schema_write_file = {
"type": "function",
"function": {
"name": "write_file",
"description": "Writing files",
"parameters": {
"type": "object",
"required": ["file_path", "content"],
"properties": {
        "file_path": {
                "type": "string",
                "description": "file path of file that will be written"
                      },
        "content": {
                 "type": "string",
                "description": "text will be written" 
},
},
},
},
}
def write_file(working_directory: str, file_path: str, content: str) -> str:
	try:
		working_dir_abs = os.path.abspath(working_directory)
		target_path = os.path.normpath(os.path.join(working_dir_abs,file_path))
                # Will be True or False
		valid_target_dir = os.path.commonpath([working_dir_abs, target_path]) == working_dir_abs
		if valid_target_dir == False:
			return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
		elif os.path.isdir(target_path) == True:
			return f'Error: Cannot write to "{file_path}" as it is a directory'
		os.makedirs(os.path.dirname(target_path),exist_ok=True)
		with open(target_path, "w") as f:
			f.write(content)
			return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
	except Exception as e:
                return f'Error: {e}'


