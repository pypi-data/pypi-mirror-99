
# region [Imports]

# * Standard Library Imports -->
import gc
import os
import re
import sys
import json
import lzma
import time
import queue
import logging
import platform
import subprocess
from enum import Enum, Flag, auto, unique
from time import sleep
from pprint import pprint, pformat
from typing import Union, TYPE_CHECKING
from datetime import tzinfo, datetime, timezone, timedelta
from functools import wraps, lru_cache, singledispatch, total_ordering, partial
from contextlib import contextmanager
from collections import Counter, ChainMap, deque, namedtuple, defaultdict
from multiprocessing import Pool
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from tempfile import TemporaryDirectory
from urllib.parse import urlparse
import asyncio
from concurrent.futures import ThreadPoolExecutor
import unicodedata
from io import BytesIO
from textwrap import dedent

# * Third Party Imports -->
from icecream import ic
# import requests
# import pyperclip
# import matplotlib.pyplot as plt
# from bs4 import BeautifulSoup
# from dotenv import load_dotenv
# from github import Github, GithubException
# from jinja2 import BaseLoader, Environment
# from natsort import natsorted
# from fuzzywuzzy import fuzz, process
import aiohttp
import discord
from discord.ext import tasks, commands, flags
from async_property import async_property
from dateparser import parse as date_parse

# * Gid Imports -->
import gidlogger as glog

# * Local Imports -->
from antipetros_discordbot.cogs import get_aliases, get_doc_data
from antipetros_discordbot.utility.misc import STANDARD_DATETIME_FORMAT, CogConfigReadOnly, make_config_name, is_even
from antipetros_discordbot.utility.checks import command_enabled_checker, allowed_requester, allowed_channel_and_allowed_role_2, has_attachments, owner_or_admin, log_invoker
from antipetros_discordbot.utility.gidtools_functions import loadjson, writejson, pathmaker, pickleit, get_pickled
from antipetros_discordbot.init_userdata.user_data_setup import ParaStorageKeeper
from antipetros_discordbot.utility.discord_markdown_helper.special_characters import ZERO_WIDTH
from antipetros_discordbot.utility.poor_mans_abc import attribute_checker
from antipetros_discordbot.utility.enums import RequestStatus, CogState
from antipetros_discordbot.utility.replacements.command_replacement import auto_meta_info_command
from antipetros_discordbot.utility.discord_markdown_helper.discord_formating_helper import embed_hyperlink
from antipetros_discordbot.utility.emoji_handling import normalize_emoji
from antipetros_discordbot.utility.parsing import parse_command_text_file

if TYPE_CHECKING:
    from antipetros_discordbot.engine.antipetros_bot import AntiPetrosBot


# endregion[Imports]

# region [TODO]


# endregion [TODO]

# region [AppUserData]

# endregion [AppUserData]

# region [Logging]

log = glog.aux_logger(__name__)
glog.import_notification(log, __name__)

# endregion[Logging]

# region [Constants]

APPDATA = ParaStorageKeeper.get_appdata()
BASE_CONFIG = ParaStorageKeeper.get_config('base_config')
COGS_CONFIG = ParaStorageKeeper.get_config('cogs_config')
# location of this file, does not work if app gets compiled to exe with pyinstaller
THIS_FILE_DIR = os.path.abspath(os.path.dirname(__file__))

COG_NAME = "BotFeedbackCog"

CONFIG_NAME = make_config_name(COG_NAME)

get_command_enabled = command_enabled_checker(CONFIG_NAME)

# endregion[Constants]

# region [Helper]

_from_cog_config = CogConfigReadOnly(CONFIG_NAME)

# endregion [Helper]


class BotFeedbackCog(commands.Cog, command_attrs={'name': COG_NAME}):
    """
    WiP
    """
# region [ClassAttributes]

    config_name = CONFIG_NAME
    bot_suggestion_data_file = pathmaker(APPDATA['bot_feedback_data'], 'bot_suggestions.json')
    bot_feature_request_data_file = pathmaker(APPDATA['bot_feedback_data'], "bot_feature_requests.json")
    bot_bug_data_file = pathmaker(APPDATA["bot_feedback_data"], "bot_bugs.json")

    docattrs = {'show_in_readme': True,
                'is_ready': (CogState.UNTESTED | CogState.FEATURE_MISSING | CogState.OUTDATED | CogState.CRASHING | CogState.EMPTY | CogState.DOCUMENTATION_MISSING,)}

    required_config_data = dedent("""
                                    """).strip('\n')
# endregion [ClassAttributes]

# region [Init]

    def __init__(self, bot: "AntiPetrosBot"):
        self.bot = bot
        self.support = self.bot.support
        self.allowed_channels = allowed_requester(self, 'channels')
        self.allowed_roles = allowed_requester(self, 'roles')
        self.allowed_dm_ids = allowed_requester(self, 'dm_ids')
        glog.class_init_notification(log, self)

# endregion [Init]

# region [Properties]

    @property
    def bot_suggestion_data(self):
        if os.path.isfile(self.bot_suggestion_data_file) is False:
            writejson([], self.bot_suggestion_data_file)
        return loadjson(self.bot_suggestion_data_file)

    @property
    def bot_feature_request_data(self):
        if os.path.isfile(self.bot_feature_request_data_file) is False:
            writejson([], self.bot_feature_request_data_file)
        return loadjson(self.bot_feature_request_data_file)

    @property
    def bot_feature_request_data(self):
        if os.path.isfile(self.bot_bug_data_file) is False:
            writejson([], self.bot_bug_data_file)
        return loadjson(self.bot_bug_data_file)

# endregion [Properties]

# region [Setup]

    async def on_ready_setup(self):

        log.debug('setup for cog "%s" finished', str(self))

    async def update(self, typus):
        return
        log.debug('cog "%s" was updated', str(self))

# endregion [Setup]

# region [Loops]


# endregion [Loops]

# region [Listener]


# endregion [Listener]

# region [Commands]


# endregion [Commands]

# region [DataStorage]


# endregion [DataStorage]

# region [HelperMethods]


# endregion [HelperMethods]

# region [SpecialMethods]

    def cog_check(self, ctx):
        return True

    async def cog_command_error(self, ctx, error):
        pass

    async def cog_before_invoke(self, ctx):
        pass

    async def cog_after_invoke(self, ctx):
        pass

    def cog_unload(self):
        log.debug("Cog '%s' UNLOADED!", str(self))

    def __repr__(self):
        return f"{self.__class__.__name__}({self.bot.__class__.__name__})"

    def __str__(self):
        return self.__class__.__name__


# endregion [SpecialMethods]


def setup(bot):
    """
    Mandatory function to add the Cog to the bot.
    """
    bot.add_cog(attribute_checker(BotFeedbackCog(bot)))


# region [Main_Exec]

if __name__ == '__main__':
    pass

# endregion [Main_Exec]