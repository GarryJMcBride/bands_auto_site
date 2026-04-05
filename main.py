import uvicorn

TESTING_PORT = 8000


def main(port: int = TESTING_PORT) -> None:
    """Run the FastAPI app with Uvicorn.

    Parameters
    ----------
    port : int, optional
        The port number to run the app on (default is 8000 for testing).

    Returns
    -------
    None

    Notes
    -----
    - This function starts the Uvicorn server to serve the FastAPI app defined in `src.backend.app`.
    - The `reload=True` option is used for development to automatically reload the server on code
        changes. This should be set to `False` in production for better performance.
    - The `workers` parameter can be adjusted based on the expected load and server capabilities.

    This function does not return anything; it starts the server.

    """
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
