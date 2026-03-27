import uvicorn


def main() -> None:
    uvicorn.run(
        "src.backend.app:app",  # "filename:variable_name" — points Uvicorn to app.py
        host="127.0.0.1",  # localhost only for local dev
        port=8000,  # desired port
        reload=True,  # auto-reload on code changes (development only)
    )


if __name__ == "__main__":
    main()
