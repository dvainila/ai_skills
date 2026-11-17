---
name: mermaid-diagrams
description: >-
  Build and edit Mermaid diagrams: flowchart, class, sequence, ERD, and
  architecture-beta. Covers syntax, visual language, role colors (classDef),
  readable layout, pitfalls, and validation. Use when the user asks to draw,
  edit, or fix a Mermaid diagram, flowchart, class diagram, sequence diagram,
  ERD, or schema picture. Do not use for pie, Gantt, or git graphs unless the
  user names that type.
---

# Mermaid diagrams

Construct and edit Mermaid diagrams. This skill is syntax, visual language, and quality — not a repository walkthrough.

## Workflow

1. If **editing** an existing fence, keep node ids; change only the requested layer. Color and layout still follow [references/readability.md](references/readability.md) unless the user asked to strip them.
2. Else **create**: pick one type → read that type's reference + [references/pitfalls.md](references/pitfalls.md) + [references/readability.md](references/readability.md) → source names from code → draw (colored, readable) → quality gate → validate.

Default: classic look, dagre, no `handDrawn`. Flowcharts are **colored by role** (`classDef`) and laid out for reading — not gray boxes. Read [references/advanced-features.md](references/advanced-features.md) only for ELK, `handDrawn`, or custom `themeVariables`.

## Pick a type

One type per diagram. Default for structure and wiring: `flowchart` (GitHub-safe).

| Need | Type | Reference |
| --- | --- | --- |
| Nesting, calls, services, DB | `flowchart` | [references/flowcharts.md](references/flowcharts.md) |
| Types, methods, module namespaces | `classDiagram` | [references/class-diagrams.md](references/class-diagrams.md) |
| Time-ordered messages | `sequenceDiagram` | [references/sequence-diagrams.md](references/sequence-diagrams.md) |
| Tables and keys | `erDiagram` | [references/erd-diagrams.md](references/erd-diagrams.md) |
| Runtime processes and DBs | `architecture-beta` | [references/architecture-diagrams.md](references/architecture-diagrams.md) |

`architecture-beta` often fails on GitHub — prefer `flowchart` with `[(db)]`. `stateDiagram-v2` / `gitGraph` / `gantt` / `pie` only when the user asks for that type.

## Visual language

Use this set only:

| Thing | How |
| --- | --- |
| Module | subgraph or `<<module>>` |
| Class | `id[ClassName]` or `class` |
| Function | `id["name()"]` |
| Service / process | `id(service)` or `<<service>>` |
| Database | `id[(name)]` or `<<database>>` |
| Contains | subgraph / `namespace` / `*--` |
| Calls | `-->` |
| Depends | `-.->` or `..>` |
| Persists | `-->` into a cylinder |

Containment: `TB`. Peer calls: `LR`. Color by **role** with named `classDef` (palette in [references/readability.md](references/readability.md)): distinct processes get distinct classes; one process shares a class; DB / model use `store`. Apply the class to the subgraph **and** its nodes.

## Source pass

Read the files you are drawing. Use real names. If a node is guessed, mark `%% inferred`. Do not invent modules, tables, or calls.

## Limits

- One question per diagram.
- ≤ 15 nodes.
- Prefer top-N plus `other["… +N"]` over dumping a package.
- Private helpers stay off the diagram unless they are the topic.

## Quality gate

Do not emit until all hold:

- [ ] Type matches the question
- [ ] Ids have no spaces; labels with `/():` are quoted
- [ ] Edges are contains, calls, or persists — not a mix without grouping
- [ ] Names match code
- [ ] Flowchart: role `classDef` on subgraphs and inner nodes; caption says what color means if >2 classes
- [ ] Readable: `LR` for call pipelines; short edge labels; no parent box that incoming edges must wrap around; no orphan islands
- [ ] Read [references/pitfalls.md](references/pitfalls.md) and [references/readability.md](references/readability.md)
- [ ] `python skills/mermaid-diagrams/scripts/validate.py <file>` (or this skill’s `scripts/validate.py`) passes when the diagram is in a file — local heuristic only, not a renderer

## Output

- Chat: one fenced `mermaid` block. Caption above it: what the diagram is, plus what colors mean if there are more than two classes.
- Persist only if asked. When writing a new file:
  1. If the user already named a path, use it.
  2. Else if a `docs/` directory exists at the repo root, put a `.mmd` or Markdown file under `docs/`.
  3. Else ask where to put the files before creating a folder.
- Do not copy the same diagram into multiple READMEs.

## Edit existing

1. Locate the fence or `.mmd`.
2. Reuse ids, subgraph names, and edge labels.
3. Patch the requested layer only (add a node, fix an edge, rename). If the fence is still uncolored, add role `classDef` as part of the same edit.
4. Re-run the quality gate and validator.
