import sys
import os
import time
import random
import signal

import orjson

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from rich.live import Live
from rich.table import Table
from rich.console import Console
from rich.panel import Panel
from rich.layout import Layout
from rich import box
from rich.align import Align


tiers = {
    "IRON": 0,
    "BRONZE": 1,
    "SILVER": 2,
    "GOLD": 3,
    "PLATINUM": 4,
    "EMERALD": 5,
    "DIAMOND": 6,
    "MASTER": 7,
    "GRANDMASTER": 8,
    "CHALLENGER": 9,
}

division = {
    "IV": 0,
    "III": 1,
    "II": 2,
    "I": 3,
}


def sort_summoners(summoners_list: list[dict], league: str) -> list[dict]:
    """
    Sorts the summoners by their rank.
    """
    if league == "solo":
        league = "420"
    elif league == "flex":
        league = "440"

    # remove summoners where the league == None
    summoners = []
    for summoner in summoners_list:
        if summoner["leagueEntries"][league] is not None:
            summoners.append(summoner)
    
    # sort the summoners
    # 1. tagLine
    # 2. gameName
    # 3. leaguePoints
    # 4. rank
    # 5. tier
    summoners.sort(key=lambda summoner: summoner["tagLine"])
    summoners.sort(key=lambda summoner: summoner["gameName"])
    summoners.sort(key=lambda summoner: summoner["leagueEntries"][league]["leaguePoints"], reverse=True)
    summoners.sort(key=lambda summoner: division[summoner["leagueEntries"][league]["rank"]], reverse=True)
    summoners.sort(key=lambda summoner: tiers[summoner["leagueEntries"][league]["tier"]], reverse=True)
    return summoners


def generate_table() -> Table:
    """Make a new table."""
    solo_table = Table()
    solo_table.add_column("#")
    solo_table.add_column("Summoner")
    solo_table.add_column("Tier")
    solo_table.add_column("Division")
    solo_table.add_column("LP")
    solo_table.add_column("Games")
    solo_table.add_column("Winrate")

    flex_table = Table()
    flex_table.add_column("#")
    flex_table.add_column("Summoner")
    flex_table.add_column("Tier")
    flex_table.add_column("Division")
    flex_table.add_column("LP")
    flex_table.add_column("Games")
    flex_table.add_column("Winrate")

    with open("summoners.json", "r") as f:
        summoners = orjson.loads(f.read())

    # Generate Solo Table
    summoners_solo = sort_summoners(summoners, "solo")
    rank = 1
    for summoner in summoners_solo:
        solo_table.add_row(
            str(rank),
            f"{summoner['gameName']}#{summoner['tagLine']}",
            f"{summoner['leagueEntries']['420']['tier']}",
            f"{summoner['leagueEntries']['420']['rank']}",
            f"{summoner['leagueEntries']['420']['leaguePoints']}",
            f"{summoner['leagueEntries']['420']['wins'] + summoner['leagueEntries']['420']['losses']}",
            f"{round(summoner['leagueEntries']['420']['wins'] / (summoner['leagueEntries']['420']['wins'] + summoner['leagueEntries']['420']['losses']) * 100, 2)}%",
        )
        rank += 1

    # Generate Solo Table
    summoners_flex = sort_summoners(summoners, "flex")
    rank = 1
    for summoner in summoners_flex:
        flex_table.add_row(
            str(rank),
            f"{summoner['gameName']}#{summoner['tagLine']}",
            f"{summoner['leagueEntries']['440']['tier']}",
            f"{summoner['leagueEntries']['440']['rank']}",
            f"{summoner['leagueEntries']['440']['leaguePoints']}",
            f"{summoner['leagueEntries']['440']['wins'] + summoner['leagueEntries']['440']['losses']}",
            f"{round(summoner['leagueEntries']['440']['wins'] / (summoner['leagueEntries']['440']['wins'] + summoner['leagueEntries']['440']['losses']) * 100, 2)}%",
        )
        rank += 1

    return solo_table, flex_table


def generate_layout() -> Layout:
    """Generate a layout containing both the solo and flex tables."""
    solo_table, flex_table = generate_table()

    # Align the tables to center horizontally and vertically
    solo_table_aligned = Align.center(solo_table, vertical="middle")
    flex_table_aligned = Align.center(flex_table, vertical="middle")

    layout = Layout()
    layout.split(
        Layout(name="solo"),
        Layout(name="flex")
    )
    layout["solo"].update(Panel(solo_table_aligned, title="Solo Queue", border_style="green"))
    layout["flex"].update(Panel(flex_table_aligned, title="Flex Queue", border_style="blue"))

    # Wrap the layout in another Align for vertical centering
    centered_layout = Layout()
    centered_layout.update(Align(layout, vertical="middle"))

    return centered_layout


class FileChangeHandler(FileSystemEventHandler):
    def __init__(self, live, callback):
        self.live = live
        self.callback = callback
        self._last_modified = time.time()

    def on_modified(self, event):
        print(f"File changed: {event.src_path}")
        if event.src_path == "summoners.json":
            # Debounce to prevent multiple updates in quick succession
            if time.time() - self._last_modified < 1:
                return
            self._last_modified = time.time()

            # Small delay to ensure the file is fully written
            time.sleep(0.1)
            self.callback(self.live)


def handle_terminal_resize(signum, frame):
    # This will be called whenever the terminal is resized.
    # You can force the Live display to refresh here.
    # live.update(generate_layout())
    live.refresh()


if __name__ == "__main__":
    console = Console()
    with Live(generate_layout(), auto_refresh=False, console=console) as live:
        # Register a signal handler to handle terminal resizes
        signal.signal(signal.SIGWINCH, handle_terminal_resize)

        while True:
            time.sleep(10)