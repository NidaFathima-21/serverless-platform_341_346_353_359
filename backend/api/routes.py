#backend/api/routes
from fastapi import APIRouter, HTTPException,Request
from pydantic import BaseModel
from services.db import get_db_connection
import os
import json
from services.executor import execute_function
from fastapi.responses import JSONResponse

router = APIRouter()

class FunctionMetadata(BaseModel):
    name: str
    route: str
    language: str
    timeout: int = 5

# CREATE
@router.post("/functions/")
def create_function(meta: FunctionMetadata):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO functions (name, route, language, timeout) VALUES (%s, %s, %s, %s)",
        (meta.name, meta.route, meta.language, meta.timeout)
    )
    conn.commit()
    cursor.close()
    conn.close()
    return {"msg": "Function created", "function": meta}

# READ ALL
@router.get("/functions/")
def list_functions():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM functions")
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result

# READ ONE
@router.get("/functions/{function_id}")
def get_function(function_id: int):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM functions WHERE id = %s", (function_id,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    if not result:
        raise HTTPException(status_code=404, detail="Function not found")
    return result

# UPDATE
@router.put("/functions/{function_id}")
def update_function(function_id: int, meta: FunctionMetadata):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE functions SET name=%s, route=%s, language=%s, timeout=%s WHERE id=%s",
        (meta.name, meta.route, meta.language, meta.timeout, function_id)
    )
    conn.commit()
    affected = cursor.rowcount
    cursor.close()
    conn.close()
    if affected == 0:
        raise HTTPException(status_code=404, detail="Function not found")
    return {"msg": "Function updated", "function": meta}

# DELETE
@router.delete("/functions/{function_id}")
def delete_function(function_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM functions WHERE id = %s", (function_id,))
    conn.commit()
    affected = cursor.rowcount
    cursor.close()
    conn.close()
    if affected == 0:
        raise HTTPException(status_code=404, detail="Function not found")
    return {"msg": f"Function with ID {function_id} deleted."}
# EXECUTE
# Task 1.2 – Smart request/response + error handling
@router.post("/functions/{function_id}/invoke")
async def invoke_function(function_id: int, request: Request):
    # Fetch function metadata
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM functions WHERE id = %s", (function_id,))
    function = cursor.fetchone()
    cursor.close()
    conn.close()

    if not function:
        return JSONResponse(content={"error": "Function not found"}, status_code=404)

    # Parse request body safely
    try:
        body_bytes = await request.body()
        input_payload = json.loads(body_bytes.decode())
    except Exception:
        return JSONResponse(content={"error": "Invalid JSON input"}, status_code=400)

    # Execute function
    try:
        result = execute_function(function, input_payload)
    except Exception as e:
        return JSONResponse(content={"error": "Unexpected execution error", "detail": str(e)}, status_code=500)

    status = result.pop("status", 200)
    return JSONResponse(content=result, status_code=status)

# Task 1.3 – Warm-up endpoint
@router.post("/functions/{function_id}/warmup")
async def warmup_function(function_id: int):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM functions WHERE id = %s", (function_id,))
    function = cursor.fetchone()
    cursor.close()
    conn.close()

    if not function:
        return JSONResponse(content={"error": "Function not found"}, status_code=404)

    # Dummy payload to trigger container start
    dummy_input = {"_warmup": True}

    result = execute_function(function, dummy_input)
    status = result.pop("status", 200)

    return JSONResponse(
        content={"message": "Warm-up attempted", "result": result},
        status_code=status
    )
# Task 1.3 – Warm-up endpoint
@router.post("/functions/{function_id}/warmup")
async def warmup_function(function_id: int):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM functions WHERE id = %s", (function_id,))
    function = cursor.fetchone()
    cursor.close()
    conn.close()

    if not function:
        return JSONResponse(content={"error": "Function not found"}, status_code=404)

    # Dummy payload to trigger container start
    dummy_input = {"_warmup": True}

    result = execute_function(function, dummy_input)
    status = result.pop("status", 200)

    return JSONResponse(
        content={"message": "Warm-up attempted", "result": result},
        status_code=status
    )
# Task 1.3 – Warm-up endpoint
@router.post("/functions/{function_id}/warmup")
async def warmup_function(function_id: int):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM functions WHERE id = %s", (function_id,))
    function = cursor.fetchone()
    cursor.close()
    conn.close()

    if not function:
        return JSONResponse(content={"error": "Function not found"}, status_code=404)

    # Dummy payload to trigger container start
    dummy_input = {"_warmup": True}

    result = execute_function(function, dummy_input)
    status = result.pop("status", 200)

    return JSONResponse(
        content={"message": "Warm-up attempted", "result": result},
        status_code=status
    )
# Task 1.3 – Warm-up endpoint
@router.post("/functions/{function_id}/warmup")
async def warmup_function(function_id: int):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM functions WHERE id = %s", (function_id,))
    function = cursor.fetchone()
    cursor.close()
    conn.close()

    if not function:
        return JSONResponse(content={"error": "Function not found"}, status_code=404)

    # Dummy payload to trigger container start
    dummy_input = {"_warmup": True}

    result = execute_function(function, dummy_input)
    status = result.pop("status", 200)

    return JSONResponse(
        content={"message": "Warm-up attempted", "result": result},
        status_code=status
    )
