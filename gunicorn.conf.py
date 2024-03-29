bind = "0.0.0.0:8001"  # Or "unix:/tmp/gunicorn.sock"
daemon = True            # Whether work in the background
debug = False            # Some extra logging
logfile = "/srv/x/ourfield/_logs/gunicorn.log"
loglevel = "info"        # The level at which to log
pidfile = "gunicorn.pid" # Path to a PID file
workers = 2              # Number of workers to initialize
umask = 0                # Umask to set when daemonizing
user = "www-data"        # Change process owner to user
group = None             # Change process group to group

def after_fork(server, worker):
    fmt = "worker=%s spawned pid=%s"
    server.log.info(fmt % (worker.id, worker.pid))

def before_fork(server, worker):
    fmt = "worker=%s spawning"
    server.log.info(fmt % worker.id)

def before_exec(server):
    serer.log.info("Forked child, reexecuting.")