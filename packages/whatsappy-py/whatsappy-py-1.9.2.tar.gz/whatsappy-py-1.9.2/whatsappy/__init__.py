from .chat import (
    last_message, new_message, send, reply, 
    send_file, reply_privately, reply_file_privately
)
from .actions import (
    add_to_group, remove_from_group, make_group_admin, 
    select_chat_by_number, select_chat_by_name
)
from .group import change_group_description, change_group_name, leave_group
from .get import get_pinned_chats, get_recent_chats, get_group_invite_link
from .login import login, close

class Whatsapp:

    login                       = login
    close                       = close

    add_to_group                = add_to_group
    remove_from_group           = remove_from_group
    make_group_admin            = make_group_admin

    last_message                = last_message
    new_message                 = new_message
    send                        = send
    send_file                   = send_file
    reply                       = reply
    reply_privately             = reply_privately
    reply_file_privately        = reply_file_privately
    select_chat_by_name         = select_chat_by_name
    select_chat_by_number       = select_chat_by_number

    get_pinned_chats            = get_pinned_chats
    get_recent_chats            = get_recent_chats
    get_group_invite_link       = get_group_invite_link

    change_group_description    = change_group_description
    change_group_name           = change_group_name
    leave_group                 = leave_group

    # TODO: Get group info (maybe turn it into a class)

    # TODO: Create group

    # TODO: Change profile picture

    # TODO: Change group profile picture url

whatsapp = Whatsapp()