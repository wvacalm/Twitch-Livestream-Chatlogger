from pathlib import Path
from datetime import datetime
from dateutil import tz

def get_datetime(sstart):
    from_zone = tz.tzutc()
    to_zone = tz.tzlocal()
    date = sstart[ :sstart.find("T")]
    time = sstart[ sstart.find("T") + 1 : sstart.find("Z")]
    format = "%Y-%m-%d_%H:%M:%S"
    dt = datetime.strptime(date + "_" + time, format)
    dt = dt.replace(tzinfo=from_zone)
    dt = dt.astimezone(to_zone)
    dtstr = dt.strftime(format)
    return dtstr

def make_logpath(channel, dtstr):
    ver = 0
    print("Creating path...")
<<<<<<< HEAD
    parent = Path(f"logs/{channel}")
    if not parent.is_dir():
        parent.mkdir()
    path = Path(f"logs/{channel}/{dtstr}-{ver}.log")
    while path.is_file():
        ver += 1
        path = Path(f"logs/{channel}/{dtstr}-{ver}.log")
=======
    parent = Path(f"{channel}")
    if not parent.is_dir():
        parent.mkdir()
    path = Path(f"{channel}/{dtstr}-{ver}.log")
    while path.is_file():
        ver += 1
        path = Path(f"{channel}/{dtstr}-{ver}.log")
>>>>>>> aefc1e07c9829c5f4e9717059d053fed4182b4cd
    return path