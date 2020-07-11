# Laureat of Discord ⚡

Be the smartest guy on discord !

Laureat of discord aim to be able to recreate the Baccalaureat game fro your childhood directly into discord.

The rule are simple you choose some category ex : **Name, Animal, Contry** and a random letter here **P**.

now you have to find words matching all category as fast as possible !

ex :
| Letter/Category | Name | Animal | Contry |
| :-: | :-: | :-: | :-: |
| P | Perdo | Peacock | Portugal |

If someone finish the round end.
The score is calculated by how many people have the same word ->
- Unique 2pts
- At least 2 players 1pts
- All players 0 pts

At the end of the round the player with most point win !

here are the avalible command for now (all command have to be prepend by a '!'):
| Command | Usage |
| :-: | :-: |
| baccalaureat n categories | create a session, n is the number of round, categories are the categories you want to play with ex : !baccalaureat 5 Name Animal Contry |
| start | start te game with players that joined in |
| cancel | delete the session of the session owner |

When the session as started you have to play in dm with the bot, you will see a board with the first letter and the categories.
To put word in categories you have to put the numer of the categories followes by your word.
in the example Animal is the 2nd categories so send "2 Peacock" to the bot will fill the board with Peacock in category Animal.

That's how you play !

In the future i want to add a dictionnary for common categories, a better way to enter word in category and a timeout to round.

Dependencies : [Discord.py](https://discordpy.readthedocs.io/en/latest/)

You can easily change the language by editing the text.py file