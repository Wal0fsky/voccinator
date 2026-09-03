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
python voccinator3.py
```

The first time you run it, the program asks where it should keep your learnsets. Press enter to put the folder in the current directory, or type N and give it your own path. It remembers your choice, so you only do this once.

## How the practise mode works

You get shown a word and you type what it means. If your answer is correct, the word disappears from the pile. If it is wrong, it stays in and the pile gets shuffled, so you will see it again later. You keep going until the pile is empty.

While practising you can type these instead of an answer:

* `save` stores your current progress
* `load` brings that progress back
* `exit` leaves the practise mode

## A quick tutorial

### 1. Create a learnset

1. Start Voccinator and choose **Create New Learnset** from the home menu.
2. Enter a name for the learnset, for example `French Basics`.
3. Enter a word and its definition when asked.
4. Repeat for as many words as you like. Type `exit` instead of a word to finish adding words.

### 2. Practise your words

1. Choose **Write Practise** from the home menu.
2. Select the learnset you want to practise.
3. Type the exact definition of each displayed word and press enter.
4. Correct answers are removed from the pile. Wrong answers stay in the pile and appear again later.
5. Continue until Voccinator tells you that you have defined all words correctly.

### 3. Save and load your progress

Saving and loading happen while you are in **Write Practise**, at the prompt where you enter a definition:

```text
word shown by Voccinator
Enter definition: save
Saving...
```

To continue later, start **Write Practise** again, choose the learnset, and type `load` at the definition prompt:

```text
word shown by Voccinator
Enter definition: load
Fetching data...
```

Your saved progress is restored and you can continue answering definitions. Type `exit` at any definition prompt when you want to leave practice. Saving creates a small progress file next to the program, so keep it there if you want to load the saved progress later.

### 4. Other home menu commands

* **Create New Learnset** creates a new CSV learnset.
* **Edit Existing Learnset** adds more word and definition pairs to an existing learnset. Type `exit` when you are finished.
* **Show Learnset** displays all words and definitions in a learnset.
* **Write Practise** starts a vocabulary quiz and includes the `save`, `load`, and `exit` commands described above.
* **Delete Words From Learnset** lets you select and remove one or more words, then asks you to confirm.
* **Exit** closes Voccinator.

## My learnsets

I pushed my own learnsets to this repo as well, so you do not have to start from zero. They are in the LEARNSETS folder and you can just use them, copy them or change them however you like. They are normal CSV files, so if you want to add your own words you can either do it in the program or open the file in a text editor. No promises that every definition is perfect, they are the ones I made for school.


## Good to know

* Your answer has to match the definition exactly, so watch out for typos and capital letters
* The program is set up for UTF8, which means accents and special characters work fine (useful for French)
* Every learnset is just a CSV file with a semicolon between the word and the definition
