# mtpkg

`mtpkg` is a command-line package manager for [Minetest](https://minetest.net).

It can:

- Install the latest compatible releases for a given set of ContentDB packages
  - Recursively install dependencies for requested packages given a base game
  - Enable the installed mods on an existing world
- Update installed ContentDB packages to their latest compatible releases

## Getting Started

```
$ python3 -m venv mtpkg-venv
$ source mtpkg-venv/bin/activate
(mtpkg-venv) $ pip install mtpkg
(mtpkg-venv) $ mtpkg -h
(mtpkg-venv) $ mtpkg -u ~/.minetest install --game Minetest/minetest_game TenPlus1/mobs
```

## Frequently Asked Questions (FAQs)

### Why is it so slow for large numbers of packages?

`mtpkg` tries to be polite by rate-limiting requests to the ContentDB, which
makes looking up a large number of packages take a long time. Even more so if
their dependencies need to be recursively queried.

