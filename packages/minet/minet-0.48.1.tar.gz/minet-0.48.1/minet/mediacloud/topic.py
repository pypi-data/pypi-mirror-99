# =============================================================================
# Minet Mediacloud Topic
# =============================================================================
#
# Function related to topics.
#
from minet.utils import request_json
from minet.mediacloud.constants import (
    MEDIACLOUD_API_BASE_URL,
    MEDIACLOUD_DEFAULT_BATCH
)
from minet.mediacloud.utils import get_next_link_id
from minet.mediacloud.formatters import format_topic_story


def url_forge(token=None, topic_id=None, link_id=None, media_id=None,
              from_media_id=None):

    url = '%s/topics/%s/stories/list?key=%s&limit=%i' % (
        MEDIACLOUD_API_BASE_URL,
        topic_id,
        token,
        MEDIACLOUD_DEFAULT_BATCH
    )

    if link_id is not None:
        url += '&link_id=%s' % link_id

    if media_id is not None:
        url += '&media_id=%s' % media_id

    if from_media_id is not None:
        url += '&link_from_media_id=%s' % from_media_id

    return url


def mediacloud_topic_stories(http, token, topic_id, link_id=None, media_id=None,
                             from_media_id=None, format='csv_dict_row'):

    while True:
        url = url_forge(
            token,
            topic_id=topic_id,
            link_id=link_id,
            media_id=media_id,
            from_media_id=from_media_id,
        )

        err, _, data = request_json(http, url)

        if err:
            raise err

        if 'stories' not in data or len(data['stories']) == 0:
            return

        next_link_id = get_next_link_id(data)

        for story in data['stories']:
            if format == 'csv_dict_row':
                yield format_topic_story(story, next_link_id, as_dict=True)
            elif format == 'csv_row':
                yield format_topic_story(story, next_link_id)
            else:
                yield story

        if next_link_id is None:
            return

        link_id = next_link_id
