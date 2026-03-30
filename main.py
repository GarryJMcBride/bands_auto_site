import uvicorn

TESTING_PORT = 8000


def main(port: int = TESTING_PORT) -> None:  #
    workers = 1
    uvicorn.run(
        "src.backend.app:app",  # "filename:variable_name" — points Uvicorn to app.py
        host="127.0.0.1",  # localhost only for local dev
        port=port,  # desired port
        reload=True,  # auto-reload on code changes (development only)
        workers=workers,
    )


# add different port number into `main()` for another instance of the app, e.g. for testing
if __name__ == "__main__":
    main()
