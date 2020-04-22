# Copyright (C) 2020 by UsergeTeam@Github, < https://github.com/UsergeTeam >.
#
# This file is part of < https://github.com/UsergeTeam/Userge > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/uaudith/Userge/blob/master/LICENSE >
#
# All rights reserved.

import time
from userge import userge, Message
from pyrogram import ChatPermissions
from pyrogram.errors import (FloodWait,
UserAdminInvalid,
UsernameInvalid,
ChatAdminRequired,
PeerIdInvalid,
UserIdInvalid)

CHANNEL = userge.getCLogger(__name__)

async def is_admin(message: Message):
    check_user = await userge.get_chat_member(message.chat.id, message.from_user.id)
    user_type = check_user.status

    if user_type == "member":
        return False

    elif user_type == "administrator":
        rm_perm = check_user.can_restrict_members

        if rm_perm:
            return True
        else:
            return False

    else:
        return True

async def is_sudoadmin(message: Message):
    check_user = await userge.get_chat_member(message.chat.id, message.from_user.id)
    user_type = check_user.status

    if user_type == "member":
        return False

    elif user_type == "administrator":
        add_adminperm = check_user.can_promote_members

        if add_adminperm:
            return True
        else:
            return False

    else:
        return True


@userge.on_cmd("promote", about="""\
__use this to promote group members__

**Usage:**

`Provides admin rights to the person in the supergroup.`

[NOTE: Requires proper admin rights in the chat!!!]


**Example:**

    `.promote [username | userid] or [reply to user]`""")

async def promote_usr(message: Message):
    """
    this function can promote members in tg group
    """
    chat_id = message.chat.id
    get_group = await userge.get_chat(chat_id)
    can_promo = await is_sudoadmin(message)

    await message.edit("`Trying to Promote User.. Hang on!`")

    if can_promo:

        user_id = message.input_str

        if user_id:

            try:
                get_mem = await userge.get_chat_member(chat_id, user_id)
                await userge.promote_chat_member(chat_id, user_id,
                                                 can_change_info=True,
                                                 can_delete_messages=True,
                                                 can_restrict_members=True,
                                                 can_invite_users=True,
                                                 can_pin_messages=True)

                await message.edit("**👑 Promoted Successfully**", del_in=0)

                await CHANNEL.log(
                    f"#PROMOTE\n\n"
                    f"USER: [{get_mem.user.first_name}](tg://user?id={get_mem.user.id}) "
                    f"(`{get_mem.user.id}`)\n"
                    f"CHAT: `{get_group.title}` (`{chat_id}`)")

            except UsernameInvalid:
                await message.edit(
                    text="`invalid username or userid, try again with valid info ⚠`", del_in=0
                    )
                return

            except PeerIdInvalid:
                await message.edit(
                    text="`invalid username or userid, try again with valid info ⚠`", del_in=0
                    )
                return

            except UserIdInvalid:
                await message.edit(
                    text="`invalid username or userid, try again with valid info ⚠`", del_in=0
                    )
                return

            except ChatAdminRequired:
                await message.edit(
                    text=r"`i don't have permission to do that` ＞︿＜", del_in=0
                    )
                return

            except Exception as e:
                await message.edit(
                    text="something went wrong! 🤔\n"
                    f"**ERROR:** `{e}`"
                )
                return

        elif message.reply_to_message:

            try:
                get_mem = await userge.get_chat_member(
                    chat_id,
                    message.reply_to_message.from_user.id
                    )
                await userge.promote_chat_member(chat_id, get_mem.user.id,
                                                 can_change_info=True,
                                                 can_delete_messages=True,
                                                 can_restrict_members=True,
                                                 can_invite_users=True,
                                                 can_pin_messages=True)

                await message.edit("**👑 Promoted Successfully**", del_in=0)

                await CHANNEL.log(
                    f"#PROMOTE\n\n"
                    f"USER: [{get_mem.user.first_name}](tg://user?id={get_mem.user.id}) "
                    f"(`{get_mem.user.id}`)\n"
                    f"CHAT: `{get_group.title}` (`{chat_id}`)")

            except ChatAdminRequired:
                await message.edit(
                    text=r"`i don't have permission to do that` ＞︿＜", del_in=0
                    )
                return

            except Exception as e:
                await message.edit(
                    text="`something went wrong 🤔,`\n"
                    f"**ERROR:** `{e}`", del_in=0)
                return

        else:
            await message.edit(
                text="`no valid user_id or message specified,`"
                "`do .help promote for more info` ⚠", del_in=0)

            return

    else:
        await message.edit(
            text=r"`i don't have proper permission to do that! ¯\_(ツ)_/¯`", del_in=0)


