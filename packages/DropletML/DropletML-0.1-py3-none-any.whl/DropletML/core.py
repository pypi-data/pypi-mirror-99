import s3fs  # https://s3fs.readthedocs.io/en/latest/
import uuid
import inspect

class Droplet1(object):
    def __init__(self, tag):
        self.tag = tag
        self.uuid = uuid.uuid1()
        self.bucket = "rainpuddle"
        self.location = f"{self.bucket}/{self.tag}{self.uuid}.pt"

    def __call__(self):
        s3 = s3fs.S3FileSystem(anon=False)

        curframe = inspect.currentframe()
        calframe = inspect.getouterframes(curframe, 2)
        for i in range(5):
            frame = calframe[1][i]
            if type(frame) == list:
                for f in frame:
                    if 'save' in f:
                        mode = 'wb'
                        print(f'Writing to {self.location}')
                        return s3.open(self.location, mode)
                    
        mode = 'rb'
        print(f'Reading from {self.location}')
        return s3.open(self.location, mode)


def droplet(tag):
    tag = tag
    _uuid = str(uuid.uuid1()).split('-')[0]
    bucket = "rainpuddle"
    location = f"{bucket}/{tag}-{_uuid}.pt"

    s3 = s3fs.S3FileSystem(anon=False)

    curframe = inspect.currentframe()
    calframe = inspect.getouterframes(curframe, 2)
    for i in range(5):
        frame = calframe[1][i]
        if type(frame) == list:
            for f in frame:
                if 'save' in f:
                    mode = 'wb'
                    print(f'Writing to {location}')
                    return s3.open(location, mode)
                
    mode = 'rb'
    print(f'Reading from {tag}')
    return s3.open(tag, mode)