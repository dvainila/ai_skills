---
name: write-clean-comment
description: Write or rewrite code comments and docstrings so they are brief, clear, and precise. Use when adding comments, shortening comments, editing docstrings, reviewing comment style, or when the user mentions comments, комментарии, or write-clean-comment.
---

# Write clean comments

Follow this whenever you write or change a comment (`#`, `//`) or a docstring.

## Rule

Prefer **one line**. Use a **second line** when the idea is actually two things (the contract and the trap) — do not cram both into one dense sentence. A **third line** is allowed only when there is a real extra constraint that will not fit on two; never more than three.

Do not restate the code, add history, or link to files the reader can already see. Write only what is easy to get wrong.

## Good

```
# Sentinel for every id. Empty tuple means no access — never confuse the two.
ALLOWED_IDS: tuple[str, ...] = ("*",)
```

```
# Defaulted: old payloads lack this field; without it, every request looks signed out.
role: UserRole = Field(default="guest")
```

Two ideas → two lines:

```
"""SQL filter: None = unrestricted, [] = no rows (AND false).
Separate from path_filters — empty there means include every path, not deny."""
```

## Bad

```
# SQL filter: None=unrestricted, []=deny (AND false); unlike path_filters where empty means include every path.
```

Readable facts, unreadable comment — split it instead of packing the one-line preference.
