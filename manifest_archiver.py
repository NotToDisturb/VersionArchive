import json

from wob import get_wob_manifests

SHIPPING_EXE = "VALORANT-Win64-Shipping.exe"
MANIFESTS_PATH = ".\\out\\manifests.json"

def load_manifests():
    with open(MANIFESTS_PATH, mode="r", encoding="utf-8") as manifests_file:
        return json.load(manifests_file)


def save_manifests(manifests):
    sorted_manifests = sorted(
        manifests,
        key=lambda v: v["upload_timestamp"] if v["release_timestamp"] == 0 else v["release_timestamp"],
        reverse=True
    )
    with open(MANIFESTS_PATH, mode="w", encoding="utf-8") as manifests_file:
        json.dump(sorted_manifests, manifests_file, indent=4)


def is_manifest_archived(manifests: list, manifest: str):
    for archived_manifest in manifests:
        if archived_manifest["manifest"] == manifest:
            return True
    return False


def archive_wob_manifests(manifests, wob):
    for version in wob:
        if is_manifest_archived(manifests, version["manifest"]):
            print(f"     {version['manifest']}: aready archived")
            continue
        manifests.append(version)
        print(f"     {version['manifest']}: new manifest")
    save_manifests(manifests)


def main():
    manifests = load_manifests()
    print("[MA] Downloading White-Owl-Bot manifests")
    wob = get_wob_manifests()
    print("[MA] Archiving White-Owl-Bot manifests:")
    archive_wob_manifests(manifests, wob)


if __name__ == "__main__":
    main()
