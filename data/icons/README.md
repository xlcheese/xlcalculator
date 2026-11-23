The small icons, as drawn: each size is its own drawing, with its border on whole pixels.
The program installs PNG copies of these (in `usr/share/icons/hicolor/*/apps/`), as Flathub asks.
After changing one, render it again at its own size, for example:

    rsvg-convert -w 16 -h 16 io.github.xlcheese.XlCalculator-16.svg \
        -o ../../usr/share/icons/hicolor/16x16/apps/io.github.xlcheese.XlCalculator.png
