![Python package](https://github.com/jwizzle/nerdchess/workflows/Python%20package/badge.svg?branch=master)

# NerdChess

A chess engine written in Python.

[They might not be 100% complete yet, but see the docs for implementation details](https://nerdchess.readthedocs.io/en/latest/index.html)

The goal of this project is to offer simple tools to simulate a game of chess, by offering the necessary objects like a board, pieces, pawns and players standalone. But also a complete chessgame that implements these objects and offers an interface to control the game.
The package includes a small commandline chess game, but the main goal is to offer an interface to create chess games from everywhere. It should be just as easy to implement the same games of chess in a web-application with Flask, a commandline interface or some graphical desktop interface.

It's still the idea to make it possible to write AI's againt this package. But for now I'm just going to finish it's basic functionality and try to keep it in mind as much as I can while making design decisions.
I'm not aiming for this to be some widely used package, and am mostly making it for fun and learning. Expect things to change a lot, and your applications to break if you don't freeze versions might you decide to use this. At least in it's current state.

## TODO
* Start seperate project for a more complete TUI chessgame implementing this package
