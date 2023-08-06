from typing import Optional, List
from enum import Enum

from .base import BaseModel
from .attachments import Like, Repost, Attachment, Geo

from .additional import PostSource, Donut

# https://vk.com/dev/objects/post


class WallPostComments(BaseModel):
    count: int
    can_post: int
    groups_can_post: int
    can_close: Optional[bool]
    can_open: Optional[bool]


class Copyright(BaseModel):
    id: int
    link: str
    name: str
    type: str


class View(BaseModel):
    count: int


class PostType(Enum):
    post = 'post'
    copy = 'copy'
    reply = 'reply'
    postpone = 'postpone'
    suggest = 'suggest'


class WallPost(BaseModel):
    id: int
    owner_id: int
    from_id: int
    created_by: Optional[int]
    date: int
    text: str
    reply_owner_id: Optional[int]
    reply_post_id: Optional[int]
    friends_only: Optional[int]
    comments: WallPostComments
    copyright: Optional[Copyright]
    likes: Like
    reposts: Repost
    views: View
    post_type: PostType
    post_source: PostSource
    attachments: List[Attachment]
    geo: Optional[Geo]
    signer_id: Optional[int]
    copy_history: Optional['WallPost']
    can_pin: Optional[int]
    can_delete: Optional[int]
    can_edit: Optional[int]
    is_pinned: Optional[int]
    marked_as_ads: int
    is_favorite: bool
    donut: Optional[Donut]
    postponed_id: Optional[int]