@userge.on_cmd("demote", about="""\
__use this to demote group members__

**Usage:**

`Remove admin rights from admin in the supergroup.`

[NOTE: Requires proper admin rights in the chat!!!]


**Example:**

    `.demote [username | userid] or [reply to user]`""")

async def demote_usr(message: Message):
    """
    this function can demote members in tg group
    """
    chat_id = message.chat.id
    get_group = await userge.get_chat(chat_id)
    can_demote = await is_sudoadmin(message)

    await message.edit("`Trying to Demote User.. Hang on!`")

    if can_demote:

        user_id = message.input_str

        if user_id:

            try:
                get_mem = await userge.get_chat_member(chat_id, user_id)
                await userge.promote_chat_member(chat_id, user_id,
                                                 can_change_info=False,
                                                 can_delete_messages=False,
                                                 can_restrict_members=False,
                                                 can_invite_users=False,
                                                 can_pin_messages=False)

                await message.edit("**🛡 Demoted Successfully**", del_in=0)
                await CHANNEL.log(
                    f"#DEMOTE\n\n"
                    f"USER: [{get_mem.user.first_name}](tg://user?id={get_mem.user.id}) "
                    f"(`{get_mem.user.id}`)\n"
                    f"CHAT: `{get_group.title}` (`{chat_id}`)")

            except UsernameInvalid:
                await message.edit(
                    text="`invalid username or userid, try again with valid info ⚠`", del_in=0
                    )
                return

            except PeerIdInvalid:
                await message.edit(
                    text="`invalid username or userid, try again with valid info ⚠`", del_in=0
                    )
                return

            except UserIdInvalid:
                await message.edit(
                    text="`invalid username or userid, try again with valid info ⚠`", del_in=0
                    )
                return

            except ChatAdminRequired:
                await message.edit(
                    text=r"`i don't have permission to do that` ＞︿＜", del_in=0
                    )
                return

            except Exception as e:
                await message.edit(
                    text="something went wrong! 🤔\n"
                    f"**ERROR:** `{e}`", del_in=0
                )
                return

        elif message.reply_to_message:

            try:
                get_mem = await userge.get_chat_member(
                    chat_id,
                    message.reply_to_message.from_user.id
                    )
                await userge.promote_chat_member(chat_id, get_mem.user.id,
                                                 can_change_info=False,
                                                 can_delete_messages=False,
                                                 can_restrict_members=False,
                                                 can_invite_users=False,
                                                 can_pin_messages=False)

                await message.edit("**🛡 Demoted Successfully**", del_in=0)
                await CHANNEL.log(
                    f"#DEMOTE\n\n"
                    f"USER: [{get_mem.user.first_name}](tg://user?id={get_mem.user.id}) "
                    f"(`{get_mem.user.id}`)\n"
                    f"CHAT: `{get_group.title}` (`{chat_id}`)")

            except ChatAdminRequired:
                await message.edit(
                    text=r"`i don't have permission to do that` ＞︿＜", del_in=0
                    )
                return

            except Exception as e:
                await message.edit(
                    text="something went wrong! 🤔\n"
                    f"**ERROR:** `{e}`", del_in=0
                )
                return

        else:
            await message.edit(
                text="`no valid user_id or message specified,`"
                "`do .help demote for more info` ⚠", del_in=0)

            return

    else:
        await message.edit(
            text=r"`i don't have proper permission to do that! ¯\_(ツ)_/¯`", del_in=0)

