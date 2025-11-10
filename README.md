# Irondale Brewing — README

Website for Irondale Brewing (https://irondalebrewing.com) built with [Pelican static site generator](https://getpelican.com/) and the [Pagefind](https://pagefind.app/) search library.

This was originally a WordPress site. Migrating the site was a great way to learn Pelican and more about static site generators overall.

The site is hosted on [Firebase](https://firebase.google.com).

## Build and Run the Site Locally

1. Install Python
1. Install npm
1. `pip install -r ./requirements.txt`
1. `npm install -g pagefind`
1. `pelican content`
1. `npx pagefind --site output`
1. `cd output`
1. `python -m http.server 8000`

You can then browse the site locally at http://localhost:8000/

# Pagefind Customization

## Summary

The theme integrates Pagefind (client-side search). During testing, the search overlay's results grew past the bottom of the viewport and the "Load more results" button was flush to the bottom. The repository contains two small, compatible changes that address the issue:

1. Host-level CSS (in the theme) to allow the overlay to scroll and ensure flex children can overflow internally.
2. Minimal Pagefind initialization and a small runtime helper in `themes/irondale-brewing/templates/base.html` to ensure the internal results area and buttons have bottom spacing in all rendering modes (light DOM or shadow DOM).

These changes were intentionally kept small and defensive to avoid brittle edits to generated Pagefind assets.

## Files of interest

- `themes/irondale-brewing/static/css/main.css`
  - Host-level layout fixes: overlay `overflow-y: auto`, `.pagefind-ui` set to `display:flex`/`flex-direction:column`, `min-height:0`, `max-height:calc(100vh - 100px)`, and `padding-bottom`. These ensure the overlay container can scroll and permit its children to overflow appropriately.

- `themes/irondale-brewing/templates/base.html`
  - Minimal `new PagefindUI({...})` initialization with small injected styles for `bundle`, `form`, and `results`.
  - `results` injection contains `flex-grow:1; overflow-y:auto; min-height:0; padding-bottom:40px;` which helps internal scrollability and adds a default bottom gap.
  - A compact runtime helper is added to handle edge cases where Pagefind renders differently or re-renders:
    - `applyPagefindBottomSpacing()` — applies inline styles (`padding-bottom` to `.pagefind-ui__results-area`, `margin-bottom` to `.pagefind-ui__button`) in both light DOM and shadow DOM.
    - `observePagefindContainer()` — installs a `MutationObserver` on `#pagefind-search-container` (and the Pagefind `shadowRoot` when present) to re-apply the spacing whenever Pagefind re-renders.
    - The helper is called on `DOMContentLoaded` and when the overlay is opened.

- `output/pagefind/pagefind-ui.css` (generated)
  - This file contains Pagefind's build-time CSS. It is not edited in source. Editing generated files is brittle — prefer the small injected styles + runtime helper implemented above.

## Why this approach

- Pagefind may render inside a shadowRoot (custom element) or into the light DOM depending on the build and runtime environment. That makes a single static CSS override brittle.
- A minimal injected `results` style plus an equally small runtime fallback (which applies inline styles when needed) is resilient across those rendering modes and across re-renders.
- Avoid direct edits to generated `output/pagefind/pagefind-ui.css` because those can be overwritten and make upstream updates harder.

## How it works (high level)

- The Pagefind UI is initialized with `new PagefindUI(...)`. The `styles` option injects small CSS for the component (bundle/form/results).
- If Pagefind renders into light DOM, the runtime helper finds `.pagefind-ui__results-area` and applies `padding-bottom` inline.
- If Pagefind renders into a `pagefind-ui` element with an open `shadowRoot`, the helper will find the shadowRoot and apply equivalent inline styles to its internal elements.
- A `MutationObserver` watches `#pagefind-search-container` (and the shadowRoot), so if Pagefind re-renders (for example after clicking "Load more results"), the helper will re-apply the spacing.

## Tweakable values

If you want to change how much breathing room appears below the results / button, edit one or more of these places:

- `themes/irondale-brewing/templates/base.html` — the `results` injected style currently contains `padding-bottom:40px;`. You can increase/decrease that value.

- The runtime helper `applyPagefindBottomSpacing()` applies `48px` to `.pagefind-ui__results-area` and `12px` to `.pagefind-ui__button`. If you prefer a different amount, update those inline style values.

Note: If you change only the injected `results` style, the runtime helper may still apply its own inline values (if it runs) and override your CSS. To keep a single source of truth, make consistent updates to both places or remove the runtime helper (not recommended).

## Testing locally

Rebuild your site and open a page with the overlay in a browser. Then:

1. Open the search overlay.
2. Repeatedly click "Load more results" until results grow past the viewport.
3. Confirm the overlay scrolls and the "Load more results" button has space below it (not flush to the viewport bottom).

Typical commands (run in repository root; use the command that matches your environment):

```powershell
# If you use make
make html

# Or directly with pelican
pelican content -o output -s pelicanconf.py
```

Then open files from `output/` in your browser or use your local static server preview.

## Alternatives (if you want stronger guarantees)

- Shadow-root style injector: Append a small `<style>` element directly into `pagefind-ui`'s open `shadowRoot`. This is fairly robust but is runtime injection into third-party DOM and should be used sparingly. The project previously had a slightly larger injector; we removed it in favor of the minimal helper.

- Edit generated `output/pagefind/pagefind-ui.css`: Works but is brittle — you'll need to re-apply changes when regenerating the pagefind build or when updating packages.

- Keep more comprehensive runtime fallbacks: If your environment produces inconsistent behavior across browsers or Pagefind versions, a more comprehensive fallback (spacer node + retrying injection + observers) can be added.