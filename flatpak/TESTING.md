# Testing the Flatpak on other desktops

Before a release goes to Flathub, try the Flatpak on Linux Mint and on a GNOME and a KDE desktop.
Virtual machines are enough (GNOME Boxes or VirtualBox, with live images):

1. **Linux Mint** (Cinnamon, X11): where most people use xl-Calculator.
2. **Fedora Workstation**: GNOME on Wayland.
3. **Fedora KDE** or **Kubuntu**: KDE Plasma on Wayland.

About 10 to 15 minutes each.

## Install the test bundle

Copy `xl-calculator.flatpak` into the machine, then in a terminal:

```
flatpak remote-add --user --if-not-exists flathub https://dl.flathub.org/repo/flathub.flatpakrepo
flatpak install --user xl-calculator.flatpak
flatpak run io.github.xlcheese.XlCalculator
```

The first install also downloads the GNOME runtime from Flathub (about 1 GB, once). To remove it
afterwards: `flatpak uninstall --user io.github.xlcheese.XlCalculator`.

To see whether the desktop runs Wayland: `echo $XDG_SESSION_TYPE` (says `wayland` or `x11`).

## Checklist

For each desktop, note anything that looks wrong, ideally with a screenshot.

**The window**
- [ ] It's in the applications menu, with the xl-Calculator icon, and the icon in the panel or dock
      is sharp (not blurry) at small sizes
- [ ] The title bar shows the mode and the Buffet button; minimize, maximize, and close work
- [ ] The number keys and the shaded keys look right with the desktop's theme (borders, shadows)

**The Buffet menu** (the most important on Wayland)
- [ ] Click the Buffet button: the menu opens right under the title bar, inside or next to the window,
      not somewhere else on the screen
- [ ] Move the window to the right edge and to the bottom of the screen, and open it again
- [ ] F10, and Alt+M (Mode), open it from the keyboard; the arrow keys move around; Escape closes it
- [ ] Clicking outside it closes it
- [ ] Ctrl+Alt+S switches to Scientific, Ctrl+Q quits (shortcuts work with the menu closed)
- [ ] Preferences → Menu → Buffet menu off: a menu bar appears; on again: the Buffet button is back

**The modes**
- [ ] Basic: 12 × 12 = 144, and √ of 9 is 3
- [ ] Scientific: the f(x) menu opens in the right place
- [ ] Unit Converter: change a unit in the dropdowns (they open in the right place)
- [ ] Currency Converter: Download Rates works; the menus list currencies; Add or Remove
      Currencies… opens the list, and searching "peso" finds eight pesos
- [ ] Preferences → Currency Converter → "Also when xl-Calculator is closed" is greyed out, with
      "Needs xl-Calculator installed from its package" (expected: a Flatpak can't do this)

**Printing**
- [ ] File → Print Preview shows the history as a tape
- [ ] File → Print opens the print dialog (printing to a PDF file is enough)

**Another language**
- [ ] Start it in Russian (or German, Spanish, French, Portuguese):
      `LANGUAGE=ru flatpak run io.github.xlcheese.XlCalculator`. The menus and the currency names
      are in that language

**Afterwards**
- [ ] Close and reopen it: it opens in the last mode, with the same settings

## Also worth trying

The `.deb` on **Ubuntu** (GNOME on Wayland): `sudo apt install ./xl-calculator_*.deb`, then the
Buffet menu items of the checklist.
