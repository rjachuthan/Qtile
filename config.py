import os
import subprocess
from functools import partial
from typing import Any

from libqtile import bar, hook, layout, widget
from libqtile.config import (
    Click,
    Drag,
    DropDown,
    Group,
    Key,
    KeyChord,
    Match,
    ScratchPad,
    Screen,
)
from libqtile.lazy import lazy

from colors import moonfly as themecolor

MOD: str = "mod4"
TERMINAL: str = "kitty"
BROWSER: str = "thorium-browser"
FONT: str = "JetBrainsMono NF"
FONTSIZE: int = 10
ICONSIZE: int = 16
colors, backgroundColor, foregroundColor, workspaceColor, chordColor = themecolor()

# Tips:
# 1. Use `python config.py` to check if the Qtile config is correct
# 2. Or better use `qtile check` for checking even the types

LAUNCHER_CMD: str = "rofi drun -show drun -config ~/.config/rofi/rofidmenu.rasi"
RUN_LOFI: str = os.path.expanduser("~/.config/qtile/scripts/lofi.sh")


@hook.subscribe.startup_once
def autostart() -> None:
    """Run the autostart script for qtile.

    Note: Make sure that
    - the path to the autostart.sh script is correct.
    - the file is executable.

    Returns:
        None
    """
    home = os.path.expanduser("~")
    subprocess.Popen([f"{home}/.config/qtile/autostart.sh"])


