try:
    from portalocker import Lock as _Lock
    from portalocker.constants import LOCK_EX, LOCK_SH
    class Lock(_Lock):
        def __init__(self, path, flags, *args, **kwargs):
            _Lock.__init__(self,path,*args,flags=flags,timeout=None,**kwargs)
except ModuleNotFoundError:
    import os
    import fcntl
    from fcntl import LOCK_EX, LOCK_SH
    # file locking from fcntl
    def lock_file(f, cmd=fcntl.LOCK_EX):
        fcntl.flock(f, cmd)
        return f
    def unlock_file(f):
        fcntl.flock(f, fcntl.LOCK_UN)
        return f

    # This file opener *must* be used in a "with" block.
    class Lock:
        # Open the file with arguments provided by user. Then acquire
        # a lock on that file object (WARNING: Advisory locking).
        def __init__(self, path, flags, *args, **kwargs):
            # Open the file and acquire a lock on the file before operating
            self.file = open(path, mode='w+', *args, **kwargs)
            # Lock the opened file
            self.file = lock_file(self.file, flags) # flags are either LOCK_EX or LOCK_SH

        # Return the opened file object (knowing a lock has been obtained).
        def __enter__(self, *args, **kwargs): return self.file

        # Unlock the file and close the file object.
        def __exit__(self, exc_type=None, exc_value=None, traceback=None):
            # Flush to make sure all buffered contents are written to file.
            self.file.flush()
            os.fsync(self.file.fileno())
            # Release the lock on the file.
            self.file = unlock_file(self.file)
            self.file.close()
            # Handle exceptions that may have come up during execution, by
            # default any exceptions are raised to the user.
            return exc_type == None
