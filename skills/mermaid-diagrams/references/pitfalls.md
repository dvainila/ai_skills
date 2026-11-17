# Mermaid pitfalls

Read before emitting a fence. These break GitHub/preview more often than “wrong type”.

## Ids and labels

- Node/subgraph/participant **ids**: `[A-Za-z][A-Za-z0-9_]*`. No spaces, no dashes in flowchart ids (`api_server` not `api-server` or `api server`).
- Text with spaces, `()`, `/`, `:`, `#` belongs in quotes: `A["POST /login"]`, `search["search()"]`.
- Do not use as ids: `end`, `graph`, `subgraph`, `class`, `click`, `style`, `end`.

## Flowchart

- `flowchart` not `graph` (legacy).
- Subgraph: `subgraph mod_id [Label]` then `end`. Every `subgraph` needs `end`.
- Nested subgraphs: close inner first.
- Edges must use **ids**, not labels: `mod_id --> db_id`.
- HTML break is `<br/>` inside a quoted label, not a real newline.
- Extra parent subgraphs: edges from outside route **around** the parent box — do not wrap a cluster that other islands call into.
- `classDef` names: letters/digits/underscore, no dashes. Do not name a class the same as a node id (`class api api`).
- `class a,b roleName` must list the subgraph **and** its nodes; subgraph fill does not color children.

## Class diagrams

- `namespace name { ... }` — braces must close.
- Relationship line **between** names, not inside the class body.
- `<<module>>` / `<<service>>` / `<<database>>` on their own line inside the class.

## Sequence

- `alt` / `opt` / `loop` / `par` / `rect` / `box` each need `end`.
- `par` branches use `and`, not `else`.
- Participant aliases: `participant API as FastAPI` — messages still say `API`.

## ERD

- Cardinality is on **both** sides: `USER ||--o{ ORDER : places`.
- Attribute comments in double quotes; no nested `"`.

## Architecture

- `architecture-beta` is optional and often missing in GitHub. Prefer `flowchart`.
- Declare group/service ids before any edge. Edges: `api:R --> L:db`.

## Config

- Skip `handDrawn`, `elk`, and custom `themeVariables` unless asked — they fail in some renderers.
- `%%` comments are whole-line only.
