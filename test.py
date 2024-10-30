from database.create import create_tables
from database.models import ChannelsToSub

create_tables()

# test channels
ChannelsToSub.create(tg_id="@test_channel_with_non_private_li")