@userge.on_cmd("ban", about="""\
__use this to ban group members__

**Usage:**

`Ban member from supergroup.`

[NOTE: Requires proper admin rights in the chat!!!]


**Example:**

    `.ban [username | userid] or [reply to user] :reason (optional)`""")

async def ban_usr(message: Message):
    """
    this function can ban user from tg group
    """
    reason = ""
    chat_id = message.chat.id
    get_group = await userge.get_chat(chat_id)
    can_ban = await is_admin(message)

    if can_ban:

        if message.reply_to_message:
            user_id = message.reply_to_message.from_user.id
            reason = message.input_str
        else:
            args = message.input_str.split(maxsplit=1)
            if len(args) == 2:
                user_id, reason = args
            elif len(args) == 1:
                user_id = args[0]
            else:
                await message.edit(
                    text="`no valid user_id or message specified,`"
                    "`do .help ban for more info` ⚠", del_in=0)
                return

        if user_id:

            try:
                get_mem = await userge.get_chat_member(chat_id, user_id)
                await userge.kick_chat_member(chat_id, user_id)
                await message.edit(
                    f"#BAN\n\n"
                    f"USER: [{get_mem.user.first_name}](tg://user?id={get_mem.user.id}) "
                    f"(`{get_mem.user.id}`)\n"
                    f"CHAT: `{get_group.title}` (`{chat_id}`)\n"
                    f"REASON: `{reason}`", log=True)

            except UsernameInvalid:
                await message.edit(
                    text="`invalid username or userid, try again with valid info ⚠`", del_in=0
                    )
                return

            except PeerIdInvalid:
                await message.edit(
                    text="`invalid username or userid, try again with valid info ⚠`", del_in=0
                    )
                return

            except UserIdInvalid:
                await message.edit(
                    text="`invalid username or userid, try again with valid info ⚠`", del_in=0
                    )
                return

            except ChatAdminRequired:
                await message.edit(
                    text=r"`i don't have permission to do that` ＞︿＜", del_in=0
                    )
                return

            except Exception as e:
                await message.edit(
                    text="something went wrong! 🤔\n"
                    f"**ERROR:** `{e}`", del_in=0
                )
                return

    else:
        await message.edit(
            text=r"`i don't have proper permission to do that! ¯\_(ツ)_/¯`", del_in=0)

@userge.on_cmd("unban", about="""\
__use this to unban group members__

**Usage:**

`Unban member from supergroup.`

[NOTE: Requires proper admin rights in the chat!!!]


**Example:**

    `.unban [username | userid] or [reply to user]`""")

