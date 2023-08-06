# plover_cards

A Plover plugin which helps you build an Anki deck from the words and phrases you have typed.

This plugin might not work perfectly, so you may want to double check the cards before you add them.

![screenshot of card builder window](https://user-images.githubusercontent.com/3298461/112348383-afbd6800-8cbf-11eb-8de7-8b6d48fe85f6.png)

## Plover Cards Hook

This part of the plugin listens to what you write and records the suggestions (you don't need to have the suggestion window open). It'll keep a count of how many times you use a stroke so you can focus on only the words you use often (or least often). Unlike the suggestions window, it'll also record suggestions for command, prefix and suffix strokes if you use them.

The data is stored in `{your_plover_config_folder}/plover_cards/card_suggestions.pickle`. This gets saved when you disable the extension, quit Plover and every 5 minutes.

### Using the hook

- Enable the plugin
  - Right click the Plover icon, "Configure", "Plugins" tab, check the box next to "plover_cards_hook", "Apply"

## Card Builder

### Before you start
- Set up Anki
  - Make an Anki collection
  - Make a note type for your steno cards (it can be the default "Basic" type, but if you want to use Anki for anything else as well then you should make a new note type)
- Use Plover and type some words that aren't in Anki
- Start the card builder
  - Make sure Anki isn't already running
  - Right click the Plover icon, "Tools", "Card Builder"

### Set Options

| Option                            | What it's used for                                                                                                                                                                                                  |
| --------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Anki Collection                   | The Anki collection with existing cards, which will be ignored when building cards. Defaults to the first `.anki2` file it can find in the [default Anki  path](https://apps.ankiweb.net/docs/manual20.html#files). |
| Note Type                         | The note type for existing cards, which will be ignored when building cards. Defaults to "Basic".                                                                                                                   |
| Ignore File                       | Where to save the list of words to ignore. Defaults to `{your_plover_config_folder}/plover_cards/ignore.txt`.                                                                                                       |
| Output File                       | Where to save the CSV file of new cards, which can then be imported into Anki. Defaults to `{your_plover_config_folder}/plover_cards/new_notes.txt`.                                                                |
| Clear output file before starting | Clear the output file when you press start. You'll want this on if you have imported the cards from the previous session, and off if you're continuing the previous session.                                        |

These options are saved in `{your_plover_config_folder}/plover_cards.cfg`

### Build Cards

- *Stroke list*: Pick which stroke you want on the back of the Anki card here.
- *Card list*:
  - You can click on any of the following columns to sort by that column. Click again to change the sort order.
  - *Count*: The number of times you typed this word and/or the number of times it was suggested to you.
  - *Translation*: The word or phrase on the front of the Anki card.
  - *Stroke*: The stroke on the back of the Anki card.
  - *Similar ignored*: Similar words that are either already in the Anki deck or have been added to the ignore list.
- *Buttons*:
  - **Clear**: Clear the chosen stroke. Useful if you want to skip this card, since by default it will choose the first stroke in the list.
  - **Ignore**: Add this word/phrase to the ignore list. It won't appear next time you use the card builder.
  - **<**: Go to previous card.
  - **>**: Go to next card.
  - **Finish**: Finish building cards.

### Add to Anki

In Anki go to `File` then `Import`. Select the output file you chose at the beginning (defaults to `{your_plover_config_folder}/plover_cards/new_notes.txt`).
