#!/usr/bin/env python
"""
Sample Barebones Pandora Player

This is a very simple Pandora player that streams music from Pandora. It
requires mpg123 or VLC to function. No songs are downloaded, they are streamed
directly from Pandora's servers.
"""
from __future__ import print_function

import os
import sys
import argparse
from pandora import clientbuilder

from .utils import Colors, Screen
from .audio_backend import RemoteVLC
from .audio_backend import MPG123Player, VLCPlayer
from .audio_backend import PlayerUnusable


class PlayerCallbacks(object):
    """Interface for Player Callbacks

    This class simply exists to document the interface for callback
    implementers implementers need not extend this class.
    """

    def pre_poll(self):
        """Called before polling for process status
        """
        pass

    def post_poll(self):
        """Called after polling for process status
        """
        pass


class PlayerApp(object):

    def __init__(self):
        self.client = None
        self.screen = Screen()

    def get_player(self, vlc_net=None):
        # The user must explicitly request network VLC so we should always
        # honor that request, to this end we try network first and fail hard
        # if that isn't available.
        if vlc_net:
            try:
                host, port = vlc_net.split(":")
                player = RemoteVLC(host, port, self, sys.stdin)
                Screen.print_success("Using Remote VLC")
                return player
            except PlayerUnusable:
                Screen.print_error("Unable to connect to vlc")
                raise

        try:
            player = VLCPlayer(self, sys.stdin)
            return player
        except PlayerUnusable:
            pass

        try:
            player = MPG123Player(self, sys.stdin)
            self.screen.print_success("Using mpg123")
            return player
        except PlayerUnusable:
            pass

        self.screen.print_error("Unable to find a player")
        sys.exit(1)

    def get_client(self):
        cfg_file = os.environ.get("PYDORA_CFG", "")
        builder = clientbuilder.PydoraConfigFileBuilder(cfg_file)
        if builder.file_exists:
            return builder.build()

        builder = clientbuilder.PianobarConfigFileBuilder()
        if builder.file_exists:
            return builder.build()

        if not self.client:
            self.screen.print_error("No valid config found")
            sys.exit(1)

    def play(self, song):
        """Play callback
        """

    def raise_volume(self, song):
        try:
            self.player.raise_volume()
        except NotImplementedError:
            self.screen.print_error("Cannot sleep this type of track")

    def lower_volume(self, song):
        try:
            self.player.lower_volume()
        except NotImplementedError:
            self.screen.print_error("Cannot sleep this type of track")

    def quit(self, song):
        self.player.end_station()
        sys.exit(0)

    def pre_poll(self):
        self.screen.set_echo(False)

    def post_poll(self):
        self.screen.set_echo(True)

    def pre_flight_checks(self):
        # See #52, this key no longer passes some server-side check
        if self.client.partner_user == "iphone":
            self.screen.print_error((
                "The `iphone` partner key set is no longer compatible with "
                "pydora. Please re-run pydora-configure to re-generate "
                "your config file before continuing."))
            sys.exit(1)

    def _parse_args(self):
        parser = argparse.ArgumentParser(
            description="command line Pandora player")
        parser.add_argument(
            "--vlc-net", dest="vlc_net",
            help="connect to VLC over the network (host:port)")
        parser.add_argument(
            "-v", dest="verbose", action="store_true",
            help="enable verbose logging")
        return parser.parse_args()

    def run(self):
        args = self._parse_args()

        self.player = self.get_player(args.vlc_net)
        self.player.start()

        self.client = self.get_client()

        self.pre_flight_checks()

        station = self.client.get_station('4168046722632754502')
        self.player.play_station(station)


def main():
    PlayerApp().run()

