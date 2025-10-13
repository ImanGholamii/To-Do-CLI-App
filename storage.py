class StorageError(Exception):
    """Base class for storage-related errors."""
    pass


class StorageReadError(StorageError):
    """Raised when reading/parsing JSON fails."""
    pass


class StorageWriteError(StorageError):
    """Raised when writing the storage fails."""
    pass
