# © 2025 Fabien FURFARO <fabien.furfaro@gmail.com>
#
# SPDX-License-Identifier: Apache-2.0+
# SPDX-FileContributor:    Fabien FURFARO

"""
Script pour extraire le texte de tous les fichiers d'un projet,
en ignorant les fichiers et dossiers spécifiés dans .gitignore.
Le texte extrait est sauvegardé dans un fichier unique structuré en Markdown.
Permet de capturer le contexte complet du projet pour des analyses via un LLM.
"""

import os

import pathspec


def load_gitignore_patterns(gitignore_path=".gitignore"):
    with open(gitignore_path, "r") as f:
        patterns = f.read().splitlines()
    spec = pathspec.PathSpec.from_lines("gitwildmatch", patterns)
    return spec


def get_language_from_extension(filename):
    ext = os.path.splitext(filename)[1].lower()
    lang_map = {
        ".py": "python",
        ".js": "javascript",
        ".java": "java",
        ".cpp": "cpp",
        ".c": "c",
        ".ts": "typescript",
        ".html": "html",
        ".css": "css",
        ".json": "json",
        ".yaml": "yaml",
        ".yml": "yaml",
        ".md": "markdown",
    }
    return lang_map.get(ext, "text")


def build_tree_markdown(root_dir, gitignore_spec, exclude_dirs=None):
    exclude_dirs = exclude_dirs or []
    tree_lines = []

    for dirpath, dirnames, filenames in os.walk(root_dir):
        # Exclure explicitement certains dossiers (ex: .git, extract)
        for excl_dir in exclude_dirs:
            if excl_dir in dirnames:
                dirnames.remove(excl_dir)
        # Appliquer aussi les règles gitignore sur les dossiers
        dirnames[:] = [
            d
            for d in dirnames
            if not gitignore_spec.match_file(
                os.path.relpath(os.path.join(dirpath, d), root_dir)
            )
        ]

        rel_path = os.path.relpath(dirpath, root_dir)
        indent = "  " * (rel_path.count(os.sep) if rel_path != "." else 0)
        base_name = os.path.basename(dirpath) if rel_path != "." else rel_path
        tree_lines.append(f"{indent}- {base_name}/")

        # Filtrer aussi les fichiers selon gitignore
        visible_files = [
            f
            for f in sorted(filenames)
            if not gitignore_spec.match_file(
                os.path.relpath(os.path.join(dirpath, f), root_dir)
            )
        ]

        for f in visible_files:
            tree_lines.append(f"{indent}  - {f}")

    return "\n".join(tree_lines)


def extract_project_text(root_dir, output_file, gitignore_spec, exclude_dirs=None):
    exclude_dirs = exclude_dirs or []
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    tree_md = build_tree_markdown(root_dir, gitignore_spec, exclude_dirs)

    with open(output_file, "w", encoding="utf-8") as out_f:
        # Écrire l’arborescence en début de fichier
        out_f.write("# Project Directory Tree\n\n")
        out_f.write(tree_md)
        out_f.write("\n\n---\n\n")

        for subdir, dirs, files in os.walk(root_dir):
            # Exclure explicitement certains dossiers (ex: .git, extract)
            for excl_dir in exclude_dirs:
                if excl_dir in dirs:
                    dirs.remove(excl_dir)
            # Appliquer aussi les règles gitignore sur les dossiers
            dirs[:] = [
                d
                for d in dirs
                if not gitignore_spec.match_file(
                    os.path.relpath(os.path.join(subdir, d), root_dir)
                )
            ]

            for file in files:
                rel_path = os.path.relpath(os.path.join(subdir, file), root_dir)
                if gitignore_spec.match_file(rel_path):
                    continue

                filepath = os.path.join(subdir, file)
                try:
                    with open(filepath, "r", encoding="utf-8") as in_f:
                        content = in_f.read()
                    lang = get_language_from_extension(file)
                    out_f.write(f"\n\n# File: {filepath}\n")
                    out_f.write(f"```{lang}\n")
                    out_f.write(content)
                    out_f.write("\n```\n")
                except Exception as e:
                    print(f"Could not read {filepath}: {e}")


if __name__ == "__main__":
    root_dir = "./"
    output_file = "./extract/projet_complet.md"
    gitignore_spec = load_gitignore_patterns(os.path.join(root_dir, ".gitignore"))
    # Ne pas parcourir .git ni extract (sortie)
    extract_project_text(
        root_dir, output_file, gitignore_spec, exclude_dirs=[".git", "extract"]
    )
