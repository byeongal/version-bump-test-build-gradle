import argparse
import json
import os
import re


# Version bump functions
def bump_version(version: str, bump_type: str) -> str:
    major, minor, patch = map(int, version.split("."))
    if bump_type == "major":
        major += 1
        minor = 0
        patch = 0
    elif bump_type == "minor":
        minor += 1
        patch = 0
    else:  # patch
        patch += 1
    return f"{major}.{minor}.{patch}"


# Update version in package.json
def bump_from_package_json(file_path: str, bump_type: str):
    with open(file_path, "r") as f:
        data = json.load(f)
    old_version = data.get("version", "0.0.0")
    new_version = bump_version(old_version, bump_type)
    data["version"] = new_version
    with open(file_path, "w", encoding="UTF-8") as f:
        json.dump(data, f, indent=2)
    return new_version  # Return the new version


# Update version in build.gradle
def bump_from_build_gradle(file_path: str, bump_type: str):
    with open(file_path, "r") as f:
        data = f.read()
    pattern = re.compile(r"version = '(\d+)\.(\d+)\.(\d+)'")
    matched = pattern.search(data)
    if matched:
        old_version = f"{matched.group(1)}.{matched.group(2)}.{matched.group(3)}"
    else:
        old_version = "0.0.0"
    new_version = bump_version(old_version, bump_type)
    updated_data = pattern.sub(f"version = '{new_version}'", data)
    with open(file_path, "w", encoding="UTF-8") as f:
        f.write(updated_data)
    return new_version  # Return the new version


def main():
    parser = argparse.ArgumentParser(description="Bump version of a package")
    parser.add_argument("--file_path", required=True, type=str, help="The path to the file to bump version")
    parser.add_argument(
        "--type", required=True, type=str, choices=["major", "minor", "patch"], help="The type of version bump"
    )
    args = parser.parse_args()

    file_path = args.file_path
    bump_type = args.type

    file_name = os.path.basename(file_path)
    if file_name == "package.json":
        new_version = bump_from_package_json(file_path, bump_type)
    elif file_name == "build.gradle":
        new_version = bump_from_build_gradle(file_path, bump_type)
    else:
        raise ValueError("Unsupported file for version bumping.")

    print(new_version)  # Output the new version


if __name__ == "__main__":
    main()
