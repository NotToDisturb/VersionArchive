import os
import json
import shutil
import numpy as np
import pandas as pd

from urllib.request import urlretrieve
from versionutils import get_game_version, get_processed_wob_versions, extract_manifest_id

SHIPPING_EXE = "VALORANT-Win64-Shipping.exe"

RAP_URL = "https://archive.org/download/valorant-archive/valorant/valorant_manifests.txt"
RAP_PATH = ".\\res\\valorant_manifests.csv"
MD_PATH = ".\\res\\ManifestDownloader.exe"

MANIFESTS_PATH = ".\\out\\manifests.json"

TEMP_PATH = ".\\temp\\"
SHIPPING_PATH = TEMP_PATH + "ShooterGame\\Binaries\\Win64\\" + SHIPPING_EXE


def load_manifests():
    with open(MANIFESTS_PATH, mode="r", encoding="utf-8") as manifests_file:
        return json.load(manifests_file)


def save_manifests(manifests):
    with open(MANIFESTS_PATH, mode="w", encoding="utf-8") as manifests_file:
        sorted_manifests = sorted(
            manifests,
            key=lambda v: v["upload_timestamp"] if v["release_timestamp"] == 0 else v["release_timestamp"],
            reverse=True
        )
        json.dump(sorted_manifests, manifests_file, indent=4)


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
# https://archive.org/download/valorant-archive/valorant/valorant_manifests.txt
def get_valorant_rap():
    urlretrieve(RAP_URL, RAP_PATH)
    rap_valorant = pd.read_csv(RAP_PATH, usecols=[1, 2, 3], delimiter="\t",
                               header=None, names=["Manifest", "Date", "Time"], index_col=False)

    rap_valorant["Timestamp"] = pd.to_datetime(rap_valorant["Date"] + " " + rap_valorant["Time"])
    rap_valorant["Timestamp"] = rap_valorant["Timestamp"].astype(np.int64) // 10 ** 9
    return rap_valorant[["Manifest", "Timestamp"]].sort_values("Timestamp", ascending=False)


def get_manifest_data(manifests: list, manifest: str):
    for archived_manifest in manifests:
        if archived_manifest["manifest"] == manifest:
            return archived_manifest
    return None


def fetch_shipping_exe(manifest: str):
    manifest_url = manifest if manifest.endswith(".manifest") \
        else f"https://valorant.secure.dyn.riotcdn.net/channels/public/releases/{manifest}.manifest"
    bundle_url = "https://valorant.secure.dyn.riotcdn.net/channels/public/bundles"
    command = f"{MD_PATH} {manifest_url} -b {bundle_url} --filter {SHIPPING_EXE} -o {TEMP_PATH}"
    os.system(command)


def archive_wob(manifests, wob):
    for version in wob:
        if get_manifest_data(manifests, version["manifest"]):
            print(f"{version['manifest']} (WOB): existing archive")
            continue

        manifests.append(version)
        print(f"{version['manifest']} (WOB): new archive")
    # WOB is quick, save only after all al done
    save_manifests(manifests)


def archive_valorant_rap(manifests: list, rap_valorant: pd.DataFrame):
    for _, row in rap_valorant.iterrows():
        manifest = extract_manifest_id(row["Manifest"])
        manifest_data = get_manifest_data(manifests, manifest)
        if manifest_data:
            print(f"{manifest} (Riot Archive): existing archive")
            continue

        print(f"{manifest} (Riot Archive): new archive")
        create_temp_folder()
        fetch_shipping_exe(row["Manifest"])
        client_version = get_game_version(SHIPPING_PATH)
        delete_temp_folder()
        print()
        archive_manifest = {
            "manifest": manifest,
            "branch": client_version["branch"],
            "version": client_version["version"],
            "date": client_version["date"],
            "upload_timestamp": row["Timestamp"],
            "release_timestamp": 0
        }
        manifests.append(archive_manifest)
        # Riot Archive requires downloads, save after every manifest
        save_manifests(manifests)


def main():
    manifests = load_manifests()

    wob = get_processed_wob_versions()
    # rap_valorant = get_valorant_rap()

    archive_wob(manifests, wob)
    # archive_valorant_rap(manifests, rap_valorant)


if __name__ == "__main__":
    main()
