# Pokémon Deck Comparing Tool

The purpose of this tool is to compare two Pokémon decks, telling the user what cards need to be removed and added from the first deck to get to the second. This allows the user to quickly know what they need to construct a new deck from cards already present in an existing deck.

# Installation Instructions

1. Clone this repository (`git clone <repository url> <destination directory>`)
2. Ensure that Python 3.10 or higher is installed on your machine. 
3. Navigate to the repository
4. Run `pip install -r requirements.txt`

# Input Files

This program requires two deck files as input. A proper deck file consists of one optional section and three required sections:
1. The "Source" section contains a url for the decklist that the file came from.
    - The syntax for this section is `Source: <url>`
    - This section is optional.\
Example:
```
Source: https://example.com/decklist
```

2. The "Pokémon" section contains the number of Pokémon cards in the deck, followed by each card with its quantity
    - The first line looks like `Pokémon: <num>`
    - All following lines look like `<quantity> <card name> <set name> <set number>`\
Example:
```
Pokémon: 12
3 Dragapult ex TWM 130
2 Duskull PRE 35
2 Dusclops PRE 36
1 Dusknoir PRE 37
...
```

3. The "Trainer" section is nearly identical to the "Pokémon" section. It contains the total number of Trainer cards in the deck followed by the quantities and names of each card.
    - The first line looks like `Trainer: <num>`
    - All following lines look like `<quantity> <card name> <set name> <set number>`
Example:
```
Trainer: 33
4 Iono PAL 185
2 Professor's Research JTG 155
2 Arven OBF 186
2 Boss's Orders PAL 172
...
```
4. The "Energy" section is nearly identical to the "Pokémon" and "Trainer" sections. It contains the total number of Energy cards in the deck followed by the quantities and names of each card.
    - The first line looks like `Energy: <num>`
    - All following lines look like `<quantity> <card name> <set name> <set number>`
Example:
```
Energy: 7
3 Luminous Energy PAL 191
2 Psychic Energy SVE 13
2 Fire Energy SVE 10
```
For all sections containing cards, the total number of cards in the section should add up to exactly the number in the section heading.

The total number of cards in the entire deck must equal exactly 60.

Examples of valid input files can be found in the `examples/` directory in this repository.

# Running the Program

To run the program, open a terminal window and run `python3 <path to src/deck_diff.py> <path to deck file 1> <path to deck file 2>`. The terminal should then output the cards that should be removed from deck 1 and added to the new deck to get to an exact copy of deck 2.

## Example Usage

This example demonstrates the program being run with the decks used by Tanner Hurley (3rd place) and Andrew Hedrick (2nd place) at the Atlanta Regional 2025. Both decks are variants on Dragapult ex. 
This output shows what needs to change from Tanner Hurley's deck to get to Andrew Hedrick's deck. 

GitHub's Markdown parser does not support custom text colors. The real output highlights all removals in red and all additions in green, but that unfortunately cannot be shown here.

$ python3 src/deck_diff.py examples/hurley-atlanta.deck examples/hedrick-atlanta.deck \
<span style="color:red">-hurley-atlanta.deck</span>\
<span style="color:green">+hedrick-atlanta.deck</span>

Pokémon: <span style="color:red">-2</span> <span style="color:green">+6</span>\
<span style="color:red">-1 Munkidori TWM 95\
-1 Genesect SFA 40</span>\
<span style="color:green">+1 Dragapult ex TWM 130\
+2 Duskull PRE 35\
+2 Dusclops PRE 36\
+1 Dusknoir PRE 37</span>

Trainer: <span style="color:red">-9</span> +6\
<span style="color:red">-2 Arven OBF 186\
-1 Nest Ball SVI 181\
-1 Energy Search SVI 172\
-1 Bravery Charm PAL 173\
-1 Defiance Band SVI 169\
-1 Exp. Share SVI 174\
-2 Artazon PAL 171</span>\
<span style="color:green">+2 Jacq SVI 175\
+1 Night Stretcher SFA 61\
+1 Earthen Vessel PAR 163\
+1 Rare Candy SVI 191\
+1 Luxurious Cape PAR 166 </span>

Energy: <span style="color:red">-3</span> <span style="color:green">+2</span>\
<span style="color:red">-3 Luminous Energy PAL 191</span>\
<span style="color:green">+1 Psychic Energy SVE 13\
+1 Fire Energy SVE 10</span>

Total Difference: 14 Cards

## Output Format
The output begins by indicating which deck we are removing cards from and which deck we are adding cards from with the lines:\
<span style="color:red">-deck_1</span>\
<span style="color:green">+deck_2</span>

Then, there is a short snippet of how many cards are removed from a category, followed by how many are added. For example:\
Pokémon: <span style="color:red">-2</span> <span style="color:green">+6</span>\
This indicates that 2 Pokémon cards are removed from deck 1, and 6 are added from deck 2.\
The Trainer and Energy categories get the same summary on their heading.

This is followed by a summary of the quantities of each individual card removed, and then the same for each individual card added:\
<span style="color:red">-1 Munkidori TWM 95</span>\
<span style="color:green">+1 Dragapult ex TWM 130</span>\
This indicates that 1 Munkidori from the Twilight Masquerade (TWM) set is removed, and 1 Dragapult ex from the TWM set is added.\
The Trainer and Energy sections also get the same summary of each card difference for their section.

Finally, a summary line is printed that summarizes the total difference in the deck:\
Total Difference: 14 Cards\
This indicates that 14 cards were replaced in deck 1 to get to deck 2.

# Other Notes

- This program ignores the rarity of all cards. If the set number for a card on the output is different than expected, this is normal behavior. 
- This program ignores the set IDs and rarities of all basic energy and trainer cards. If a basic energy or trainer card is listed from a different set or with different rarity than expected, this is normal behavior. 

# Reporting Bugs

Please report any bugs you may encounter to Peter Fowles (foul.in.basket@gmail.com). 