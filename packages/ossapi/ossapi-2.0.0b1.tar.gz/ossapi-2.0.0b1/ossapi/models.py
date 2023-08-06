# opt-in to forward type annotations
# https://docs.python.org/3.7/whatsnew/3.7.html#pep-563-postponed-evaluation-of-annotations
from __future__ import annotations
from dataclasses import dataclass
from typing import Optional, TypeVar, Generic, Any, List
from types import SimpleNamespace

from ossapi.mod import Mod
from ossapi.enums import *
from ossapi.utils import Datetime

T = TypeVar("T")


"""
a type hint of ``Optional[Any]`` or ``Any`` means that I don't know what type it
is, not that the api actually lets any type be returned there.
"""

# =================
# Documented Models
# =================

@dataclass
class UserCompact:
    """
    https://osu.ppy.sh/docs/index.html#usercompact
    """
    # required fields
    # ---------------
    avatar_url: str
    country_code: str
    default_group: str
    id: int
    is_active: bool
    is_bot: bool
    is_deleted: bool
    is_online: bool
    is_supporter: bool
    last_visit: bool
    pm_friends_only: bool
    profile_colour: str
    username: str

    # optional fields
    # ---------------
    account_history: Optional[List[UserAccountHistory]]
    active_tournament_banner: Optional[ProfileBanner]
    badges: Optional[List[UserBadge]]
    beatmap_playcounts_count: Optional[int]
    blocks: Optional[UserRelation]
    country: Optional[Country]
    cover: Optional[Cover]
    favourite_beatmapset_count: Optional[int]
    # undocumented
    follow_user_mapping: Optional[List[int]]
    follower_count: Optional[int]
    friends: Optional[List[UserRelation]]
    graveyard_beatmapset_count: Optional[int]
    groups: Optional[List[UserGroup]]
    is_admin: Optional[bool]
    is_bng: Optional[bool]
    is_full_bn: Optional[bool]
    is_gmt: Optional[bool]
    is_limited_bn: Optional[bool]
    is_moderator: Optional[bool]
    is_nat: Optional[bool]
    is_restricted: Optional[bool]
    is_silenced: Optional[bool]
    loved_beatmapset_count: Optional[int]
    # undocumented
    mapping_follower_count: Optional[int]
    monthly_playcounts: Optional[List[UserMonthlyPlaycount]]
    page: Optional[UserPage]
    previous_usernames: Optional[List[str]]
    ranked_and_approved_beatmapset_count: Optional[int]
    replays_watched_counts: Optional[List[UserReplaysWatchedCount]]
    scores_best_count: Optional[int]
    scores_first_count: Optional[int]
    scores_recent_count: Optional[int]
    statistics: Optional[UserStatistics]
    statistics_rulesets: Optional[UserStatisticsRulesets]
    support_level: Optional[int]
    unranked_beatmapset_count: Optional[int]
    unread_pm_count: Optional[int]
    user_achievements: Optional[List[UserAchievement]]
    user_preferences: Optional[UserProfileCustomization]
    rank_history: Optional[RankHistory]
    # this is deprecated, TODO remove when the api does
    rankHistory: Optional[RankHistory]

@dataclass
class User(UserCompact):
    comments_count: int
    cover_url: str
    discord: Optional[str]
    has_supported: bool
    interests: Optional[str]
    join_date: Datetime
    kudosu: Kudosu
    location: Optional[str]
    max_blocks: int
    max_friends: int
    occupation: Optional[str]
    playmode: str
    playstyle: Optional[PlayStyles]
    post_count: int
    profile_order: List[ProfilePage]
    title: Optional[str]
    # undocumented
    title_url: Optional[Any]
    twitter: Optional[str]
    website: Optional[str]



@dataclass
class BeatmapCompact:
    # required fields
    # ---------------
    difficulty_rating: float
    id: int
    mode: GameMode
    status: RankStatus
    total_length: int
    version: str

    # optional fields
    # ---------------
    beatmapset: Optional[BeatmapsetCompact]
    checksum: Optional[str]
    failtimes: Optional[Failtimes]
    max_combo: Optional[int]


@dataclass
class Beatmap(BeatmapCompact):
    total_length: int
    version: str
    accuracy: int
    ar: int
    beatmapset_id: int
    bpm: int
    convert: bool
    count_circles: int
    count_sliders: int
    count_spinners: int
    cs: int
    deleted_at: str
    drain: int
    hit_length: int
    is_scoreable: bool
    last_updated: Datetime
    mode_int: int
    passcount: int
    playcount: int
    ranked: int
    url: str

    # overridden fields
    # -----------------
    beatmapset: Optional[Beatmapset]


