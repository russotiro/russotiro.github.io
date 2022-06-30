from datetime import date
import re
from sys import argv

"""
argv[1] == song link
argv[2] == image link
argv[3] == Title
argv[4] == Artist
argv[5] == Album
argv[6] == Year
"""
assert len(argv) == 7

# append current date to argv
argv.append(date.today().strftime("%B %#d, %Y"))

# patterns[0:5] are the regex patterns corresponding to argv[1:6]
# metadata[0:5] are the Match objects with actual strings corresponding to argv[1:6]
# metadata[6] and argv[7] are the date I put it on my website & the pattern to detect that
metadata = []
patterns = [r"(?<=<a href=\")\S+(?=\")",
            r"(?<=class=\"the\-art\" src=\")\S+(?=\")",
            r"(?<=&#8220;).+(?=&#8221;)",
            r"(?<=<p>by ).+(?=<\/p>)",
            r"(?<=<p>from <em>).+(?=<\/em>)",
            r"(?<=<\/em> \()\d{4}(?=\)<\/p>)",
            r"(?<=<\/div>\n {8}<!\-\- ).+(?= \-\->)"]
patterns = map(re.compile, patterns)


###########################
# now actually do the stuff

with open("index.html", "r") as file:
    contents = file.read()


# replace fields in the-obsession
for pattern, field in zip(patterns, argv[1:8]):
    metadata.append(pattern.search(contents).group())
    contents = pattern.sub(field, contents, 1)

# add new entry to bottom section
entry = f"""
        <tr>
            <td><a href="{metadata[0]}"><img src="{metadata[1]}" alt="Album art for obsession"></a></td>
            <td>{metadata[2]}</td>
            <td>{metadata[3]}</td>
            <td><em>{metadata[4]}</em></td>
            <td>{metadata[5]}</td>
            <td>{metadata[6]}</td>
        </tr>"""

index = re.search(r"(?<=<\/th>\n {8}<\/tr>)\n", contents).span()[0]
contents = contents[:index] + entry + contents[index:]


with open("index.html", "w") as file:
    file.write(contents)
