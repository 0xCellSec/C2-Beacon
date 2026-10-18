import uuid
from app.core.models import BeaconMeta, BeaconLog

"""
beacon: 

what will it do? 
* initially sends a registration message to the server
* once registered, periodically contact the server for any pending tasks using an exponential backoff strategy
* if task is pending, execute task and return results 

"""


