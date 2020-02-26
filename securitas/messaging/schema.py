from fedora_messaging import message

class MemberSponsorV1(message.Message):
    """The message sent when a user is added to a group by a sponsor"""

    topic = "fas.group.member.sponsor"
    body_schema = {
        "id": "http://fedoraproject.org/message-schema/securtitas",
        "$schema": "http://json-schema.org/draft-04/schema#",
        "description": "The message sent when a user is added to a group by a sponsor",
        "type": "object",
        "required": ["msg"],
        "properties": {
            "msg": {
                "description": "an object",
                "type": "object",
                "properties": {
                    "agent": {"type": "string"},
                }
            }
        },
    }

    def __str__(self):
        """
        Return a complete human-readable representation of the message, which
        in this case is equivalent to the summary.
        """
        return self.summary

    @property
    def summary(self):
        """Return a summary of the message."""
        return f"{self.agent} sponsored {self.user}'s membership in the {self.group} group"
