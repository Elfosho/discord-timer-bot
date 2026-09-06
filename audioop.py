# Stub implementation of the deprecated 'audioop' module for Python 3.14+.
# The discord library imports this module, but its audio‑related functions are not used
# in this bot (it only uses voice state intents). Providing an empty module prevents
# the import error while keeping the runtime lightweight.

def __getattr__(name):
    """Return a dummy function for any attribute that discord might try to call.
    This raises a clear error if an unexpected audio operation is actually requested.
    """
    def _missing(*args, **kwargs):
        raise NotImplementedError(
            f"audioop.{name} is not implemented in the stub module. Voice/audio functionality is not required for this bot."
        )
    return _missing
