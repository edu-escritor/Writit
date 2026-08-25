# Project Structure and File Naming Convention

This document defines the directory structure and file naming conventions used for writing projects.

A project may be divided into **parts**, or it may have **no parts at all**. The directory structure and file naming convention differ slightly between these two cases.

---

## 1. Common Project Structure

Every project contains, at its root:

```text
master.rst
meta/
```

Example:

```text
.
├── master.rst
└── meta/
```

### `master.rst`

The main file of the project.

### `meta/`

Contains metadata, documentation, prompts, summaries, glossaries, and other auxiliary files related to the project.

For example:

```text
meta/
├── glossario.rst
├── micro.md
├── prompt-microfasica.md
├── prompt-revisao.md
└── resumo.md
```

Files inside `meta/` do **not** need to follow the chapter naming convention described below.

---

## 2. General Naming Rules

### 2.1 Slugs

Human-readable titles are converted into **slugs** when used in filenames.

Rules:

* Use lowercase characters.
* Remove accents and other diacritics.
* Replace spaces with `-`.
* Use `-` as the separator between words.
* Do not use `_` inside a slug.

Examples:

```text
Velho Novo Mundo
→ velho-novo-mundo

Mensagem Não Lida
→ mensagem-nao-lida

Open Source Intelligence
→ open-source-intelligence

Investigação Muito Importante
→ investigacao-muito-importante
```

The `_` character is reserved for separating the structural components of a filename.

---

## 3. Ordering

Content items use an explicit numeric index:

```text
i0010
i0020
i0030
i0040
...
```

The format is:

```text
i{index:04}
```

The index represents the **ordering position of the item**, not necessarily its chapter number.

Indices normally increase by 10.

This intentionally leaves room for inserting new items without renumbering existing files.

For example, a new item can be inserted between:

```text
i0030
i0040
```

using:

```text
i0035
```

or, if necessary:

```text
i0031
i0032
```

Therefore, the index should be treated as an **ordering key**, not as a chapter number displayed to the reader.

---

## 4. Versions

Each content item may have multiple versions.

Versions use the format:

```text
v001
v002
v003
...
```

Formally:

```text
v{version:03}
```

Example:

```text
i0010_v001_velho-novo-mundo.rst
i0010_v002_velho-novo-mundo.rst
i0010_v003_velho-novo-mundo.rst
```

A higher version number represents a later version of the same logical content item.

The index remains unchanged between versions.

---

# 5. Projects Without Parts

If the work is **not divided into parts**, its content files are stored inside:

```text
chapters/
```

Example:

```text
.
├── master.rst
├── meta/
│   └── ...
└── chapters/
    ├── i0010_v001_first-chapter.rst
    ├── i0020_v001_second-chapter.rst
    └── i0030_v001_third-chapter.rst
```

The filename format is:

```text
i{index:04}_v{version:03}_{slug}.rst
```

or, schematically:

```text
iIIII_vVVV_slug.rst
```

Example:

```text
i0040_v003_connection-lost.rst
```

Where:

```text
i0040             ordering index
v003              version
connection-lost   slug
.rst               file extension
```

Projects without parts **must not introduce an artificial part number**.

Therefore, avoid names such as:

```text
p000_i0010_v001_first-chapter.rst
p001_i0010_v001_first-chapter.rst
```

if the work does not actually contain parts.

Likewise, a project without parts should not use an artificial:

```text
parte_01/
```

directory merely for structural consistency.

The absence of a `pXXX` component has semantic meaning: **the work is not divided into parts**.

---

# 6. Projects With Parts

If the work is divided into parts, each part receives its own directory.

Directories use the format:

```text
parte_{part:02}
```

For example:

```text
parte_01/
parte_02/
parte_03/
```

A complete structure might look like:

