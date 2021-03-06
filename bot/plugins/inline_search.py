#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
#  GetSongsBot
#  Copyright (C) 2021 The Authors

#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Affero General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.

#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Affero General Public License for more details.

#  You should have received a copy of the GNU Affero General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.


from telethon import events
from telethon.errors import (
    QueryIdInvalidError
)
from bot import (
    BOT,
    SPT_NTOIQ_TEXT,
    SPT_SRCHTGSBR_TEXT,
    SPT_YSEQI_TEXT,
    TG_INLINE_SRCH_CACHE_TIME,
    TG_INLINE_SRCH_NUM_RESULTS
)
from bot.helpers.imdb_bot_srch import (
    search_imdb_in_line
)


@BOT.on(
    events.InlineQuery
)
async def handler(event: events.InlineQuery.Event):
    start_at = int(event.query.offset or 0)
    limit = TG_INLINE_SRCH_NUM_RESULTS
    new_offset = str(start_at + limit)
    search_query = event.query.query
    search_results = []
    switch_pm_text_s = ""
    cache_time = TG_INLINE_SRCH_CACHE_TIME
    if search_query.strip() != "":
        search_results, rtbt = await search_imdb_in_line(
            event.client,
            event,
            search_query,
            start_at,
            limit
        )
        len_srch_ress = len(search_results)
        switch_pm_text_s = SPT_YSEQI_TEXT.format(
            len_srch_ress=str(len_srch_ress),
            rtbt=str(rtbt),
            search_query=str(search_query)
        )
    else:
        switch_pm_text_s = SPT_NTOIQ_TEXT
    new_offset = None
    try:
        await event.answer(
            results=search_results,
            cache_time=cache_time,
            gallery=False,
            next_offset=new_offset,
            private=False,
            switch_pm=switch_pm_text_s,
            switch_pm_param="inline",
        )
    except QueryIdInvalidError:
        await event.answer(
            results=[],
            cache_time=cache_time,
            gallery=False,
            next_offset=None,
            private=False,
            switch_pm=SPT_SRCHTGSBR_TEXT,
            switch_pm_param="toolongxtion",
        )
