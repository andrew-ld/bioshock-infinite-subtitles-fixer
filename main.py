import os
import re
import sys
import typing


def main(path: str, fixed_path: str):
    for filename in os.listdir(path):
        absolute_path = os.path.join(path, filename)

        with open(absolute_path, "rb") as config_file:
            config = config_file.read().decode("utf-16", errors="ignore")

        result = []

        for line in config.splitlines():
            line = line.strip()

            if not line.startswith("Subtitles["):
                result.append(line)
                continue

            subtitle = re.findall(r'Subtitle=\\\"(.*)\\\"\)', line)

            if len(subtitle) == 0:
                result.append(line)
                continue

            assert len(subtitle) == 1
            subtitle = typing.cast(str, subtitle[0])

            subtitle_lines = subtitle.split("&bs;n")
            max_len = max(map(len, subtitle_lines))

            if max_len < 90:
                result.append(line)
                continue

            fixed_subtitle_lines = []

            for subtitle_line in subtitle_lines:
                if len(subtitle_line) < 90:
                    fixed_subtitle_lines.append(subtitle_line)
                    continue

                new_line = []

                for word in subtitle_line.split():
                    new_line.append(word)

                    if sum(map(len, new_line)) > min((90, len(subtitle_line) / 2)):
                        fixed_subtitle_lines.append(" ".join(new_line))
                        new_line = []

                if new_line:
                    fixed_subtitle_lines.append(" ".join(new_line))

            fixed_subtitle = "&bs;n".join(fixed_subtitle_lines)
            result.append(line.replace(subtitle, fixed_subtitle))

        fixed_result = "\r\n".join(result) + "\r\n"

        with open(os.path.join(fixed_path, filename), "wb") as result_file:
            result_file.write(fixed_result.encode("utf-16"))


if __name__ == "__main__":
    main(sys.argv[-2], sys.argv[-1])
