# Terraria Fishing bot

A [Terraria](https://terraria.org/) fishing bot.

It uses image recognition to determine the position of the in-game bobber and (with [Sonar Potion](https://terraria.wiki.gg/wiki/Sonar_Potion)) also tries to determine what fish has been caught.

This uses pyautogui, python-opencv (and OpenCV) together with [Tesseract OCR](https://github.com/tesseract-ocr/tesseract) to automatically fish.

## Running

Download the repository

Install python (tested with 3.12)

(Optional) Create virtual python environment

pip install -r requirements.txt

Run main.py in your preferred terminal

## Caveats

While fishing in lava it might lose track of the bobber when lava spouts up around it, this has not been a huge problem for catching in my testing though.

It currently (bobber1.png) only searches for the [Golden Fishing Bobber](https://terraria.wiki.gg/wiki/Glowing_Fishing_Bobber) though other bobbers could be added.

The OCR isn't great, Terraria appartently uses "Andy Bold" as a typeface with very little kerning, which tesseract-ocr does not detect very well.
