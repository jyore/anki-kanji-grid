# Kanji Grid Advanced

Create an interactive display of all of the Kanji from your decks with a relative strength measurement.

**Requires Anki 2.1**

Add-On homepage: https://github.com/jyore/anki-kanji-grid<br/>
Issue list: https://github.com/jyore/anki-kanji-grid/issues


Features include:
- Interactive graphical representation of your kanji knowledge
  - See what kanji you have repped and not repped that are in your decks
  - See what kanji you are missing from popular kanji sets
  - Get a relative measurement of your strength based on total exposure to the kanji
  - See useful statistics for each Kanji such as: card count, number of reviews, first & last rep dates, pass rate, and more
- Export graphics into HTML and PDF formats
- Target your grid towards only the decks you want to measure (useful for excluding sentence bank decks from results)
- Target only specific fields for each note-type (useful for not counting tag/file/url/etc references that you may not want to count)
- Customize the layout of your results and the strength measurement
- Group the grid results by popular Kanji sets
  - JLPT
  - RTK
  - Grade Level
  - Jouyou & Jinmeiyou
  - None (Get a single printout for all Kanji, without being grouped)


Based on the original Kanji grid add-on and its various forks.
- https://ankiweb.net/shared/info/1990160569 (no longer available)
- https://ankiweb.net/shared/info/942570791
- https://ankiweb.net/shared/info/1690856263
- https://ankiweb.net/shared/info/1940609130



## Installation

Install the add-on by using the anki browser or by downloading a release from the releases page and extracting the directory to the addons21 folder.



## Configuration

To configure the add-on, open the Anki Add-on Menu via `Tools->Add-ons` and highlighting `Kanji Grid Advanced`. Then click the `Config` button on the right-side of the screen. This will bring up an interface that will allow you to configure how the add-on will work.

![Configuration Menu][conf-menu]

* Select which decks to scan in the left-hand box [default: all-on, except for Default deck]
* Browse the available note-types and select which fields to scan for each [default: all-on]
* Set the number of characters that will show up in each row of the grid (columns) [default: 40]
* Set the number of reviews to indicate what you believe to be strong [default: 500]

Once you are finished configuring the add-on, select `ok` to save the changes.


## Running

To run the add-on and view your grid, start by selecting `Tools->Generate Kanji Grid` from the Anki menu bar. This will generate a small interface that will ask you to select how you'd like your results to be grouped.

![Group-By Menu][group-menu]

* JLPT: Groupss the results by JLPT Kanji sets N5-N1
* Grade Levels: Groups the results by Grade levels
* RTK: Groups the results based on RTK 1 and RTK 3 Kanji sets
* Jouyou & Jinmeiyou Kanji: Groups the results into Jouyou and Jinmeiyou Kanji
* None: Will display one large grid of Kanji without grouping the results at all


After selecting how to group your results, select `ok` to generate the grid.
![Kanji Grid][grid]

Above the Kanji display, it will list the number of Kanji you have cards for out of the total count for the set, along with the percent complete. Below the kanji list, a smaller grid can be expanded via a drop-down that shows all Kanji from the set that you do not have cards for:
![Kanji Grid][grid-with-missing]

When viewing the grid, you can hover over any Kanji to view stats related to your reviews of that character. You may also click the character to bring up the Jisho details on that specific character.
![Tool Tip][tooltip]

Finally, you may choose to export the results into an HTML document or into a PDF file by using the export buttons at the bottom of the grid view.
![Export][export]


[conf-menu]: https://user-images.githubusercontent.com/904738/50525132-3febb300-0a9f-11e9-8cc8-bef59a926e04.png
[group-menu]: https://user-images.githubusercontent.com/904738/50525133-3febb300-0a9f-11e9-9d08-7de1733b54d2.png
[grid]: https://user-images.githubusercontent.com/904738/50525134-40844980-0a9f-11e9-846c-4ea89829e707.png
[grid-with-missing]: https://user-images.githubusercontent.com/904738/50527298-0f127a80-0aad-11e9-9243-c6d4eccc24c6.png
[tooltip]: https://user-images.githubusercontent.com/904738/50525136-40844980-0a9f-11e9-847a-5373037ba6f7.png
[export]: https://user-images.githubusercontent.com/904738/50525524-86421180-0aa1-11e9-9018-dad8e7e4af47.png
