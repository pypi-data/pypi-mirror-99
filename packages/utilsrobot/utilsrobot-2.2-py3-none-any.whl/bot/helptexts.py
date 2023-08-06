#================================================================================================================================
welcomehelpp = """

Admin commands:
 - /savewelcome <text>: Set a new welcome message. Supports markdown and fillings.
 - /welcome : See Your Current Welcome Message
 - /clearwelcome : Clears Your Current Welcome Message
"""

filterrhelp = """
Here is the help for the Filters module:

 • /filters: List all active filters saved in the chat.

Admin only:
 • /savefilter <keyword> <reply message>: Add a filter to this chat. The bot will now reply that message whenever 'keyword'is mentioned. If you reply to a sticker with a keyword, the bot will reply with that sticker. NOTE: all filter keywords are in lowercase.

 • /stop <filter keyword>: Stop that filter.

Chat creator only:
 • /removeallfilters: Remove all chat filters at once.
"""

promotehelpp = """
**Here is the help for the Promote Module**

• /promote `<reply to user/userid/username>`
    **Promote the user in the chat.**

• /demote `<reply to user/userid/username>`
    **Demote the user in the chat.**
"""

banhelpp = """
**Here is the help for the Bans Module**

• /ban `<reply to user/userid/username> <reason>`
    **Ban the user from the chat.**

• /unban `<reply to user/userid/username> <reason>`
    **Unban the user from the chat.**
"""

kickhelpp = """
**Here is the help for the Kick Module**

• /kick `<reply to user/userid/username> <reason>`
    **Kick the user from the chat.**
"""

pinhelpp = """
**Here is the help for the Pin/Unpin Module**

• /pin `<reply to message>`
    **Pin the message in the chat**
    **For Loud pin use (`/pin loud`).**

• /unpin `<reply to message>`
    **Unpin the message in the chat**
    **For Unpinning All Messages Use (`/unpin all`).**

"""
purgehelpp = """
**Here is the help for the Purge Module**

• /purge `<reply to message>`
    **Purge all messages from the replied message.**

• /del `<reply to message>`
    **Deletes The Replied Message.**
"""
notesshelp = """
Here is the help for the Notes module:

 • `#<notename>`: To Get The Note
 • /notes : list all saved notes in this chat
 
Admins only:
 • /save <notename> <reply message> :  save the replied message as a note with name notename
 • /clear <notename>: clear note with this name
 
 Chat Creator Only:
 • /removeallnotes: removes all notes from the group
 
 Note: Note names are case-insensitive, and they are automatically converted to lowercase before getting saved.
 """
lockktypes = """
Available message types to lock/unlock are: 
- `all` 
- `msg` 
- `media`
- `sticker`
- `gif`
- `game`
- `inline`
- `poll`
- `invite`
- `pin`
- `info`
"""

lockhelpp = """Here is The Help For Notes Module 

Do stickers annoy you? or want to avoid people sharing links? or pictures? You're in the right place!

The locks module allows you to lock away some common items in the telegram world; the bot will automatically delete them!

Admin commands:
- /lock <item>: Lock one or more items. Now, only admins can use this type!
- /unlock <item>: Unlock one or more items. Everyone can use this type again!
- /locktypes: Show the list of all lockable items."""

fedhelpp = """
 - /newfed <fed_name>: Creates a Federation, one allowed per user.
 - /renamefed <fed_id> <new_fed_name>: Renames the fed id to a new name.
 - /delfed <fed_id>: Delete a Federation, and any information related to it. 
 - /fpromote <user>: Assigns the user as a federation admin. 
 - /fdemote <user>: Drops the user from the federation admin to a normal user.
 - /subfed <fed_id>: Subscribes to a given fed ID, fedbans from that subscribed fed will also happen in your fed
 - /unsubfed <fed_id>: Unsubscribes to a given fed ID
 - /setfedlog <fed_id>: Sets the group as a fed log report base for the federation
 - /unsetfedlog <fed_id>: Removed the group as a fed log report base for the federation
 - /fbroadcast <message>: Broadcasts a messages to all groups that have joined your fed
 - /fedsubs: Shows the feds your group is subscribed to (broken rn)
 - /fban (<user>|<reason>): Fed bans a user. Syntax: `fban 12345 | testing`, `fban @MissJuliaRobot | testing`.
 - /unfban <user> <reason>: Removes a user from a fed ban.
 - /fedinfo <fed_id>: Information about the specified Federation.
 - /joinfed <fed_id>: Join the current chat to the Federation. 
 - /leavefed <fed_id>: Leave the Federation given. 
 - /setfrules <rules>: Arrange Federation rules.
 - /fedadmins: Show Federation admin.
 - /fbanlist: Displays all users who are victimized at the Federation at this time.
 - /fedchats: Get all the chats that are connected in the Federation.
 - /chatfed : See the Federation in the current chat.
 - /fbanstat: Shows if you/or the user you are replying to or their username/id is fbanned somewhere or not.
 - /fednotif <on/off>: Should the bot send notifications for fban/unfban in PM.
 - /frules: See the current federation rules.
 - /exportfbans: Returns a list of all banned users in the current federation.
 - /importfbans: Imports all fbanned uses from the export file into the current chat federation.
**NOTE**: Federation ban doesn't ban the user from the fed chats instead kicks everytime they join the chat.
"""
#==========================================================================