async def unban_usr(message: Message):
    """
    this function can unban user from tg group
    """
    chat_id = message.chat.id
    get_group = await userge.get_chat(chat_id)
    can_unban = await is_admin(message)

    if can_unban:

        user_id = message.input_str

        if user_id:

            try:
                get_mem = await userge.get_chat_member(chat_id, user_id)
                await userge.unban_chat_member(chat_id, user_id)
                await message.edit("**🛡 Successfully Unbanned**", del_in=0)
                await CHANNEL.log(
                    f"#UNBAN\n\n"
                    f"USER: [{get_mem.user.first_name}](tg://user?id={get_mem.user.id}) "
                    f"(`{get_mem.user.id}`)\n"
                    f"CHAT: `{get_group.title}` (`{chat_id}`)")

            except UsernameInvalid:
                await message.edit(
                    text="`invalid username or userid, try again with valid info ⚠`", del_in=0
                    )
                return

            except PeerIdInvalid:
                await message.edit(
                    text="`invalid username or userid, try again with valid info ⚠`", del_in=0
                    )
                return

            except UserIdInvalid:
                await message.edit(
                    text="`invalid username or userid, try again with valid info ⚠`", del_in=0
                    )
                return

            except Exception as e:
                await message.edit(
                    text="something went wrong! 🤔\n"
                    f"**ERROR:** `{e}`", del_in=0
                )
                return

        elif message.reply_to_message:

            try:
                get_mem = await userge.get_chat_member(
                    chat_id,
                    message.reply_to_message.from_user.id
                    )
                await userge.unban_chat_member(chat_id, get_mem.user.id)
                await message.edit("**🛡 Successfully Unbanned**", del_in=0)
                await CHANNEL.log(
                    f"#UNBAN\n\n"
                    f"USER: [{get_mem.user.first_name}](tg://user?id={get_mem.user.id}) "
                    f"(`{get_mem.user.id}`)\n"
                    f"CHAT: `{get_group.title}` (`{chat_id}`)")

            except Exception as e:
                await message.edit(
                    text="`something went wrong 🤔,`"
                    f"**ERROR:** `{e}`", del_in=0
                    )
                return

        else:
            await message.edit(
                text="`no valid user_id or message specified,`"
                "`do .help unban for more info` ⚠", del_in=0)

            return

    else:
        await message.edit(
            text=r"`i don't have proper permission to do that! ¯\_(ツ)_/¯`", del_in=0)

@userge.on_cmd("kick", about="""\
__use this to kick group members__

**Usage:**

`Kick member from supergroup. member can rejoin the group again if they want.`

[NOTE: Requires proper admin rights in the chat!!!]


**Example:**

    `.kick [username | userid] or [reply to user]""")

async def kick_usr(message: Message):
    """
    this function can kick user from tg group
    """
    chat_id = message.chat.id
    get_group = await userge.get_chat(chat_id)
    can_kick = await is_admin(message)

    if can_kick:

        user_id = message.input_str

        if user_id:

            try:
                get_mem = await userge.get_chat_member(chat_id, user_id)
                await userge.kick_chat_member(chat_id, user_id, int(time.time() + 45))
                await message.edit(
                    f"#KICK\n\n"
                    f"USER: [{get_mem.user.first_name}](tg://user?id={get_mem.user.id}) "
                    f"(`{get_mem.user.id}`)\n"
                    f"CHAT: `{get_group.title}` (`{chat_id}`)", log=True)

            except UsernameInvalid:
                await message.edit(
                    text="`invalid username or userid, try again with valid info ⚠`", del_in=0
                    )
                return

            except PeerIdInvalid:
                await message.edit(
                    text="`invalid username or userid, try again with valid info ⚠`", del_in=0
                    )
                return

            except UserIdInvalid:
                await message.edit(
                    text="`invalid username or userid, try again with valid info ⚠`", del_in=0
                    )
                return

            except ChatAdminRequired:
                await message.edit(
                    text=r"`i don't have permission to do that` ＞︿＜", del_in=0
                    )
                return

            except Exception as e:
                await message.edit(
                    text="something went wrong! 🤔\n"
                    f"**ERROR:** `{e}`", del_in=0
                )
                return

        elif message.reply_to_message:

            try:
                get_mem = await userge.get_chat_member(
                    chat_id,
                    message.reply_to_message.from_user.id
                    )
                await userge.kick_chat_member(chat_id, get_mem.user.id, int(time.time() + 45))
                await message.edit(
                    f"#KICK\n\n"
                    f"USER: [{get_mem.user.first_name}](tg://user?id={get_mem.user.id}) "
                    f"(`{get_mem.user.id}`)\n"
                    f"CHAT: `{get_group.title}` (`{chat_id}`)", log=True)

            except ChatAdminRequired:
                await message.edit(
                    text=r"`i don't have permission to do that` ＞︿＜", del_in=0
                    )
                return

            except Exception as e:
                await message.edit(
                    text="something went wrong! 🤔\n"
                    f"**ERROR:** `{e}`", del_in=0
                )
                return

        else:
            await message.edit(
                text="`no valid user_id or message specified,`"
                "`do .help kick for more info` ⚠", del_in=0)

            return

    else:
        await message.edit(
            text=r"`i don't have proper permission to do that! ¯\_(ツ)_/¯`", del_in=0)

