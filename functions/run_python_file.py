import os
import subprocess
schema_run_python_file = {
"type": "function",
"function": {
"name": "run_python_file",
"description": "Executes a Python script and can accept optional arguments",
"parameters": {
"type": "object",
"required": ["file_path"],
"properties": {
	"file_path": {
		"type": "string",
		"description": "file path of python file to execute"
		      },
	"args": {
		"type": "array",
		"items": {
			"type": "string"
					},
		"description": "optional command-line arguments passed to the Python file/script",
}
},
},
},
}
def run_python_file(working_directory:str, file_path: str, args: list[str] | None = None) -> str:    
	try:
		working_dir_abs = os.path.abspath(working_directory)
		target_path = os.path.normpath(os.path.join(working_dir_abs,file_path))
		# Will be True or False
		valid_target_dir = os.path.commonpath([working_dir_abs, target_path]) == working_dir_abs
		if valid_target_dir == False:
                	return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
		elif os.path.isfile(target_path) == False:
			return  f'Error: "{file_path}" does not exist or is not a regular file'
		elif file_path.endswith('.py') == False:
                	return f'Error: "{file_path}" is not a Python file'
		command = ["python", target_path]
		if args is not None:
			command.extend(args)
		result = subprocess.run(command,cwd=working_dir_abs,capture_output=True,text=True,timeout=30)
		parts = []
		if result.returncode != 0:
			parts.append(f'Process exited with code {result.returncode}')
		if result.stdout == "" and result.stderr == "":
			parts.append("No output produced")
		else:
			parts.append(f'STDOUT: {result.stdout}')
			parts.append(f'STDERR: {result.stderr}')
		whole = "\n".join(parts)
		return whole
	except Exception as e:
		return f'Error: {e}'
