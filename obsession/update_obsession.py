from datetime import date
import re
from sys import argv
import glob
import os
from PIL import Image

# Known bugs:
# - if artist_album is the same as a previous entry, album art will be overwritten


"""
argv[1] == song link
argv[2] == Title
argv[3] == Artist
argv[4] == Album
argv[5] == Year
"""
try: 
    assert len(argv) == 6
except AssertionError:
    usage = """Usage: python update_obsession.py <song URL> <song title> <artist> <album> <year>
The album art must be the most recently downloaded file in your Downloads folder."""
    print(usage)
    exit(1)


##################
# helper functions

def album_art_link(new_info: list[str]):
    local_art_path = "/assets/img/obsession/"
    local_art_path += new_info[2] + "_" + new_info[3]
    local_art_path = local_art_path.lower().replace(" ", "_")

    list_of_files = glob.glob("C:/Users/russo/Downloads/*")
    temp_art_path = max(list_of_files, key=os.path.getctime)
    art = Image.open(temp_art_path)
    art = art.resize((400, 400), Image.Resampling.LANCZOS)

    file_ext = re.compile(r"\.\w+$").search(temp_art_path).group()
    local_art_path += file_ext
    new_art_path = "C:/Users/russo/Documents/GitHub/russotiro.github.io" + local_art_path
    art.save(fp=new_art_path)
    os.remove(temp_art_path)

    return local_art_path


##################
# more setup stuff

new_info = argv[1:]

# append current date to new_info. insert link to album art in new_info
new_info.append(date.today().strftime("%B %#d, %Y"))
new_info.insert(1, album_art_link(new_info))

# patterns[0:5] are the regex patterns corresponding to new_info[0:5]
# metadata[0:5] are the Match objects with actual strings corresponding to new_info[0:5]
# metadata[6] and new_info[6] are the date I put it on my website & the pattern to detect that
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
for pattern, field in zip(patterns, new_info[0:7]):
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
