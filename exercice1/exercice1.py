"""Exercice 1 """

MAX_BLOCK_WIDTH = 100

PHRASES = {
    "b1_l1": "Le code propre facilite la maintenance",
    "b2_l1": "Tester souvent évite beaucoup d'erreurs",
    "b2_l2": "Cette phrase ne doit pas s'afficher",
    "b3_l1": "Cette phrase ne doit pas s'afficher",
    "b3_l2": "Un bon code doit rester simple et clair",
    "b3_l3": "La simplicité améliore la qualité du code",
    "b3_l4": "Refactoriser améliore la compréhension",
}

BLOCKS = {
    "bloc_1": ["b1_l1"],
    "bloc_2": ["b2_l1", "b2_l2"],
    "bloc_3": ["b3_l1", "b3_l2", "b3_l3", "b3_l4"],
}

DISPLAY_ORDER = ["bloc_1", "bloc_2", "bloc_3"]

EXCLUDED_LINE_IDS = {"b2_l2", "b3_l2"}


def render_block(lines: list[str], max_width: int) -> str:
    text_lines = [line.lower() for line in lines]
    content_width = min(max((len(line) for line in text_lines), default=0), max_width - 2)
    horizontal = "-" * (content_width + 2)

    rendered = [horizontal]
    for line in text_lines:
        clipped = line[:content_width]
        rendered.append(f"|{clipped.ljust(content_width)}|")
    rendered.append(horizontal)
    return "\n".join(rendered)


def main() -> None:
    blocks_to_print = []
    for block_id in DISPLAY_ORDER:
        line_ids = BLOCKS.get(block_id, [])
        lines = [
            PHRASES[line_id]
            for line_id in line_ids
            if line_id in PHRASES and line_id not in EXCLUDED_LINE_IDS
        ]
        blocks_to_print.append(render_block(lines, MAX_BLOCK_WIDTH))

    print("\n\n".join(blocks_to_print))


if __name__ == "__main__":
    main()