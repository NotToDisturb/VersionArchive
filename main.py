import os
import json
import shutil
import numpy as np
import pandas as pd

from versionutils import get_game_version

RAP_PATH = ".\\res\\Riot Archive Project - Valorant.csv"
MD_PATH = ".\\res\\ManifestDownloader.exe"

MANIFESTS_PATH = ".\\out\\manifests.json"

TEMP_PATH = ".\\temp\\"

SHIPPING_EXE = "VALORANT-Win64-Shipping.exe"


def create_temp_folder():
    if os.path.isdir(TEMP_PATH):
        return
    os.mkdir(TEMP_PATH)


def delete_temp_folder():
    if not os.path.isdir(TEMP_PATH):
        return
    shutil.rmtree(TEMP_PATH, ignore_errors=True)


# Riot Archive Project
# https://docs.google.com/spreadsheets/d/18Fl88fB2sI57OFhOFSHtcOlHZG9kMS0uU3kjFxzv_EA/edit#gid=181398849
def get_valorant_rap():
    rap_valorant = pd.read_csv(RAP_PATH, usecols=[1, 2, 3],
                               header=None, names=["Manifest", "Date", "Time"], index_col=False)

    rap_valorant["Timestamp"] = pd.to_datetime(rap_valorant["Date"] + " " + rap_valorant["Time"])
    rap_valorant["Timestamp"] = rap_valorant["Timestamp"].astype(np.int64) // 10 ** 9
    return rap_valorant[["Manifest", "Timestamp"]]


def fetch_shipping_exe(manifest: str):
    manifest_url = manifest if manifest.endswith(".manifest") \
        else f"https://valorant.secure.dyn.riotcdn.net/channels/public/releases/{manifest}.manifest"
    bundle_url = "https://valorant.secure.dyn.riotcdn.net/channels/public/bundles"
    command = f"{MD_PATH} {manifest_url} -b {bundle_url} --filter {SHIPPING_EXE} -o {TEMP_PATH}"

    create_temp_folder()
    os.system(command)


def archive_valorant_rap(manifests: dict, rap_valorant: pd.DataFrame):
    for _, row in rap_valorant.iterrows():
        manifest_url = row["Manifest"]
        manifest = manifest_url.split(".manifest")[0].split("/")[-1]
        print(manifest, row["Timestamp"])


def main():
    with open(MANIFESTS_PATH, encoding="utf-8") as manifests_file:
        manifests = json.load(manifests_file)
        rap_valorant = get_valorant_rap()

        archive_valorant_rap(manifests, rap_valorant)

        delete_temp_folder()


if __name__ == "__main__":
    main()
