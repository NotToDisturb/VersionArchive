import json

from urllib.request import Request, urlopen
from fake_useragent import UserAgent

WOB_URL = "https://raw.githubusercontent.com/WhiteOwlBot/WhiteOwl-public-data/main/manifests.json"


def get_wob_manifests() -> list:
    request = Request(WOB_URL)
    request.add_header("User-Agent", UserAgent().random)
    raw_manifests = urlopen(request).read().decode("utf-8")
    processed_manifests = [process_manifest(version) for version in json.loads(raw_manifests)]
    return sorted(
        processed_manifests,
        key=lambda v: v["upload_timestamp"] if v["release_timestamp"] == 0 else v["release_timestamp"],
        reverse=True
    )

def process_manifest(version):
    return {
        "manifest": version["id"],
        "branch": clean_manifest_branch(version["build_info"]["branch"]),
        "version": version["build_info"]["version"],
        "date": version["build_info"]["build_date"],
        "upload_timestamp": version["upload_timestamp"],
        "release_timestamp": version["release_timestamp"]
    }

def clean_manifest_branch(dirty_branch):
    return dirty_branch if dirty_branch == "pbe" else dirty_branch.split("-")[0]