@userge.on_cmd("mute", about="""\
__use this to mute group members__

**Usage:**

`Mute member in the supergroup. you can only use one flag for command`

[NOTE: Requires proper admin rights in the chat!!!]

**Available Flags:**
`-m` : __minutes__
`-h` : __hours__
`-d` : __days__


**Example:**

    `.mute -flag [username | userid] or [reply to user] :reason (optional)`
    `.mute -d1 @someusername/userid/replytouser SPAM` (mute for one day:reason SPAM)""")

async def mute_usr(message: Message):
    """
    this function can mute user from tg group
    """
    reason = ""
    chat_id = message.chat.id
    flags = message.flags
    get_group = await userge.get_chat(chat_id)
    can_mute = await is_admin(message)

    minutes = int(flags.get('-m', 0))
    hours = int(flags.get('-h', 0))
    days = int(flags.get('-d', 0))

    await message.edit("`Trying to Mute User.. Hang on!`")

    if can_mute:

        if message.reply_to_message:
            user_id = message.reply_to_message.from_user.id
            reason = message.filtered_input_str
        else:
            args = message.filtered_input_str.split(maxsplit=1)
            if len(args) == 2:
                user_id, reason = args
            elif len(args) == 1:
                user_id = args[0]
            else:
                await message.edit(
                    text="`no valid user_id or message specified,`"
                    "`do .help mute for more info`", del_in=0)
                return

        if minutes:

            try:
                get_mem = await userge.get_chat_member(chat_id, user_id)
                mute_period = minutes * 60
                await userge.restrict_chat_member(chat_id, user_id,
                                                  ChatPermissions(),
                                                  int(time.time() + mute_period))
                await message.edit(
                    f"#MUTE\n\n"
                    f"USER: [{get_mem.user.first_name}](tg://user?id={get_mem.user.id}) "
                    f"(`{get_mem.user.id}`)\n"
                    f"CHAT: `{get_group.title}` (`{chat_id}`)\n"
                    f"MUTE UNTIL: `{minutes} minutes`\n"
                    f"REASON: `{reason}`", log=True)

            except UsernameInvalid:
                await message.edit(
                    text="`invalid username or userid, try again with valid info ⚠`", del_in=0
                    )
                return

            except PeerIdInvalid:
                await message.edit(
                    text="`invalid username or userid, try again with valid info ⚠`", del_in=0
                    )
                return

            except UserIdInvalid:
                await message.edit(
                    text="`invalid username or userid, try again with valid info ⚠`", del_in=0
                    )
                return

            except ChatAdminRequired:
                await message.edit(
                    text=r"`i don't have permission to do that` ＞︿＜", del_in=0
                    )
                return

            except Exception as e:
                await message.edit(
                    text=f"`something went wrong 🤔,`"
                    f"`do .help mute for more info`\n"
                    f"**ERROR**: {e}", del_in=0)
                return

        elif hours:

            try:
                get_mem = await userge.get_chat_member(chat_id, user_id)
                mute_period = hours * 3600
                await userge.restrict_chat_member(chat_id, user_id,
                                                  ChatPermissions(),
                                                  int(time.time() + mute_period))
                await message.edit(
                    f"#MUTE\n\n"
                    f"USER: [{get_mem.user.first_name}](tg://user?id={get_mem.user.id}) "
                    f"(`{get_mem.user.id}`)\n"
                    f"CHAT: `{get_group.title}` (`{chat_id}`)\n"
                    f"MUTE UNTIL: `{hours} hours`\n"
                    f"REASON: `{reason}`", log=True)

            except UsernameInvalid:
                await message.edit(
                    text="`invalid username or userid, try again with valid info ⚠`", del_in=0
                    )
                return

            except PeerIdInvalid:
                await message.edit(
                    text="`invalid username or userid, try again with valid info ⚠`", del_in=0
                    )
                return

            except UserIdInvalid:
                await message.edit(
                    text="`invalid username or userid, try again with valid info ⚠`", del_in=0
                    )
                return

            except ChatAdminRequired:
                await message.edit(
                    text=r"`i don't have permission to do that` ＞︿＜", del_in=0
                    )
                return

            except Exception as e:
                await message.edit(
                    text=f"`something went wrong 🤔,`"
                    f"`do .help mute for more info`\n"
                    f"**ERROR**: {e}", del_in=0)
                return

        elif days:

            try:
                get_mem = await userge.get_chat_member(chat_id, user_id)
                mute_period = hours * 86400
                await userge.restrict_chat_member(chat_id, user_id,
                                                  ChatPermissions(),
                                                  int(time.time() + mute_period))
                await message.edit(
                    f"#MUTE\n\n"
                    f"USER: [{get_mem.user.first_name}](tg://user?id={get_mem.user.id}) "
                    f"(`{get_mem.user.id}`)\n"
                    f"CHAT: `{get_group.title}` (`{chat_id}`)\n"
                    f"MUTE UNTIL: `{days} days`\n"
                    f"REASON: `{reason}`", log=True)

            except UsernameInvalid:
                await message.edit(
                    text="`invalid username or userid, try again with valid info ⚠`", del_in=0
                    )
                return

            except PeerIdInvalid:
                await message.edit(
                    text="`invalid username or userid, try again with valid info ⚠`", del_in=0
                    )
                return

            except UserIdInvalid:
                await message.edit(
                    text="`invalid username or userid, try again with valid info ⚠`", del_in=0
                    )
                return

            except ChatAdminRequired:
                await message.edit(
                    text=r"`i don't have permission to do that` ＞︿＜", del_in=0
                    )
                return

            except Exception as e:
                await message.edit(
                    text=f"`something went wrong 🤔,`"
                    f"`do .help mute for more info`\n"
                    f"**ERROR**: {e}", del_in=0)
                return

        else:

            try:
                get_mem = await userge.get_chat_member(chat_id, user_id)
                await userge.restrict_chat_member(chat_id, user_id, ChatPermissions())
                await message.edit(
                    f"#MUTE\n\n"
                    f"USER: [{get_mem.user.first_name}](tg://user?id={get_mem.user.id}) "
                    f"(`{get_mem.user.id}`)\n"
                    f"CHAT: `{get_group.title}` (`{chat_id}`)\n"
                    f"MUTE UNTIL: `forever`\n"
                    f"REASON: `{reason}`", log=True)

            except UsernameInvalid:
                await message.edit(
                    text="`invalid username or userid, try again with valid info ⚠`", del_in=0
                    )
                return

            except PeerIdInvalid:
                await message.edit(
                    text="`invalid username or userid, try again with valid info ⚠`", del_in=0
                    )
                return

            except UserIdInvalid:
                await message.edit(
                    text="`invalid username or userid, try again with valid info ⚠`", del_in=0
                    )
                return

            except ChatAdminRequired:
                await message.edit(
                    text=r"`i don't have permission to do that` ＞︿＜", del_in=0
                    )
                return

            except Exception as e:
                await message.edit(
                    text=f"`something went wrong 🤔,`"
                    f"`do .help mute for more info`\n"
                    f"**ERROR**: {e}", del_in=0)

                return

    else:
        await message.edit(
            text=r"`i don't have proper permission to do that! ¯\_(ツ)_/¯`", del_in=0)