@dataclass
class BeatmapsetCompact:
    """
    https://osu.ppy.sh/docs/index.html#beatmapsetcompact
    """
    # required fields
    # ---------------
    artist: str
    artist_unicode: str
    covers: Covers
    creator: str
    favourite_count: int
    id: int
    play_count: int
    preview_url: str
    source: str
    status: RankStatus
    title: str
    title_unicode: str
    user_id: int
    video: str
    # documented as being in ``Beatmapset`` only, but returned by
    # ``api.beatmapset_events`` which uses a ``BeatmapsetCompact``.
    hype: Hype
    # undocumented
    nsfw: bool

    # optional fields
    # ---------------
    beatmaps: Optional[List[Beatmap]]
    converts: Optional[Any]
    current_user_attributes: Optional[Any]
    description: Optional[Any]
    discussions: Optional[Any]
    events: Optional[Any]
    genre: Optional[Any]
    has_favourited: Optional[bool]
    language: Optional[Any]
    nominations: Optional[Any]
    ratings: Optional[Any]
    recent_favourites: Optional[Any]
    related_users: Optional[Any]
    user: Optional[UserCompact]

@dataclass
class Beatmapset(BeatmapsetCompact):
    availability: Availability
    bpm: int
    can_be_hyped: bool
    discussion_enabled: bool
    discussion_locked: bool
    is_scoreable: bool
    last_updated: Datetime
    legacy_thread_url: Optional[str]
    nominations_summary: Nominations
    ranked: RankStatus
    ranked_date: Optional[Datetime]
    storyboard: bool
    submitted_date: Optional[Datetime]
    tags: str


@dataclass
class Match:
    pass

@dataclass
class Score:
    """
    https://osu.ppy.sh/docs/index.html#score
    """
    id: int
    best_id: int
    user_id: int
    accuracy: float
    mods: Mod
    score: int
    max_combo: int
    perfect: bool
    statistics: Statistics
    pp: float
    rank: int
    created_at: Datetime
    mode: GameMode
    mode_int: int
    replay: bool

    beatmap: Optional[Beatmap]
    beatmapset: Optional[BeatmapsetCompact]
    rank_country: Optional[int]
    rank_global: Optional[int]
    weight: Optional[float]
    user: Optional[UserCompact]
    match: Optional[Match]

@dataclass
class BeatmapUserScore:
    position: int
    score: Score


@dataclass
class CommentableMeta:
    # this class is currently not following the documentation in order to work
    # around https://github.com/ppy/osu-web/issues/7317. Will be updated when
    # that issue is resolved (one way or the other).
    id: Optional[int]
    title: str
    type: Optional[str]
    url: Optional[str]
    # undocumented
    owner_id: Optional[int]
    owner_title: Optional[str]

@dataclass
class Comment:
    commentable_id: int
    commentable_type: str
    created_at: Datetime
    deleted_at: Optional[Datetime]
    edited_at: Optional[Datetime]
    edited_by_id: Optional[int]
    id: int
    legacy_name: Optional[str]
    message: Optional[str]
    message_html: Optional[str]
    parent_id: Optional[int]
    pinned: bool
    replies_count: int
    updated_at: Datetime
    user_id: int
    votes_count: int

# Cursors are an interesting case. As I understand it, they don't have a
# predefined set of attributes across all endpoints, but instead differ per
# endpoint. I don't want to have dozens of different cursor classes (although
# that would perhaps be the proper way to go about this), so just allow
# any attribute.
# We do, however, have to tell our code what type each attribute is, if we
# receive that atttribute. So ``__annotations`` will need updating as we
# encounter new cursor attributes.
class Cursor(SimpleNamespace):
    __annotations__ = {
        "created_at": Datetime,
        "id": int,
        "_id": str,
        "queued_at": str,
        "approved_date": Datetime,
        "last_update": str,
        "votes_count": int,
        "page": int
    }

@dataclass
class CommentBundle:
    commentable_meta: List[CommentableMeta]
    comments: List[Comment]
    has_more: bool
    has_more_id: Optional[int]
    included_comments: List[Comment]
    pinned_comments: Optional[List[Comment]]
    sort: str
    top_level_count: Optional[int]
    total: Optional[int]
    user_follow: bool
    user_votes: List[int]
    users: List[UserCompact]
    # undocumented
    cursor: Cursor


@dataclass
class ForumPost:
    pass

@dataclass
class ForumTopic:
    pass


@dataclass
class ForumTopicAndPosts:
    cursor: Cursor
    search: str
    posts: List[ForumPost]
    topic: ForumTopic

@dataclass
class SearchResult(Generic[T]):
    data: List[T]
    total: int


@dataclass
class WikiPage:
    layout: str
    locale: str
    markdown: str
    path: str
    subtitle: Optional[str]
    tags: List[str]
    title: str

@dataclass
class Search:
    user: Optional[SearchResult[UserCompact]]
    wiki_page: Optional[SearchResult[WikiPage]]

@dataclass
class Spotlight:
    end_date: Datetime
    id: int
    mode_specific: int
    participant_count: Optional[int]
    name: int
    start_date: Datetime
    type: str

