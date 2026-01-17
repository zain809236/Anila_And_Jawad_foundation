Local fonts for offline use
===========================

This folder holds fonts downloaded for offline usage by the site.

Files:
- `archivo-black.woff2` — Archivo Black (downloaded via script)
- `quattrocento-regular.woff2` — Quattrocento regular (downloaded via script)
- `fonts.css` — @font-face rules referencing the files above

To download the font files automatically, run the script from the project root:

PowerShell (Windows):

```powershell
cd <project-root>
.\scripts\download-fonts.ps1
```

After running, open a `src/*.html` file in the browser; the pages already
reference `../assets/fonts/fonts.css` so the fonts should load locally.

If you also want Font Awesome self-hosted, tell me and I'll add a similar
script and local CSS to fetch and wire it up.
