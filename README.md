# Obsidian Auto-Linker

Automatically creates `[[wikilinks]]` between notes in your Obsidian vault. No plugins needed — just a Python script.

## The Problem

Obsidian Graph View only shows connections between notes that explicitly link to each other with `[[wikilinks]]`. If you imported notes from Apple Notes, Notion, Evernote, or anywhere else, your graph is a sea of disconnected dots.

## The Solution

This script scans every note in your vault, checks if any other note title is mentioned in the body text, and wraps the first occurrence in `[[wikilinks]]`. Your Graph View lights up instantly.

## Usage

```bash
python3 obsidian_auto_linker.py /path/to/your/vault
```

Or just run it with the default path (`~/Documents/Obsidian Vault`):

```bash
python3 obsidian_auto_linker.py
```

## How It Works

1. Collects all `.md` note titles in your vault
2. For each note, checks if any other note title appears in its body
3. Wraps the first match in `[[wikilinks]]` (skips if already linked)
4. Preserves YAML frontmatter — only modifies the body
5. Processes longest titles first to avoid partial matches

## Safety

- Only modifies the first occurrence per note (not aggressive)
- Skips very short titles (<=5 chars) to avoid false positives
- Skips system files (Dashboard, MOC, Home)
- Preserves frontmatter completely
- Case-insensitive matching with word boundaries
- No dependencies — pure Python 3

## Example Output

```
Scanning vault: /Users/you/Documents/Obsidian Vault

Found 1389 notes
Linkable note titles: 1200

  + 1 links in: Product Roadmap
  + 2 links in: Weekly Review 2026-03-10
  + 1 links in: Meeting with Investors

Done! Added 25 links across 17 files.
Open Graph View (Cmd+G) in Obsidian to see your connections.
```

## Pro Tips

- Run it weekly with a cron job to keep your graph growing
- Works great after importing notes from Apple Notes, Notion, or Evernote
- Pair with the Dataview plugin for auto-generated dashboards

## License

MIT — free to use, share, modify.

---

Built with Claude. If this helped you, star the repo and share it.
