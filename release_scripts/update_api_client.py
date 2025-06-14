import subprocess
from pathlib import Path

import toml
import yaml

PACKAGE_FOLDER = Path(__file__).parents[1] / "src/bitpanda_api"
API_FOLDER = PACKAGE_FOLDER / "api"
TEMP_FOLDER = PACKAGE_FOLDER.parent / "temp"


def move_non_generated_files_to_temp_folder() -> dict[Path, Path]:
    # Find all of the files that end with _many in the api_folder
    files_to_move = [
        file for file in API_FOLDER.rglob("*.py") if file.is_file() and "_many" in file.stem
    ]

    TEMP_FOLDER.mkdir(parents=True, exist_ok=True)
    file_sources = {}

    # Move the files to the temp folder
    for file in files_to_move:
        original_path = file.relative_to(API_FOLDER)
        new_path = file.rename(TEMP_FOLDER / file.name)
        file_sources[original_path] = new_path.relative_to(TEMP_FOLDER)

    return file_sources


def move_files_from_temp_folder(mapping: dict[Path, Path]):
    for original_path, temp_path in mapping.items():
        temp_file = TEMP_FOLDER / temp_path
        original_file = API_FOLDER / original_path

        temp_file.rename(original_file)

    # Delete the temp folder
    TEMP_FOLDER.rmdir()


def generate_client(openapi_file: Path):
    subprocess.run(
        [
            "openapi-python-client",
            "generate",
            "--overwrite",
            "--path",
            openapi_file.as_posix(),
            "--output-path",
            PACKAGE_FOLDER.as_posix(),
            "--meta",
            "none",
        ],
        capture_output=True,
    )


def update_project_version(version: str):
    pyproject_path = Path(__file__).parents[1] / "pyproject.toml"

    with open(pyproject_path, "r") as file:
        pyproject_data = toml.load(file)

    pyproject_data["project"]["version"] = version

    with open(pyproject_path, "w") as file:
        toml.dump(pyproject_data, file)


def read_api_version(openapi_data: dict) -> str:
    return openapi_data["info"]["version"]


def main():
    openapi_path = Path(__file__).parent / "openapi.yaml"
    if not openapi_path.exists():
        raise FileNotFoundError("OpenAPI schema not found -> Run 'download_openapi.py' first")

    with openapi_path.open("r") as file:
        openapi_data = yaml.safe_load(file)

    api_version = read_api_version(openapi_data)

    file_mapping = move_non_generated_files_to_temp_folder()

    print(f"Generating API Client: {api_version}")

    generate_client(openapi_path)
    update_project_version(api_version)

    move_files_from_temp_folder(file_mapping)

    print(f"Updated project version to: {api_version}")


if __name__ == "__main__":
    main()