@dataclass
class Rankings:
    beatmapsets: Optional[List[Beatmapset]]
    cursor: Cursor
    ranking: List[UserStatistics]
    spotlight: Optional[Spotlight]
    total: int

@dataclass
class BeatmapsetDiscussionPost:
    id: int
    beatmapset_discussion_id: int
    user_id: int
    last_editor_id: int
    deleted_by_id: int
    system: bool
    message: str
    created_at: Datetime
    updated_at: Datetime
    deleted_at: Optional[Datetime]

@dataclass
class BeatmapsetDiscussion:
    id: int
    beatmapset_id: int
    beatmap_id: int
    user_id: int
    deleted_by_id: int
    message_type: MessageType
    parent_id: Optional[int]
    # a point of time which is ``timestamp`` milliseconds into the map
    timestamp: Optional[int]
    resolved: bool
    can_be_resolved: bool
    can_grant_kudosu: bool
    created_at: Datetime
    updated_at: Datetime
    deleted_at: Optional[Datetime]
    last_post_at: Datetime
    kudosu_denied: bool
    starting_post: BeatmapsetDiscussionPost
    # documented as being non-optional but in reality it's not always returned
    posts: Optional[List[BeatmapsetDiscussionPost]]
    beatmap: Optional[BeatmapCompact]
    beatmapset: Optional[BeatmapsetCompact]

@dataclass
class BeatmapsetDiscussionVote:
    score: int
    user_id: int

    # all of the following are documented as being returned, but they never are
    # (for the endpoints we've implemented anyway)
    # beatmapset_discussion_id: int
    # created_at: Datetime
    # id: int
    # updated_at: Datetime


# ===================
# Undocumented Models
# ===================


@dataclass
class BeatmapSearchResult:
    beatmapsets: List[Beatmapset]
    cursor: Cursor
    recommended_difficulty: float
    error: Optional[str]
    total: int


@dataclass
class BeatmapsetDiscussionReview:
    # https://github.com/ppy/osu-web/blob/master/app/Libraries/BeatmapsetDiscussionReview.php
    max_blocks: int

@dataclass
class BeatmapsetEventComment:
    # the values returned by the api for this class depends on
    # `BeatmapsetEvent.type`. Until we have a clean way of dealing with that,
    # mark everything as optional.
    beatmap_discussion_id: Optional[int]
    beatmap_discussion_post_id: Optional[int]
    new_vote: Optional[BeatmapsetDiscussionVote]
    votes: Optional[List[BeatmapsetDiscussionVote]]
    modes: Optional[str]
    # Theese types change based on `BeatmapsetEvent.type`, will need to deal
    # with that as well
    old: Optional[Any]
    new: Optional[Any]
    reason: Optional[str]

@dataclass
class BeatmapsetEvent:
    # https://github.com/ppy/osu-web/blob/master/app/Models/BeatmapsetEvent.php
    # https://github.com/ppy/osu-web/blob/master/app/Transformers/BeatmapsetEventTransformer.php
    id: int
    type: BeatmapsetEventType
    comment: Optional[BeatmapsetEventComment]
    created_at: Optional[Datetime]

    user_id: Optional[int]
    beatmapset: Optional[BeatmapsetCompact]
    discussion: Optional[BeatmapsetDiscussion]


@dataclass
class ModdingHistoryEventsBundle:
    # https://github.com/ppy/osu-web/blob/master/app/Libraries/ModdingHistoryEventsBundle.php#L84
    events: List[BeatmapsetEvent]
    reviewsConfig: BeatmapsetDiscussionReview
    users: List[UserCompact]

@dataclass
class UserRelation:
    # undocumented (and not a class on osu-web)
    # https://github.com/ppy/osu-web/blob/master/app/Transformers/UserRelationTransformer.php#L16
    target_id: int
    relation_type: UserRelationType
    mutual: bool

    # optional fields
    # ---------------
    target: Optional[UserCompact]


@dataclass
class UserStatistics:
    # undocumented
    # https://github.com/ppy/osu-web/blob/master/app/Transformers/UserStatisticsTransformer.php
    level: UserLevel
    global_rank: int
    pp: float
    ranked_score: int
    hit_accuracy: float
    play_count: int
    play_time: int
    total_score: int
    total_hits: int
    maximum_combo: int
    replays_watched_by_others: int
    is_ranked: bool
    grade_counts: UserGradeCounts

    # optional fields
    # ---------------
    country_rank: Optional[int]
    rank: Optional[int]
    user: Optional[UserCompact]
    variants: Optional[Any]

@dataclass
class UserStatisticsRulesets:
    # undocumented
    # https://github.com/ppy/osu-web/blob/master/app/Transformers/UserStatisticsRulesetsTransformer.php
    osu: Optional[UserStatistics]
    taiko: Optional[UserStatistics]
    fruits: Optional[UserStatistics]
    mania: Optional[UserStatistics]