# A list of available commands that can be bound to keys can be found
# at https://docs.qtile.org/en/latest/manual/config/lazy.html
keys = [
    # Switch between windows
    Key([MOD], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([MOD], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([MOD], "j", lazy.layout.down(), desc="Move focus down"),
    Key([MOD], "k", lazy.layout.up(), desc="Move focus up"),
    Key([MOD], "space", lazy.layout.next(), desc="Move window focus to other window"),
    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key([MOD, "shift"], "h", lazy.layout.shuffle_left(), desc="Move window left"),
    Key([MOD, "shift"], "l", lazy.layout.shuffle_right(), desc="Move window right"),
    Key([MOD, "shift"], "j", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([MOD, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),
    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([MOD, "control"], "h", lazy.layout.grow_left(), desc="Grow window left"),
    Key([MOD, "control"], "l", lazy.layout.grow_right(), desc="Grow window right"),
    Key([MOD, "control"], "j", lazy.layout.grow_down(), desc="Grow window down"),
    Key([MOD, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),
    Key([MOD], "n", lazy.layout.normalize(), desc="Reset all window sizes"),
    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key(
        [MOD, "shift"],
        "Return",
        lazy.layout.toggle_split(),
        desc="Toggle split and unsplit sides of stack",
    ),
    Key([MOD], "Return", lazy.spawn(TERMINAL), desc="Launch terminal"),
    Key([MOD], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([MOD, "shift"], "w", lazy.window.kill(), desc="Kill focused window"),
    Key([MOD, "shift"], "f", lazy.window.toggle_fullscreen(), desc="Toggle fullscreen"),
    Key(
        [MOD, "shift"],
        "t",
        lazy.window.toggle_floating(),
        desc="Toggle floating window",
    ),
    Key([MOD], "b", lazy.hide_show_bar(), desc="Toggle Qtile Bar"),
    Key([MOD, "shift"], "r", lazy.layout.reset(), desc=""),
    Key([MOD, "shift"], "s", lazy.spawn("flameshot gui"), desc="Screenshot"),
    Key([MOD, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([MOD, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    Key([MOD], "d", lazy.spawn(LAUNCHER_CMD), desc="Spawn Launcher"),
    KeyChord(
        [MOD],
        "f",
        [
            Key([], "b", lazy.spawn(f"jumpapp {BROWSER}"), desc="Jump to Browser"),
            Key([], "q", lazy.spawn("jumpapp qutebrowser"), desc="Jump to Browser"),
            Key([], "n", lazy.spawn("jumpapp logseq"), desc="Jump to LogSeq"),
            Key([], "m", lazy.spawn("jumpapp mpv"), desc="Jump to MPV"),
            Key([], "c", lazy.spawn("jumpapp code"), desc="Jump to VS Code"),
        ],
        desc="Find Applications",
    ),
    KeyChord(
        [MOD],
        "p",
        [
            Key([], "n", lazy.spawn("playerctl next"), desc="Play Next"),
            Key(
                [],
                "p",
                lazy.spawn("playerctl --all-players play-pause"),
                desc="Toggle Play Pause",
            ),
            Key([], "b", lazy.spawn("playerctl previous"), desc="Play Previous"),
            Key([], "l", lazy.spawn(RUN_LOFI), desc="Run Lofi Music"),
        ],
        desc="Media Controls",
    ),
]

groups = [Group(i) for i in "123456789"]

for i in groups:
    keys.extend(
        [
            # mod1 + letter of group = switch to group
            Key(
                [MOD],
                i.name,
                lazy.group[i.name].toscreen(),
                desc="Switch to group {}".format(i.name),
            ),
            # mod1 + shift + letter of group = switch to & move focused window to group
            Key(
                [MOD, "shift"],
                i.name,
                lazy.window.togroup(i.name, switch_group=True),
                desc="Switch to & move focused window to group {}".format(i.name),
            ),
            # Or, use below if you prefer not to switch to that group.
            # # mod1 + shift + letter of group = move focused window to group
            # Key([mod, "shift"], i.name, lazy.window.togroup(i.name),
            #     desc="move focused window to group {}".format(i.name)),
        ]
    )

# Define Scratchpads
default_scratchpad = partial(DropDown, width=0.5, height=0.5, x=0.2, y=0.2, opacity=1)
music_scratchpad = partial(DropDown, width=0.8, height=0.8, x=0.1, y=0.1, opacity=1)

groups.append(
    ScratchPad(
        "scratchpad",
        [
            default_scratchpad("term", "kitty --class=scratch"),
            default_scratchpad("ranger", "kitty --class=ranger -e ranger"),
            default_scratchpad("volume", "kitty --class=volume -e pulsemixer"),
            default_scratchpad("calculator", "galculator"),
            music_scratchpad("music", "youtube-music"),
        ],
    )
)

# Adding Scratchpad Keybindings
keys.extend(
    [
        Key([MOD], "t", lazy.group["scratchpad"].dropdown_toggle("term")),
        Key([MOD], "v", lazy.group["scratchpad"].dropdown_toggle("volume")),
        Key([MOD], "c", lazy.group["scratchpad"].dropdown_toggle("calculator")),
        Key([MOD], "m", lazy.group["scratchpad"].dropdown_toggle("music")),
    ]
)


# Define layouts and layout themes
layout_theme: dict[str, Any] = {
    "margin": 5,
    "border_width": 1,
    "border_focus": colors[2],
    "border_normal": backgroundColor,
}

layouts = [
    # layout.MonadTall(**layout_theme),
    layout.Columns(**layout_theme),
    layout.MonadWide(**layout_theme),
    # layout.Floating(**layout_theme),
    # layout.RatioTile(**layout_theme),
    # layout.Max(**layout_theme),
]

widget_defaults = dict(font=FONT, fontsize=10, padding=3)
extension_defaults = widget_defaults.copy()

txt_icon = partial(widget.TextBox, fontsize=20, font=FONT, foreground=colors[7])


def truncate_text(text: str, length: int = 30) -> str:
    """
    Truncates the given text to a maximum length of `length` characters.
    - If the `text` is longer than `length`, it truncates the text and appends
      '...' to the truncated text.
    - If the `text` is shorter than `length`, it pads the text with spaces to
      make it `length` characters long.

    Args:
        text (str): The text to be truncated.
        length (int, optional): The maximum length of the truncated text.
            Defaults to 30.

    Returns:
        str: The truncated text.
    """
    shortend = text[: length - 3]
    return f"{shortend}..." if len(text) > length else text.ljust(length)


widget_list = [
    widget.CurrentLayoutIcon(
        scale=0.6,
        foreground=colors[6],
        background=colors[6],
        padding=5,
        fontsize=FONTSIZE,
    ),
    widget.Sep(linewidth=0, padding=10),
    widget.GroupBox(
        font=FONT,
        fontsize=FONTSIZE,
        # padding=6,
        disable_drag=True,
        active=colors[2],
        inactive=foregroundColor,
        hide_unused=True,
        rounded=True,
        highlight_method="block",
        foreground=foregroundColor,
        background=backgroundColor,
        use_mouse_wheel=False,
    ),
    widget.Sep(linewidth=0, padding=10),
    widget.TaskList(
        icon_size=ICONSIZE,
        fontsize=FONTSIZE,
        font=FONT,
        padding=4,
        highlight_method="block",
        parse_text=truncate_text,
        urgent_alert_method="border",
        urgent_border=colors[1],
        rounded=True,
        txt_floating="🗗 ",
        txt_maximized="🗖 ",
        txt_minimized="🗕 ",
    ),
    widget.OpenWeather(
        app_key="4cf3731a25d1d1f4e4a00207afd451a2",
        cityid="1277333",
        format="{icon} {location_city} {main_temp}°",
        metric=True,
        font=FONT,
        fontsize=FONTSIZE,
        foreground=foregroundColor,
    ),
    widget.Sep(linewidth=0, padding=10),
    widget.Systray(background=backgroundColor, icon_size=ICONSIZE),
    widget.Sep(linewidth=0, padding=10),
    widget.CPU(
        font=FONT,
        fontsize=FONTSIZE,
        update_interval=1.0,
        format="  {load_percent}%",
        foreground=foregroundColor,
        padding=5,
    ),
    widget.Sep(linewidth=0, padding=10),
    widget.ThermalZone(
        font=FONT,
        fontsize=FONTSIZE,
        fgcolor_normal=foregroundColor,
        foreground=foregroundColor,
        padding=5,
        format="󰏈  {temp}°C",
    ),
    widget.Sep(linewidth=0, padding=10),
    widget.NvidiaSensors(
        font=FONT,
        fontsize=FONTSIZE,
        format="  {temp}°C",
        foreground=foregroundColor,
    ),
    widget.Sep(linewidth=0, padding=10),
    widget.Clock(
        format="  %I:%M %p", font=FONT, fontsize=FONTSIZE, foreground=foregroundColor
    ),
    widget.Sep(linewidth=0, padding=10),
    # txt_icon(text=""),
    widget.Volume(
        font=FONT,
        fontsize=(FONTSIZE+4),
        foreground=foregroundColor,
        emoji=True,
        padding=5,
        emoji_list=["󰝟", "", "", ""],
    ),
    widget.Sep(linewidth=0, padding=10),
    widget.Sep(linewidth=1, padding=10, foreground=colors[5]),
    widget.Sep(linewidth=0, padding=10),
    widget.QuickExit(),
]

screens = [
    Screen(
        top=bar.Bar(
            widgets=widget_list,
            size=30,
            background=backgroundColor,
            margin=5,
            opacity=0.8,
            border_width=[0, 0, 0, 0],  # Draw top and bottom borders
        ),
    ),
]

# Drag floating layouts.
mouse = [
    Drag(
        [MOD],
        "Button1",
        lazy.window.set_position_floating(),
        start=lazy.window.get_position(),
    ),
    Drag(
        [MOD], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()
    ),
    Click([MOD], "Button2", lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules: list = []
follow_mouse_focus = True
bring_front_click = False
floats_kept_above = True
cursor_warp = False

floating_layout = layout.Floating(
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
        Match(title="Lxappearance"),
        Match(title="galculator"),
    ]
)

auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# When using the Wayland backend, this can be used to configure input devices.
wl_input_rules = None

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"
