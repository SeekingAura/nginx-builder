import os
import shutil
import logging


def multi_language(
    project_assets: str,
    dist_path: str,
    dist_languages: list[str],
) -> None:
    end_folder: str = os.path.split(project_assets)[-1]
    for dist_language_i in dist_languages:
        destination_path = os.path.join(dist_path, dist_language_i, end_folder)
        # Check if file already exists
        if os.path.isdir(destination_path):
            logging.warning(f"{destination_path}, exists in the destination path!")
            shutil.rmtree(
                path=destination_path,
            )
        shutil.copytree(
            src=project_assets,
            dst=destination_path,
        )


def single_language(
    project_assets: str,
    dist_path: str,
) -> None:
    end_folder: str = os.path.split(project_assets)[-1]
    destination_path: str = os.path.join(dist_path, end_folder)
    # Check if file already exists
    if os.path.isdir(destination_path):
        logging.warning(f"{destination_path}, exists in the destination path!")
        shutil.rmtree(
            path=destination_path,
        )
    shutil.copytree(
        src=project_assets,
        dst=os.path.join(dist_path, end_folder),
    )


if __name__ == "__main__":
    PROJECTS_DIR: str = "projects"
    DIST_DIR: str = "dist"
    project_names: list[str] = os.listdir(DIST_DIR)
    languages: tuple[str, ...] = (
        "es",
        "en",
        "pt",
    )

    for project_name_i in project_names:
        dist_path: str = os.path.join(DIST_DIR, project_name_i)
        dist_languages: list[str] = os.listdir(dist_path)
        project_assets: str = os.path.join(
            PROJECTS_DIR, project_name_i, "src", "assets"
        )
        if dist_languages[1] in languages:
            multi_language(
                project_assets=project_assets,
                dist_path=dist_path,
                dist_languages=dist_languages,
            )
        else:
            single_language(
                project_assets=project_assets,
                dist_path=dist_path,
            )
