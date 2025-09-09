import datetime
from pathlib import Path

README_PATH = Path("README.md")
TOPICS_DIR = Path("topics")
MARKER_START = "<!-- TIL_START -->"
MARKER_END = "<!-- TIL_END -->"


def format_timestamp(timestamp):
    return datetime.datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d")


def collect_notes() -> list[dict[str, str]]:
    if not TOPICS_DIR.exists():
        print(f"Warning: Directory '{TOPICS_DIR}' not found.")
        return []

    topics_structure = []

    for topic_dir in sorted(TOPICS_DIR.iterdir()):
        if not topic_dir.is_dir():
            continue

        md_files = sorted(topic_dir.glob("*.md"))
        if not md_files:
            continue

        topics_structure.append(
            {
                "dir_name": topic_dir.name,
                "dir_path": topic_dir.as_posix(),
                "notes": [
                    {
                        'md_file_name': file.stem,
                        'md_file_path': file.as_posix(),
                        'md_file_timestamp': format_timestamp(file.stat().st_mtime)
                    }
                    for file in md_files
                ]
            }
        )

    return topics_structure


def render_toc(topics):
    lines = [""]
    for topic in topics:
        lines.append(f"- [{topic['dir_name']}]({topic['dir_path']}/)")
        for note in topic["notes"]:
            lines.append(f"  - {note['md_file_timestamp']}: [{note['md_file_name']}]({note['md_file_path']})")
        lines.append("")
    return "\n".join(lines)


def update_readme():
    readme_file_path = Path("README.md")
    if not readme_file_path.exists():
        raise FileExistsError(f'{README_PATH} not found.')

    readme_file = README_PATH.read_text(encoding="utf-8")

    if MARKER_START not in readme_file or MARKER_END not in readme_file:
        raise NameError('Markers not found in README.md. Aborting.')

    before, *middle_and_after = readme_file.split(MARKER_START)
    middle, after = MARKER_END.join(middle_and_after).split(MARKER_END, 1)

    topics_structure = collect_notes()
    new_toc = render_toc(topics_structure)
    new_middle = f"\n{new_toc}\n"

    new_content = before + MARKER_START + new_middle + MARKER_END + after

    if new_content != topics_structure:
        README_PATH.write_text(new_content, encoding="utf-8")
        print("README.md updated")
    else:
        print("No changes in TOC.")


if __name__ == "__main__":
    update_readme()


# TODO: fix for pre-commit