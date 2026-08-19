# field notes

a local reference notebook for designers. drop travel photos in, and each one
gets a name, a palette, and material tags — then files itself into the trip it
came from. everything lives in your browser. no account, no cloud, no install.

the whole app is **one HTML file**.

<p align="center">
  <img src="docs/screenshot-grid.png" alt="the library grid" width="100%">
</p>
<p align="center">
  <img src="docs/screenshot-zine.jpg" alt="printed mini-zines, folded and cut" width="70%">
  <br>
  <em>references, folded into single-sheet mini-zines</em>
</p>

> 🎬 **watch the 60-second demo:** [instagram reel →](https://www.instagram.com/p/DZKyrzPiPD6/)

---

## what it does

- **drop a photo, get a card.** each image gets a short name, a one-line
  description, an accurate hex palette, and the materials it shows.
- **sorts itself by trip.** location + date are read straight from the photo's
  EXIF (GPS → city), so shots file into "Antwerp", "Tokyo", etc. automatically.
- **prints to a zine.** select a few cards and fold them into a single-sheet
  mini-zine (one cut) or a saddle-stitch booklet, ready for the printer.

## how it works

this is a single-file port of the original local Node app. the interface is
unchanged; the server, macOS tools, and on-disk library are now in the browser.

- **one file.** `index.html` is the entire product — fonts, demo photos, UI, and
  logic. open it. there is nothing to install.
- **tagging.** if you paste an Anthropic API key in **settings**, each new photo
  is sent to Claude from your browser (same JSON record as before: name, palette,
  materials). without a key, the app still works: it samples a four-colour
  palette locally, names the file, and files the trip from EXIF.
- **image work** is all in-page: canvas for downscaling / HEIC (when the browser
  can decode it), and a JPEG EXIF reader for GPS + capture date.
- **persistence** is IndexedDB on this device. export / import a JSON backup from
  settings whenever you want a file you can copy or commit.

## why i built it

i come back from every trip with a camera roll full of the same kinds of things:
a wall, a doorway, a stack of tiles, the exact orange of a café sign. references.
the problem was never taking them — it was everything after. they'd sit in my phone,
unsorted and unnamed, and by the time i wanted one i couldn't find it. pinterest felt
like someone else's feed; a folder of photos felt like a junk drawer.

so i built the tool i actually wanted: drop a photo in and it gets a name, a palette,
and the materials it's made of, then files itself by the trip it came from — no tagging,
no accounts. it started in antwerp during design week, where i was photographing more
than i could keep track of, and grew from there.

this edition takes that same notebook and folds the server into the page, so it
runs anywhere a browser does.

## setup

> **before you start, you need:**
> 1. **a browser** — any current Chrome, Firefox, Safari, or Edge
> 2. *(optional)* an **Anthropic API key** if you want Claude to name and tag
>    photos ([get one](https://console.anthropic.com)). without it, drops still
>    file by trip and get a local palette.

```bash
# open the file
open index.html          # macOS
xdg-open index.html      # linux
start index.html         # windows
```

or serve the folder (useful if a `file://` page blocks the anthropic call):

```bash
python3 -m http.server 4317
# then open http://localhost:4317
```

a fresh open starts with a few demo reference photos so the grid isn't empty.

**image analysis:**

1. **local (default).** palette is sampled from the pixels; the trip comes from
   EXIF. nothing leaves the machine.
2. **claude (optional).** open **settings**, paste `ANTHROPIC_API_KEY`, and new
   drops (or **look again** on a card) use the same vision prompt as the original
   app. the key is stored only in this browser.

## tech stack

- one self-contained HTML file — no framework, no build step to *run*
- vanilla JS + CSS (EB Garamond + Inter, embedded)
- IndexedDB for the library, canvas for image work, JPEG EXIF for trips
- optional Claude analysis via the Anthropic API (browser CORS header)
- printable zines (pages, PocketMod mini-zine, saddle-stitch booklet)

## project layout

```
field-notes/
  index.html              the whole app — open this
  field-notes.src.html    source before fonts/photos are inlined
  build-single-file.py    regenerates index.html
  samples/                demo photos the first run seeds from
  fonts/                  EB Garamond + Inter (embedded into the html)
  server.js               original Node edition (no longer required)
```

rebuild the single file after editing the source:

```bash
python3 build-single-file.py
```

## what i'd do next

a running list, roughly in order of how much i want them:

- group by material or colour across trips, not just by location
- a "palette from a whole trip" view — the dominant colours of antwerp vs tokyo
- export a trip as a single shareable page or PDF, not only a printed zine
- let two photos sit side by side to compare materials directly

## credits

built with [Claude](https://claude.com/claude-code). started during, and inspired
by, **Antwerp Design Week**.

by **Laurence Mac Donald** — [@by.laurence on instagram](https://instagram.com/by.laurence).

## license

[MIT](LICENSE) © Laurence Mac Donald