@userge.on_cmd("unmute", about="""\
__use this to unmute group members__

**Usage:**

`Unmute member from supergroup.`

[NOTE: Requires proper admin rights in the chat!!!]


**Example:**

    `.unmute [username | userid]  or [reply to user]`""")

async def unmute_usr(message: Message):
    """
    this function can unmute user from tg group
    """
    chat_id = message.chat.id
    get_group = await userge.get_chat(chat_id)
    can_unmute = await is_admin(message)

    amsg = get_group.permissions.can_send_messages
    amedia = get_group.permissions.can_send_media_messages
    astickers = get_group.permissions.can_send_stickers
    aanimations = get_group.permissions.can_send_animations
    agames = get_group.permissions.can_send_games
    ainlinebots = get_group.permissions.can_use_inline_bots
    awebprev = get_group.permissions.can_add_web_page_previews
    apolls = get_group.permissions.can_send_polls
    ainfo = get_group.permissions.can_change_info
    ainvite = get_group.permissions.can_invite_users
    apin = get_group.permissions.can_pin_messages

    if can_unmute:

        user_id = message.input_str

        if user_id:

            try:
                get_mem = await userge.get_chat_member(chat_id, user_id)
                await userge.restrict_chat_member(chat_id, user_id,
                                                  ChatPermissions(
                                                      can_send_messages=amsg,
                                                      can_send_media_messages=amedia,
                                                      can_send_stickers=astickers,
                                                      can_send_animations=aanimations,
                                                      can_send_games=agames,
                                                      can_use_inline_bots=ainlinebots,
                                                      can_add_web_page_previews=awebprev,
                                                      can_send_polls=apolls,
                                                      can_change_info=ainfo,
                                                      can_invite_users=ainvite,
                                                      can_pin_messages=apin))

                await message.edit("**🛡 Successfully Unmuted**", del_in=0)
                await CHANNEL.log(
                    f"#UNMUTE\n\n"
                    f"USER: [{get_mem.user.first_name}](tg://user?id={get_mem.user.id}) "
                    f"(`{get_mem.user.id}`)\n"
                    f"CHAT: `{get_group.title}` (`{chat_id}`)")

            except UsernameInvalid:
                await message.edit(
                    text="`something went wrong 🤔,`"
                    "`do .help unmute for more info`", del_in=0)

            except PeerIdInvalid:
                await message.edit(
                    text="`invalid username or userid, try again with valid info ⚠`", del_in=0
                    )
                return

            except UserIdInvalid:
                await message.edit(
                    text="`invalid username or userid, try again with valid info ⚠`", del_in=0
                    )
                return

            except Exception as e:
                await message.edit(
                    text="something went wrong! 🤔\n"
                    f"**ERROR:** `{e}`", del_in=0
                )
                return

        elif message.reply_to_message:

            try:
                get_mem = await userge.get_chat_member(
                    chat_id,
                    message.reply_to_message.from_user.id
                    )
                await userge.restrict_chat_member(chat_id, get_mem.user.id,
                                                  ChatPermissions(
                                                      can_send_messages=amsg,
                                                      can_send_media_messages=amedia,
                                                      can_send_stickers=astickers,
                                                      can_send_animations=aanimations,
                                                      can_send_games=agames,
                                                      can_use_inline_bots=ainlinebots,
                                                      can_add_web_page_previews=awebprev,
                                                      can_send_polls=apolls,
                                                      can_change_info=ainfo,
                                                      can_invite_users=ainvite,
                                                      can_pin_messages=apin))

                await message.edit("**🛡 Successfully Unmuted**", del_in=0)
                await CHANNEL.log(
                    f"#UNMUTE\n\n"
                    f"USER: [{get_mem.user.first_name}](tg://user?id={get_mem.user.id}) "
                    f"(`{get_mem.user.id}`)\n"
                    f"CHAT: `{get_group.title}` (`{chat_id}`)")

            except Exception as e:
                await message.edit(
                    text="something went wrong! 🤔\n"
                    f"**ERROR:** `{e}`", del_in=0
                )
                return

        else:
            await message.edit(
                text="`no valid user_id or message specified,`"
                "`do .help unmute for more info`", del_in=0)

            return

    else:
        await message.edit(
            text=r"`i don't have proper permission to do that! ¯\_(ツ)_/¯`", del_in=0)

