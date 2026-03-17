import pytest
from pydantic import ValidationError

from app.schemas import Vote


def test_vote_accepts_allowed_dir_values():
    upvote = Vote(post_id=1, dir=1)
    remove_vote = Vote(post_id=1, dir=0)

    assert upvote.dir == 1
    assert remove_vote.dir == 0


@pytest.mark.parametrize("value", [-1, 2, 999])
def test_vote_rejects_invalid_dir_values(value):
    with pytest.raises(ValidationError):
        Vote(post_id=1, dir=value)
