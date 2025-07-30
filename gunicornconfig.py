import multiprocessing
import os

bind = "0.0.0.0:8000"
workers = 4
timeout = 120
worker_class = "sync"
loglevel = "info"
accesslog = "-"
errorlog = "-"