import os
import json
import shutil
import numpy as np
import pandas as pd

from versionutils import get_game_version

SHIPPING_EXE = "VALORANT-Win64-Shipping.exe"

RAP_PATH = ".\\res\\Riot Archive Project - Valorant.csv"
MD_PATH = ".\\res\\ManifestDownloader.exe"

MANIFESTS_PATH = ".\\out\\manifests.json"

TEMP_PATH = ".\\temp\\"
SHIPPING_PATH = TEMP_PATH + "ShooterGame\\Binaries\\Win64\\" + SHIPPING_EXE


def create_temp_folder():
    if os.path.isdir(TEMP_PATH):
        return
    os.mkdir(TEMP_PATH)


def delete_temp_folder():
    if not os.path.isdir(TEMP_PATH):
        return
    shutil.rmtree(TEMP_PATH, ignore_errors=True)


def extract_manifest_id(manifest_url: str):
    return manifest_url.split(".manifest")[0].split("/")[-1]


def extract_version_number(client_version: str):
    if client_version.startswith("pbe"):
        return ""
    split_version = client_version.split("-")
    return split_version[1] + ".00." + split_version[-1]


# Riot Archive Project
# https://docs.google.com/spreadsheets/d/18Fl88fB2sI57OFhOFSHtcOlHZG9kMS0uU3kjFxzv_EA/edit#gid=181398849
def get_valorant_rap():
    rap_valorant = pd.read_csv(RAP_PATH, usecols=[1, 2, 3],
                               header=None, names=["Manifest", "Date", "Time"], index_col=False)

    rap_valorant["Timestamp"] = pd.to_datetime(rap_valorant["Date"] + " " + rap_valorant["Time"])
    rap_valorant["Timestamp"] = rap_valorant["Timestamp"].astype(np.int64) // 10 ** 9
    return rap_valorant[["Manifest", "Timestamp"]]


def is_manifest_in_archive(manifests: dict, manifest: str):
    for archived_manifest in manifests:
        if archived_manifest["manifest"] == manifest:
            return True
    return False


def fetch_shipping_exe(manifest: str):
    manifest_url = manifest if manifest.endswith(".manifest") \
        else f"https://valorant.secure.dyn.riotcdn.net/channels/public/releases/{manifest}.manifest"
    bundle_url = "https://valorant.secure.dyn.riotcdn.net/channels/public/bundles"
    command = f"{MD_PATH} {manifest_url} -b {bundle_url} --filter {SHIPPING_EXE} -o {TEMP_PATH}"

    create_temp_folder()
    os.system(command)


def archive_valorant_rap(manifests, rap_valorant: pd.DataFrame):
    for _, row in rap_valorant.iterrows():
        manifest = extract_manifest_id(row["Manifest"])

        if not is_manifest_in_archive(manifests, manifest):
            print(f"Archiving {manifest}...")
            fetch_shipping_exe(row["Manifest"])
            client_version = get_game_version(SHIPPING_PATH)
            archive_manifest = {
                "manifest": manifest,
                "version_number": extract_version_number(client_version),
                "client_version": client_version,
                "release_timestamp": row["Timestamp"]
            }
            manifests.append(archive_manifest)


def main():
    with open(MANIFESTS_PATH, mode="r", encoding="utf-8") as manifests_file:
        manifests = json.load(manifests_file)

    rap_valorant = get_valorant_rap()
    archive_valorant_rap(manifests, rap_valorant)
    delete_temp_folder()

    with open(MANIFESTS_PATH, mode="w", encoding="utf-8") as manifests_file:
        json.dump(manifests, manifests_file, indent=4)


if __name__ == "__main__":
    main()
