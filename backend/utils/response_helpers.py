from fastapi.responses import JSONResponse

def success_response(data: dict, message: str = "Success"):
    return JSONResponse({"status": "success", "message": message, "data": data})

def error_response(message: str, status_code: int = 400):
    return JSONResponse({"status": "error", "message": message}, status_code=status_code)
