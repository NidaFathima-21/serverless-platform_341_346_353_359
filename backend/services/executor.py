import os
import subprocess
import json
import uuid
import tempfile
from services.pool import start_container

# Dynamically resolve base path to /functions folder
BASE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'functions'))
print("[DEBUG] BASE_PATH is:", BASE_PATH)
DOCKER_TIMEOUT = 5

def execute_function(function, event):
    func_id = function["id"]
    language = function["language"].lower()
    func_path = os.path.join(BASE_PATH, language, str(func_id))

    print("========== DEBUG START ==========")
    print("Function ID:", func_id)
    print("Language:", language)
    print("Expected function path:", func_path)
    print("Exists?", os.path.exists(func_path))
    print("========== DEBUG END ==========")

    if not os.path.exists(func_path):
        return {"error": "Function code not found", "status": 404}

    code_file = "function.py" if language == "python" else "function.js"
    if not os.path.exists(os.path.join(func_path, code_file)):
        return {"error": f"{code_file} missing in function directory", "status": 400}

    # Load test_input.json if event is empty (e.g., warm-up)
    if not event:
        test_input_path = os.path.join(func_path, "test_input.json")
        if os.path.exists(test_input_path):
            try:
                with open(test_input_path) as f:
                    event = json.load(f)
                print("[DEBUG] Loaded test_input.json for fallback input")
            except Exception as e:
                return {"error": f"Failed to load test_input.json: {str(e)}", "status": 400}
        else:
            event = {"_warmup": True}

    # Write event to temporary input file
    temp_input = os.path.join(tempfile.gettempdir(), f"input_{uuid.uuid4().hex}.json")
    with open(temp_input, "w") as f:
        json.dump(event, f)

    # Start or reuse container
    try:
        container_id = start_container(func_id, language, func_path)
    except Exception as e:
        return {"error": str(e), "status": 500}

    # Copy the input file into the running container
    copy_cmd = ["docker", "cp", temp_input, f"{container_id}:/tmp/input.json"]
    copy_result = subprocess.run(copy_cmd, capture_output=True, text=True)
    if copy_result.returncode != 0:
        return {"error": "Failed to copy input to container", "stderr": copy_result.stderr.strip(), "status": 500}

    # Run the handler inside the already running container
    exec_cmd = [
        "docker", "exec", container_id,
        "python" if language == "python" else "node",
        "/app/entrypoint.py" if language == "python" else "/app/entrypoint.js"
    ]

    try:
        print("[DEBUG] Exec command:", " ".join(exec_cmd))
        result = subprocess.run(exec_cmd, capture_output=True, text=True, timeout=DOCKER_TIMEOUT)
        print("[DEBUG] STDOUT:", result.stdout)
        print("[DEBUG] STDERR:", result.stderr)

        if result.returncode != 0:
            return {
                "error": "Docker execution failed",
                "stderr": result.stderr.strip(),
                "status": 500
            }

        output = result.stdout.strip()
        try:
            parsed = json.loads(output)
            if isinstance(parsed, dict):
                return {**parsed, "status": 200}
            else:
                return {"output": parsed, "status": 200}
        except json.JSONDecodeError:
            return {"error": "Invalid output format (not JSON)", "raw": output, "status": 502}

    except subprocess.TimeoutExpired:
        return {"error": "Function execution timed out", "status": 408}
    except Exception as e:
        return {"error": str(e), "status": 500}
    finally:
        if os.path.exists(temp_input):
            os.remove(temp_input)
