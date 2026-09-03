# Voccinator 3.0

A small vocabulary trainer that runs in your terminal. You make your own learnsets, you type in words and their meanings, and then you let the program quiz you until you get everything right. I built it because writing vocab on paper cards takes forever and I kept losing them.

## What it can do

* Create a new learnset and fill it with word and definition pairs
* Add more words to a learnset you already made
* Show everything that is inside a learnset
* Write practise, where you get a word and have to type the definition
* Delete single words from a learnset

Everything gets saved as CSV files in a folder called LEARNSETS, so you can open them in Excel or a text editor if you want.

## Setup

You need Python 3. Install the two packages first:

```bash
pip install -r requirements.txt
```

Then start it:

```bash
python voccinator.py
```

The first time you run it, the program asks where it should keep your learnsets. Press enter to put the folder in the current directory, or type N and give it your own path. It remembers your choice, so you only do this once.

## How the practise mode works

You get shown a word and you type what it means. If your answer is correct, the word disappears from the pile. If it is wrong, it stays in and the pile gets shuffled, so you will see it again later. You keep going until the pile is empty.

While practising you can type these instead of an answer:

* `save` stores your current progress
* `load` brings that progress back
* `exit` leaves the practise mode

## Good to know

* Your answer has to match the definition exactly, so watch out for typos and capital letters
* The program is set up for UTF8, which means accents and special characters work fine (useful for French)
* Every learnset is just a CSV file with a semicolon between the word and the definition
