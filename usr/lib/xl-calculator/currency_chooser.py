# xl-Calculator: a calculator for Linux Mint and the Cinnamon desktop.
# Copyright (C) 2026 Wesley Hayslip
#
# This program is free software: you can redistribute it and/or modify it under the
# terms of the GNU General Public License as published by the Free Software Foundation,
# either version 3 of the License, or (at your option) any later version.
# It is distributed WITHOUT ANY WARRANTY; see <https://www.gnu.org/licenses/>.
# SPDX-License-Identifier: GPL-3.0-or-later
"""Add or Remove Currencies: every currency there's a rate for, to tick the ones the Currency
Converter's menus offer. Changes take effect at once, in every window."""

from gi.repository import Gdk, Gtk
from i18n import _, ngettext
from currency import BOC, ECB, UN, Rates, currency_name, english_currency_name, offered_currencies

def source_note(source):
    """Where a currency's rate comes from, and how often it changes, beside it in the list."""
    if source == UN:
        return _("UN Treasury, monthly")
    if source == BOC:
        return _("Bank of Canada, daily")
    return _("European Central Bank, daily")


class CurrencyChooser(Gtk.Window):
    """The list of currencies, each with a tick box, and a search box above it."""

    def __init__(self, calculator):
        super().__init__(title=_("Currencies in the Menus"), transient_for=calculator, destroy_with_parent=True)
        self.calculator = calculator
        self.set_type_hint(Gdk.WindowTypeHint.DIALOG)
        self.set_default_size(460, 600)
        self.syncing = False

        outer = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        for side in ("start", "end", "top", "bottom"):
            getattr(outer, f"set_margin_{side}")(12)
        intro = Gtk.Label(label=_("Tick the currencies to show in the Currency Converter's menus."), xalign=0)
        intro.set_line_wrap(True)
        outer.pack_start(intro, False, False, 0)
        self.search = Gtk.SearchEntry(placeholder_text=_("Search by name or code"))
        self.search.connect("search-changed", lambda entry: self.list.invalidate_filter())
        outer.pack_start(self.search, False, False, 0)

        self.list = Gtk.ListBox(selection_mode=Gtk.SelectionMode.NONE)
        self.list.set_filter_func(self.matches)
        self.ticks = {}
        data = Rates.get()
        sources = data["sources"] if data else {}
        for name, code in sorted(((currency_name(c), c) for c in offered_currencies()), key=lambda p: p[0].casefold()):
            tick = Gtk.CheckButton(label=f"{name} ({code})")
            tick.connect("toggled", self.on_toggled)
            note = Gtk.Label(label=source_note(sources.get(code, ECB)), xalign=1)
            note.get_style_context().add_class("dim-label")
            line = Gtk.Box(spacing=12)
            for side in ("start", "end"):
                getattr(line, f"set_margin_{side}")(6)
            line.pack_start(tick, True, True, 0)
            line.pack_end(note, False, False, 0)
            row = Gtk.ListBoxRow()
            row.add(line)
            row.search_text = f"{name} {code} {english_currency_name(code)}".casefold()   # "peso" in any language
            self.list.add(row)
            self.ticks[code] = tick
        scroller = Gtk.ScrolledWindow()
        scroller.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        scroller.set_shadow_type(Gtk.ShadowType.IN)
        scroller.add(self.list)
        outer.pack_start(scroller, True, True, 0)

        if data is None or UN not in data["dates"]:
            more = Gtk.Label(label=_("More currencies appear here once rates have been downloaded."), xalign=0)
            more.get_style_context().add_class("dim-label")
            more.set_line_wrap(True)
            outer.pack_start(more, False, False, 0)
        self.count = Gtk.Label(xalign=0)
        outer.pack_start(self.count, False, False, 0)

        common = Gtk.Button(label=_("Common Currencies"))
        common.set_tooltip_text(_("Show the most traded currencies and your own, as at first"))
        common.connect("clicked", lambda b: calculator.set_shown_currencies(None))
        close = Gtk.Button(label=_("Close"))
        close.connect("clicked", lambda b: self.destroy())
        buttons = Gtk.Box(spacing=6)
        buttons.pack_start(common, False, False, 0)
        buttons.pack_end(close, False, False, 0)
        outer.pack_start(buttons, False, False, 0)
        self.add(outer)
        self.connect("key-press-event", self.on_key)
        self.sync()
        self.show_all()
        self.search.grab_focus()

    def matches(self, row):
        words = self.search.get_text().casefold().split()
        return all(word in row.search_text for word in words)

    def on_toggled(self, tick):
        if self.syncing:
            return
        self.calculator.set_shown_currencies([code for code, t in self.ticks.items() if t.get_active()])

    def sync(self):
        """Show which currencies the menus offer (they can also change from another window)."""
        shown = set(self.calculator.shown_currency_codes())
        self.syncing = True
        for code, tick in self.ticks.items():
            tick.set_active(code in shown)
        self.syncing = False
        count = sum(1 for code in self.ticks if code in shown)
        self.count.set_text(ngettext("{count} of {total} currencies in the menus",
                                     "{count} of {total} currencies in the menus", count)
                            .format(count=count, total=len(self.ticks)))

    def on_key(self, widget, event):
        if Gdk.keyval_name(event.keyval) == "Escape" and not self.search.get_text():
            self.destroy()
            return True
        return False