```text
.
├── master.rst
├── meta/
│   └── ...
├── parte_01/
│   ├── p001_i0000_parte-01.rst
│   ├── p001_i0010_v001_first-chapter.rst
│   └── p001_i0020_v001_second-chapter.rst
├── parte_02/
│   ├── p002_i0000_parte-02.rst
│   ├── p002_i0010_v001_third-chapter.rst
│   └── p002_i0020_v001_fourth-chapter.rst
└── parte_03/
    ├── p003_i0000_parte-03.rst
    └── p003_i0010_v001_epilogue.rst
```

---

## 7. Filenames in Projects With Parts

Normal content files use:

```text
p{part:03}_i{index:04}_v{version:03}_{slug}.rst
```

Schematically:

```text
pPPP_iIIII_vVVV_slug.rst
```

Example:

```text
p002_i0060_v002_joker.rst
```

This decomposes into:

```text
p002     part 2
i0060    ordering index 60
v002     version 2
joker    slug
.rst     file extension
```

Another example:

```text
p002_i0040_v003_connection-lost.rst
```

means that the file belongs to **Part 2**, occupies ordering position **40**, and is **version 3** of the item whose slug is `connection-lost`.

---

# 8. Part Header Files

Projects with parts have a special file representing the part itself.

It uses index:

```text
i0000
```

Example:

```text
p001_i0000_parte-01.rst
p002_i0000_parte-02.rst
p003_i0000_parte-03.rst
```

The format is:

```text
p{part:03}_i0000_parte-{part:02}.rst
```

Unlike normal content files, the part header does **not** contain a version component.

Therefore:

```text
p002_i0000_parte-02.rst
```

is correct.

Not:

```text
p002_i0000_v001_parte-02.rst
```

The `i0000` value is reserved for the part itself and places it before all content items belonging to that part.

---

# 9. Directory Names vs. Slugs

Directory names and slugs intentionally use different separators.

Directory:

```text
parte_01/
```

Slug:

```text
parte-01
```

Therefore:

```text
parte_01/
└── p001_i0000_parte-01.rst
```

This is intentional.

The `_` in `parte_01` belongs to the **directory naming convention**.

The `-` in `parte-01` belongs to the **slug naming convention**.

They should not be normalised to the same separator.

---

# 10. Naming Grammar

The convention can be summarised formally as follows.

### Project without parts

```text
chapters/
    i{index:04}_v{version:03}_{slug}.rst
```

Example:

```text
chapters/
    i0040_v003_connection-lost.rst
```

### Project with parts

```text
parte_{part:02}/
    p{part:03}_i{index:04}_v{version:03}_{slug}.rst
```

Example:

```text
parte_02/
    p002_i0040_v003_connection-lost.rst
```

### Part header

```text
parte_{part:02}/
    p{part:03}_i0000_parte-{part:02}.rst
```

Example:

```text
parte_02/
    p002_i0000_parte-02.rst
```

---

# 11. Semantic Meaning of Each Component

| Component      | Format            | Meaning                                                |
| -------------- | ----------------- | ------------------------------------------------------ |
| Part directory | `parte_02`        | Directory containing Part 2                            |
| Part           | `p002`            | Content belongs to Part 2                              |
| Index          | `i0040`           | Ordering position within the relevant content sequence |
| Version        | `v003`            | Third version of the item                              |
| Slug           | `connection-lost` | Human-readable identifier                              |
| Extension      | `.rst`            | reStructuredText source file                           |

The important principle is that these components describe **different dimensions** of the document.

For example:

```text
p002_i0040_v003_connection-lost.rst
```

should be read as:

> Part 2 → item at position 40 → version 3 → `connection-lost`

---

# 12. Core Design Principle

The filesystem should reflect the **actual editorial structure of the work**.

If a work has parts:

```text
parte_01/
parte_02/
parte_03/
```

and filenames include:

```text
p001_
p002_
p003_
```

If a work has no parts:

```text
chapters/
```

and filenames begin directly with:

```text
i0010_
i0020_
i0030_
```

A technical structure should not imply an editorial structure that does not exist.

In short:

```text
WITH PARTS
parte_02/p002_i0040_v003_connection-lost.rst

WITHOUT PARTS
chapters/i0040_v003_connection-lost.rst
```

This distinction is intentional and forms part of the naming specification.
