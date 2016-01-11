Guckenheimer Corporate Dining Menu Fetcher [![Build Status](https://travis-ci.org/AndrewX192/guckenheimer-menu-fetcher.svg?branch=master)](https://travis-ci.org/AndrewX192/guckenheimer-menu-fetcher)
==============

System to retrieve weekly food menu from Guckenheimer Corporate Dining

Example
---
````
>>> from menu import GuckenheimerMenu
>>> menu = GuckenheimerMenu('twitterseattle')
>>> menu.get_menu('breakfast', day=5)
'Breakfast Burritos with Cage Free Eggs, Potatoes, Cheddar Cheese & Bacon or Roasted Vegetables'
````