import requests
import re
import minify_html
import csv

from commoner import Shout
from ratelimit import limits, RateLimitException, sleep_and_retry
from os import listdir
from os.path import isfile, join

ONE_MINUTE = 60
MAX_CALLS_PER_MINUTE = 300

WEBHOOK_ROOT = "https://webbook.nist.gov"
WEBHOOK_QUERY = "/cgi/cbook.cgi?ID={}&Units=SI"
WEBHOOK_URL = WEBHOOK_ROOT + WEBHOOK_QUERY

SUCCESS = 0
SKIP = 0
FAIL = 0

TOTAL_IMAGES_TO_FETCH = 0
with open("species.txt", "r") as f:
    SPECIES = f.read().splitlines()
    for entry in SPECIES:
        if entry[2] != "N/A":
            TOTAL_IMAGES_TO_FETCH += 1

regex_data = {
    "name": "<h1 id=Top>(.*)</h1>",
    "formula": '<li><strong><a title="IUPAC definition of empirical formula"href=http://goldbook.iupac.org/E02063.html>Formula</a>:</strong>(.*)<li><strong><a title="IUPAC definition of relative molecular mass',
    "molar_mass": '<li><strong><a title="IUPAC definition of relative molecular mass \(molecular weight\)"href=http://goldbook.iupac.org/R05271.html>Molecular weight</a>:</strong>(.*)<li><div',
    "inchi": "<div class=left-float><strong>IUPAC Standard InChI:</strong><span clss=inchi-text>InChI=([^<]*)</span>",
    "inchi_key": "<strong>IUPAC Standard InChIKey:</strong> <span class=inchi-text>([^<]*)</span>",
    "cas_number": "<strong>CAS Registry Number:</strong>\s([^<]+)",
    "structure": "<strong>Chemical structure:</strong> <img alt=(.*) class=struct src=([^<>]*)",
    "other_names": "<strong>Other names:</strong>\s([^<]+)",
}


def fetch_text(url):
    response = requests.get(url)
    return response.text


def extract_data(text):
    text = minify_html.minify(text)
    data = {}
    for key in regex_data:
        data[key] = re.findall(regex_data[key], text)
    return data


def filter_data(data):
    for key in data:
        if type(data[key]) == str:
            data[key] = data[key].strip()
        elif type(data[key]) == list and len(data[key]) == 1:
            if type(data[key][0]) == str:
                data[key] = data[key][0].strip()
        if key == "formula":
            if data["structure"] != []:
                data[key] = data["structure"][0][0]
        elif key == "other_names":
            if type(data[key]) == str:
                data[key] = data[key].split("; ")
            elif type(data[key]) == list:
                if len(data[key]) != 0:
                    data[key] = data[key][0].split("; ")
            else:
                Shout.error(
                    f"Unknown type for other_names: {type(data[key])}, {data[key]}"
                )
        elif data[key] == "structure":
            data[key] = data[key][0][1]
    return data


def download_image(url, filename="image.png"):
    try:
        data = requests.get(url)
    except requests.exceptions.ConnectionError:
        Shout.error(f"Connection error for {url}")
        return None
    with open(filename, "wb") as f:
        f.write(data.content)
    return None


@sleep_and_retry
@limits(calls=MAX_CALLS_PER_MINUTE, period=ONE_MINUTE)
def get(cas_number, ROOT_PATH=""):
    global SUCCESS, SKIP, FAIL
    data = filter_data(extract_data(fetch_text(WEBHOOK_URL.format(cas_number))))
    if data["structure"] == [] or data["formula"] == []:
        Shout.warning(
            f"Failed to download image for {data['name']} ({cas_number}), moving on (formula not found)"
        )
        with open("failed.txt", "a") as f:
            f.write(cas_number + "\n")
        FAIL += 1
        return data
    try:
        IMG_URL = data["structure"][0][1]
        IMG_NAME = f"{data['formula']}.png"
        download_image(WEBHOOK_ROOT + IMG_URL, join(ROOT_PATH, IMG_NAME))
        Shout.success(
            f"Downloaded image for {data['name']}/{cas_number} to {join(ROOT_PATH, IMG_NAME)}"
        )
    except FileNotFoundError:
        Shout.warning(
            f"Failed to download image for {data['name']} ({cas_number}), proceeding anyway (image not found)"
        )
        with open("failed.txt", "a") as f:
            f.write(cas_number + "\n")
        FAIL += 1
    return data


def run():
    global SUCCESS, SKIP, FAIL
    IMAGE_PATH = "./images"
    IMAGES_IN_FOLDER = [f for f in listdir(IMAGE_PATH) if isfile(join(IMAGE_PATH, f))]
    FAILED_IMAGES = open("failed.txt", "r").read().splitlines()
    Shout.info(
        f"Found {len(IMAGES_IN_FOLDER)} images in folder ({len(IMAGES_IN_FOLDER) + len(FAILED_IMAGES)}/{TOTAL_IMAGES_TO_FETCH}, including {len(FAILED_IMAGES)} failed images)"
    )
    with open("species.txt", "r") as f:
        data = csv.reader(f, delimiter="\t")
        for row in data:
            ROW_NAME = row[0]
            ROW_FORMULA = row[1]
            ROW_CAS = row[2]
            if ROW_CAS != "N/A":
                if (
                    f"{ROW_FORMULA}.png" not in IMAGES_IN_FOLDER
                    and ROW_CAS not in FAILED_IMAGES
                ):
                    try:
                        get(ROW_CAS, ROOT_PATH=IMAGE_PATH)
                        SUCCESS += 1
                    except RateLimitException:
                        Shout.warning("Rate limit exceeded")
                else:
                    SKIP += 1
                    print(f"Skipping {ROW_FORMULA}, already downloaded")
        Shout.info(
            f"Downloaded {SUCCESS} images, skipped {SKIP-FAIL} images (already downloaded), images missing for {FAIL} images"
        )


run()
