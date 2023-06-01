try:  # pragma: no cover
    import dotenv

    dotenv.load_dotenv(verbose=True)
except ImportError:  # pragma: no cover
    pass
