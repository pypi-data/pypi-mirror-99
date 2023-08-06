from enum import Enum
from typing import Optional

from ..base import BaseModel

# https://vk.com/dev/objects/post_source


class Type(Enum):
    vk = 'vk'
    widget = 'widget'
    api = 'api'
    rss = 'rss'
    sms = 'sms'


class Platform(Enum):
    android = 'android'
    iphone = 'iphone'
    wphone = 'wphone'


class Data(Enum):
    profile_activity = 'profile_activity'
    profile_photo = 'profile_photo'
    comments = 'comments'
    like = 'like'
    poll = 'poll'


class PostSource(BaseModel):
    type: Type
    platform: Optional[Platform]
    data: Optional[Data]
    url: Optional[str]
