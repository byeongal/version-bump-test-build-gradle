import argparse
import json
import os
import re


def bump_version(version: str, bump_type: str):
    major, minor, patch = map(int, version.split("."))
    if bump_type == "major":
        major += 1
        minor = 0
        patch = 0
    elif bump_type == "minor":
        minor += 1
        patch = 0
    else:
        patch += 1
    return f"{major}.{minor}.{patch}"


def bump_from_package_json(file_path: str, bump_type: str):
    with open(file_path, "r") as f:
        data = json.load(f)

    old_version = data.get("version", "0.0.0")
    new_version = bump_version(old_version, bump_type)
    data["version"] = new_version
    print(f"::set-output name=OLD_VERSION::{old_version}")
    print(f"::set-output name=NEW_VERSION::{new_version}")

    with open(file_path, "w", encoding="UTF-8") as f:
        json.dump(data, f, indent=2)


def bump_from_build_gradle(file_path: str, bump_type: str):
    with open(file_path, "r") as f:
        data = f.read()
    pattern = re.compile(r"version = \"(\d+)\.(\d+)\.(\d+)\"")
    matched = pattern.search(data)
    old_version = "0.0.0"
    if matched:
        major_version, minor_version, patch_version = matched.groups()
        old_version = f"{major_version}.{minor_version}.{patch_version}"
    new_version = bump_version(old_version, bump_type)
    updated_data = pattern.sub(f'version = "{new_version}"', data)
    print(f"::set-output name=OLD_VERSION::{old_version}")
    print(f"::set-output name=NEW_VERSION::{new_version}")
    with open(file_path, "w", encoding="UTF-8") as f:
        f.write(updated_data)


SUPPORT_FILE_NAME = {
    "package.json": bump_from_package_json,
    "build.gradle": bump_from_build_gradle,
}


def bump(file_path: str, bump_type: str):
    file_name = os.path.basename(file_path)
    if os.path.exists(file_path) is False:
        print(f"File {file_path} does not exist")
        exit(1)
    if file_name not in SUPPORT_FILE_NAME:
        print(f"File {file_name} is not supported")
        exit(2)
    SUPPORT_FILE_NAME[file_name](file_path, bump_type)


def parse_args():
    parser = argparse.ArgumentParser(description="Bump version of a package")
    parser.add_argument("--file_path", type=str, help="The path to the file containing the version to update")
    parser.add_argument(
        "--type",
        type=str,
        choices=["major", "minor", "patch"],
        default="minor",
        help="Which part of the version to bump",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    bump(args.file_path, args.type)


if __name__ == "__main__":
    main()
