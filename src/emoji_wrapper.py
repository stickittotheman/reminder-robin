THUMBS_UP = "👍"
THUMBS_DOWN = "👎"


def get_count_for_emoji(msg, emoji_to_count):
    reaction = [r for r in msg.reactions if r.emoji == emoji_to_count]
    return reaction[0].count
