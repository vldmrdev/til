from pathlib import Path
import sys


def collect_notes(topics_path: Path) -> list[dict[str, str]]:
    if not topics_path.exists():
        print(f"Warning: Directory '{topics_path}' not found.")
        return []

    topics_structure = []

    for topic_dir in sorted(topics_path.iterdir()):
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
            lines.append(f"  - [{note['md_file_name']}]({note['md_file_path']})")
        lines.append("")
    return "\n".join(lines)


def update_readme(
        readme_file_path: Path,
        topics_dir_path: Path,
        marker_start: str,
        marker_end: str
):
    if not readme_file_path.exists():
        raise FileExistsError(f'{readme_file_path} not found.')

    readme_file = readme_file_path.read_text(encoding="utf-8")

    if marker_start not in readme_file or marker_end not in readme_file:
        raise NameError('Markers not found in README.md. Aborting.')

    before, *middle_and_after = readme_file.split(marker_start)
    middle, after = marker_end.join(middle_and_after).split(marker_end, 1)

    topics_structure = collect_notes(topics_dir_path)
    new_toc = render_toc(topics_structure)
    new_middle = f"\n{new_toc}\n"

    new_content = before + marker_start + new_middle + marker_end + after

    if new_content != readme_file:
        readme_file_path.write_text(new_content, encoding="utf-8")
        # print(readme_file)
        # print(new_content)
        print("README.md updated")
        sys.exit(1)
    else:
        print("No changes in README.md.")
        sys.exit(0)


if __name__ == "__main__":
    README_PATH = Path("README.md")
    TOPICS_DIR = Path("topics")
    MARKER_START = "<!-- TIL_START -->"
    MARKER_END = "<!-- TIL_END -->"

    update_readme(README_PATH, TOPICS_DIR, MARKER_START, MARKER_END)

# TODO: fix for pre-commit
