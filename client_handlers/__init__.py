from client_handlers.buttons_h import HowDItWorks, GetLink
from client_handlers.dump_cmd import Dump
from client_handlers.mailing import Mailing
from client_handlers.settings import OpSettings, ChangeOpConfig, ChannelUsernameDownloader
from client_handlers.start import StartCmd

active_handlers = [
    StartCmd,
    Mailing,
    HowDItWorks,
    GetLink,
    OpSettings,
    ChangeOpConfig,
    ChannelUsernameDownloader,
    Dump,
]
