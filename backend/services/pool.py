# backend/services/pool.py

import subprocess

POOL = {}

def start_container(func_id, language, func_path):
    container_name = f"pool_{language}_{func_id}"

    if container_name in POOL:
        return POOL[container_name]

    image = "function-runner-python" if language == "python" else "function-runner-js"

    cmd = [
        "docker", "run", "-d",
        "--name", container_name,
        "-v", f"{func_path}:/function",  # 🟢 Don't override /app!
        image
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode == 0:
        container_id = result.stdout.strip()
        POOL[container_name] = container_id
        return container_id
    else:
        raise RuntimeError(f"Failed to start container: {result.stderr.strip()}")