@userge.on_cmd("zombies", about="""\
__use this to clean zombie accounts__

**Usage:**

`check & remove zombie (deleted) accounts from supergroup.`

[NOTE: Requires proper admin rights in the chat!!!]

**Available Flags:**

`-c` : __clean__

**Example:**

    `.zombies [check deleted accounts in group]`
    `.zombies -c [remove deleted accounts from group]`""")

async def zombie_clean(message: Message):
    """
    this function can remove deleted accounts from tg group
    """
    chat_id = message.chat.id
    get_group = await userge.get_chat(chat_id)
    flags = message.flags

    rm_delaccs = '-c' in flags

    can_clean = await is_admin(message)

    if rm_delaccs:

        del_users = 0
        del_admins = 0
        del_total = 0
        del_stats = r"`Zero zombie accounts found in this chat... WOOHOO group is clean.. \^o^/`"

        if can_clean:

            await message.edit("`Hang on!! cleaning zombie accounts from this chat..`")
            async for member in userge.iter_chat_members(chat_id):

                if member.user.is_deleted:

                    try:
                        await userge.kick_chat_member(
                            chat_id,
                            member.user.id, int(time.time() + 45))

                    except UserAdminInvalid:
                        del_users -= 1
                        del_admins += 1

                    except FloodWait as e:
                        time.sleep(e.x)
                    del_users += 1
                    del_total += 1

            if del_admins > 0:
                del_stats = f"**Found** `{del_total}` total zombies..👻\
                \n🗑 **Cleaned** `{del_users}` **zombie (deleted) accounts from this chat**\
                \n🛡 `{del_admins}` **deleted admin accounts are skipped**"

            else:
                del_stats = f"**Found** `{del_total}` total zombies..👻\
                \n🗑 **Cleaned** `{del_users}` **zombie (deleted) accounts from this chat**"

            await message.edit(f"🗑 {del_stats}", del_in=0)
            await CHANNEL.log(
                f"#ZOMBIE_CLEAN\n\n"
                f"CHAT: `{get_group.title}` (`{chat_id}`)\n"
                f"TOTAL ZOMBIE COUNT: `{del_total}`\n"
                f"CLEANED ZOMBIE COUNT: `{del_users}`\n"
                f"ZOMBIE ADMIN COUNT: `{del_admins}`"
            )

        else:
            await message.edit(r"`i don't have proper permission to do that! ¯\_(ツ)_/¯`", del_in=0)

    else:

        del_users = 0
        del_stats = r"`Zero zombie accounts found in this chat... WOOHOO group is clean.. \^o^/`"
        await message.edit("`🔎 Searching for zombie accounts in this chat..`")
        async for member in userge.iter_chat_members(chat_id):

            if member.user.is_deleted:
                del_users += 1

        if del_users > 0:

            del_stats = f"**Found** `{del_users}` **zombie accounts in this chat.**"
            await message.edit(
                f"🕵️‍♂️ {del_stats} "
                "**you can clean them using** `.zombies -c`", del_in=0)
            await CHANNEL.log(
                f"#ZOMBIE_CHECK\n\n"
                f"CHAT: `{get_group.title}` (`{chat_id}`)\n"
                f"ZOMBIE COUNT: `{del_users}`"
                )

        else:
            await message.edit(f"{del_stats}", del_in=0)
            await CHANNEL.log(
                f"#ZOMBIE_CHECK\n\n"
                f"CHAT: `{get_group.title}` (`{chat_id}`)\n"
                r"ZOMBIE COUNT: `WOOHOO group is clean.. \^o^/`"
                )
