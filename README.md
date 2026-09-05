# Writit

**Writit** is a project management application for literary writing and other creative projects, built as a hands-on way to learn Python.

It provides a command-line interface for creating and organising writing projects, managing chapters and parts, and keeping multiple versions of individual files.

🚦 **Status:** Writit is currently under development. It is primarily a learning project, and its structure and features may change significantly.

## 🏷️ Why Writit?

Writit started from two related goals:

1. Learn Python by building a real application rather than working only through isolated exercises.
1. Create a simple set of tools for managing the structure and files of long-form writing projects.

The project is therefore both a practical writing tool and a place to experiment with Python concepts, architecture, testing and CLI development.

## 🥕 Features

Writit currently supports or is being developed to support:

* Creation of writing projects from the command line.
* Different project structures:
    * standalone works;
    * chapter-based works;
    * works divided into parts and chapters.
* Automatic project folder structures.
* Creation of new writing files.
* Automatic file indexing.
* Multiple versions of the same file.
* Localised project structures and metadata.
* Automatic generation and synchronisation of a `master.md` file.
* Conversion to LibreOffice ODT files.
* Markdown-based source files.
* Project metadata stored alongside the project.
* Automated tests with pytest.

## 🧬 Project structures

Writit supports three basic types of writing projects.

### 🗎 Standalone

For standalone works such as articles, essays, and short stories that do not need to be divided into chapters or parts.

The manuscript files will be created in a folder with the localized name for `text`.

```text
my-project/
├── meta/
├── text/
│   └── v001_stand-alone.md
└── master.md
```

### 📑 Chaptered

For works organised as a sequence of chapters.

```text
my-project/
├── meta/
├── chapters/
│   ├── i0010_v001_first-chapter.md
│   └── i0020_v001_second-chapter.md
└── master.md
```

### 📚 Parted

For larger works divided into parts, with chapters inside each part.

```text
my-project/
├── meta/
├── part_01/
│   ├── p001_i0000_part-01.md
│   ├── p001_i0010_v001_first-chapter.md
│   └── p001_i0020_v001_second-chapter.md
├── part_02/
│   ├── p002_i0000_part-02.md
│   └── p002_i0010_v001_another-chapter.md
└── master.md
```

The numbering scheme makes the structure and ordering of the project explicit while allowing titles and versions to change independently.

## ⌨️ CLI

Writit is designed primarily as a command-line application.

Examples:

```bash
writit project create /path/to/projects \
    --title "My Novel" \
    --project-type parted \
    --parts 3
```

Create a new file:

```bash
writit file create /path/to/project/part_01 \
    --title "The First Chapter"
```

Create a new version of an existing file:

```bash
writit file version /path/to/project/part_01/p001_i0010_v001_the-first-chapter.md
```

> The CLI is still evolving, so commands and options may change.

## 🗂️ File naming

Writit uses structured filenames to represent the position and version of a file.

For example:

```text
p001_i0020_v004_old-new-world.md
```

where:

* `p001` — part number;
* `i0020` — position/index within the project;
* `v004` — file version;
* `old-new-world` — slug generated from the title.

Depending on the project type, some components may be omitted:

```text
v004_short-story.md
i0020_v004_chapter.md
p001_i0020_v004_chapter.md
```

## 🌐 Localisation

Writit includes a simple localisation system so that generated project structures and metadata can follow different languages.

For example:

```text
chapters/
part_01/
summary.md
```

can become:

```text
capitulos/
parte_01/
resumo.md
```

Date formatting and other generated text can also be localised.

## 🛠️ Development

Writit is written in Python and currently uses tools and libraries including:

* Python 3
* Click
* pytest
* Markdown

The codebase is deliberately being developed incrementally as part of the learning process.

## 🎯 Goals

The long-term direction of Writit is to provide a lightweight environment for managing the source files behind literary and other structured creative projects.

Possible areas of development include:

* improved master-file generation and synchronisation;
* export to publication-oriented formats;
* better project metadata management;
* additional localisation;
* more flexible templates;
* richer CLI tools for reorganising projects;
* support for other creative project structures.

The exact scope is intentionally open while the project evolves.

## ⚖️ License

This project is licensed under the MIT License. See the `LICENSE` file for details.
