import logging


# Rest Countries API path -- don't change unless you know what you're doing
API_PATH = 'https://api.bitbucket.org/2.0/'

# If set, write data to ingester under this address
INGESTER_PATH = 'http://localhost:9002'
# Write data to stdout
VERBOSE = False

# Maximum number of commits per repository, set to None to turn off
LIMIT = None

# Log file destination, absolute or relative to execution
LOG_FILE = 'restcountries.log'
# Writes log to file if True
LOG_TO_FILE = True
# Writes log to error console if True
LOG_TO_STDERR = True
# Ignore log levels below this. Available: DEBUG, INFO, WARNING, ERROR, CRITICAL
LOG_LEVEL = logging.INFO
# Prefix for log lines. See `logging` module documentation for details.
LOG_FORMAT = '%(asctime)s %(levelname)s: %(message)s'

# If True, cache requests
CACHE_ENABLED = False
# Cache store location
CACHE_PATH = '.cache/'
# Maximum age of cached contents in seconds
CACHE_SECONDS = 1 * 24 * 3600  # 1 day
# Non-200 response types to cache anyway
CACHE_STATUS = [404]

# Timeout for requests
REQUEST_TIMEOUT = 20
# Number of retries for failed requests
REQUEST_RETRIES = 3
