# Color and readability

Always apply this file for flowcharts. Sequence and ERD: skip `classDef`; sequence may use `box` around participants.

Default look stays classic / dagre / no `handDrawn`. Color comes from **`classDef`**, not from a custom theme.

## Color by role

One `classDef` per **role**, not per node. Light fill, darker stroke, matching `color:` for text.

| Role | `classDef` | fill | stroke | text |
| --- | --- | --- | --- | --- |
| UI / browser | `browser` | `#E3F2FD` | `#1565C0` | `#0D47A1` |
| HTTP / API | `http` | `#FFF3E0` | `#EF6C00` | `#E65100` |
| Domain / pipeline | `domain` | `#F3E5F5` | `#7B1FA2` | `#4A148C` |
| Process A | `procA` | `#E0F7FA` | `#00838F` | `#006064` |
| Process B | `procB` | `#FCE4EC` | `#C2185B` | `#880E4F` |
| Process C | `procC` | `#FFF8E1` | `#F9A825` | `#F57F17` |
| Store / DB / model | `store` | `#E8F5E9` | `#2E7D32` | `#1B5E20` |

Reuse these hex values. Rename the class if a node id would collide (`class api api` is bad if subgraph id is `api` — use `http`).

Rules:

- Distinct processes (separate ports, compose services) get **distinct** classes.
- Nested modules of **one** process share one class.
- Database, files-as-DB, and the model box use `store`. A local JSON file inside an isolated process stays that process’s class, not `store`.
- Apply `class id1,id2 Name` to the **subgraph id and every inner node**. Subgraph fill does not color children.
- Caption (one line): what the colors mean, if more than two classes.
- No `style NodeId …`. No `linkStyle`. No one-off rainbow fills.

```
classDef browser fill:#E3F2FD,stroke:#1565C0,color:#0D47A1
classDef http fill:#FFF3E0,stroke:#EF6C00,color:#E65100
classDef store fill:#E8F5E9,stroke:#2E7D32,color:#1B5E20
class spa,useAuthMe browser
class api,handler http
class db,model store
```

Error-only accent (keep rare): `fill:#fde8e8,stroke:#c0392b`.

## Layout that stays readable

- **Pipeline of calls:** outer `flowchart LR`. **Containment:** `direction TB` inside a module subgraph.
- **Edge labels:** short, only facts not already in the node name. Drop `cookie /auth/*` if the target is already `/auth/*`.
- **No extra parent subgraph** around a cluster that other islands point into. Mermaid routes those edges **around the whole box**.
- **Orphans:** a subgraph with no edges looks like a mistake. Give it an internal node, or park it with `A ~~~ B` next to a related island — not in empty space on the opposite side of a long edge.
- **Parallel arrows:** `A --> B & C` / `A & B --> C` instead of two identical labeled edges.
- **Dense flowcharts:** front matter is OK:

```
---
config:
  flowchart:
    curve: basis
    nodeSpacing: 24
    rankSpacing: 36
    padding: 8
---
```

Do not add `layout: elk`, `handDrawn`, or `themeVariables` unless the user asks.

## Anti-patterns

- TB stack of many module boxes with long labeled edges (unreadable).
- Wrapping Web+API in `subgraph app` while Worker still points at API.
- Coloring every node a different hex with `style`.
- Leaving an isolated process box floating far from the others.
