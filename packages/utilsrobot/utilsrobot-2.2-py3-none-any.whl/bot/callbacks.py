from bot.utilsbot import callback
from bot.helptexts import (
    welcomehelpp,
    filterrhelp,
    promotehelpp,
    banhelpp,
    kickhelpp,
    pinhelpp,
    purgehelpp,
    notesshelp,
    lockktypes,
    lockhelpp,
    fedhelpp,
)
from telethon import events, functions, Button
import bot.utilsbot

@callback("banhelp")
async def _(event):
    await event.edit(f"{banhelpp}",buttons=[Button.inline(" <-- Back", data="helpstarter")])

@callback("promotehelp")
async def _(event):
    await event.edit(f"{promotehelpp}",buttons=[Button.inline(" <-- Back", data="helpstarter")])

@callback("kickhelp")
async def _(event):
    await event.edit(f"{kickhelpp}",buttons=[Button.inline(" <-- Back", data="helpstarter")])

@callback("pinhelp")
async def _(event):
    await event.edit(f"{pinhelpp}",buttons=[Button.inline(" <-- Back", data="helpstarter")])

@callback("purgehelp")
async def _(event):
    await event.edit(f"{purgehelpp}",buttons=[Button.inline(" <-- Back", data="helpstarter")])

@callback("lockhelp")
async def _(event):
    await event.edit(f"{lockhelpp}",buttons=[Button.inline(" <-- Back", data="helpstarter")])

@callback("filterhelp")
async def _(event):
    await event.edit(f"{filterrhelp}",buttons=[Button.inline(" <-- Back", data="helpstarter")])

@callback("noteshelp")
async def _(event):
    await event.edit(f"{notesshelp}",buttons=[Button.inline(" <-- Back", data="helpstarter")])

@callback("welcomehelp")
async def _(event):
    await event.edit(f"{welcomehelpp}",buttons=[Button.inline(" <-- Back", data="helpstarter")])

@callback("fedhelp")
async def _(event):
    await event.edit(f"{fedhelpp}",buttons=[Button.inline(" <-- Back", data="helpstarter")])
