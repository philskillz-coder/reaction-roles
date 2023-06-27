from __future__ import annotations

import asyncio
from typing import TYPE_CHECKING

from discord import ui

from imp.emoji import Emojis

if TYPE_CHECKING:
    from imp.better.interaction import BetterInteraction


# class PollOptionButton(ui.Button):
#     def __init__(self, option: PollOption, label: str, emoji: str, custom_id: str, row: int):
#         super().__init__(
#             label=label,
#             emoji=emoji,
#             custom_id=custom_id,
#             row=row
#         )
#         self.option = option
#
#     async def callback(self, interaction: BetterInteraction):
#         async with interaction.client.pool.acquire() as cursor:
#             if await self.option.poll.user_voted(
#                     cursor,
#                     user=interaction.user.id
#             ):
#                 return await interaction.response.send_message(
#                     content=await self.option.poll.client.translator.translate(
#                         cursor,
#                         guild_rid=await self.option.poll.guild_rid(cursor),
#                         key="poll.already_voted"
#                     ),
#                     ephemeral=True
#                 )
#
#             await interaction.response.send_message(
#                 content=await self.option.poll.client.translator.translate(
#                     cursor,
#                     guild_rid=await self.option.poll.guild_rid(cursor),
#                     key="poll.voted",
#                     option=await self.option.name(cursor)
#                 ),
#                 ephemeral=True
#             )
#
#             await self.option.poll.add_vote(
#                 cursor,
#                 PollVote(interaction.user.id, self.option.poll.rid, self.option.rid)
#             )
#             await asyncio.sleep(self.option.poll.POLL_UPDATE_TIME)
#             if self.option.poll.update_ready():
#                 await self.option.poll.update(cursor)
#
#
# class PollView(ui.View):
#     def __init__(self, poll: Poll):
#         super().__init__(timeout=None)
#         self.poll = poll
#         self._option_count = 0
#
#     async def add_options(self, cursor: Connection):
#         options = await self.poll.options(cursor)
#         self._option_count = len(options)
#         for i, option in enumerate(options):
#             self.add_item(
#                 PollOptionButton(
#                     option,
#                     label=await option.name(cursor),
#                     emoji=Emojis.emojis[i],
#                     custom_id=f"poll:{self.poll.hid}:option:{option.hid}",
#                     row=i//4
#                 )
#             )
#
#         return self
#
#     # async def add_stop(self):
#     #     self.add_item(PollStopButton(self.poll, f"poll:{self.poll.hid}:stop", row=self._option_count//4+1))
#
#     # async def add_start(self):
#     #     self.add_item(PollStartButton(self.poll, f"poll:{self.poll.hid}:start", row=self._option_count//4+1))
#
#     async def press_start(self, cursor: Connection):
#         self.clear_items()
#         await self.add_options(cursor)
#         # await self.add_stop()
#
#     async def press_stop(self):
#         self.clear_items()
#         self.stop()
#
#     async def run(self, cursor: Connection):
#         started = await self.poll.started(
#             cursor,
#         )
#
#         if started:
#             await self.add_options(cursor)
#             # await self.add_stop()
#
#         # else:
#         #     await self.add_start()
#
#         return self
