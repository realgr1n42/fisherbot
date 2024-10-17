import os
from typing import List

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton, ReplyKeyboardMarkup


class CustomInlineButton:
    def __init__(self, text: str, callback_data: str):
        self.text = text
        self.callback_data = callback_data


class CustomReplyButton:
    def __init__(self, text: str):
        self.text = text


def create_centered_line(text, fill_char='-', line_width=30):
    text_length = len(text)
    if text_length >= line_width:
        return text
    else:
        total_padding = line_width - text_length
        left_padding = fill_char * (total_padding // 2)
        right_padding = fill_char * (total_padding - len(left_padding))
        line = f"{left_padding}{text}{right_padding}"
        return line


def print_directory_tree(startpath):
    stack = []
    for root, dirs, files in os.walk(startpath):
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        files = [f for f in files if not f.startswith('.')]
        level = root.replace(startpath, '').count(os.sep)
        indent = ''
        if level > 0:
            indent = '│   ' * (level - 1) + '├── '
        else:
            indent = ''
        print('{}{}/'.format(indent, os.path.basename(root)))
        subindent = '│   ' * level + '├── '
        for i, f in enumerate(files):
            if i == len(files) - 1:
                subindent = '│   ' * level + '└── '
            print('{}{}'.format(subindent, f))


def generate_inline_buttons(buttons: List[CustomInlineButton]):
    return [InlineKeyboardButton(text=button.text, callback_data=button.callback_data) for button in buttons]


def create_inline_keyboard(buttons: List[CustomInlineButton]):
    keyboard = [generate_inline_buttons([button]) for button in buttons]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def generate_reply_buttons(buttons: List[CustomReplyButton]):
    return [KeyboardButton(text=button.text) for button in buttons]


def create_reply_keyboard(buttons: List[CustomReplyButton]):
    keyboard = [generate_reply_buttons(buttons)]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)


