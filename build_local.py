import argparse
import glob
import shutil
import subprocess
from typing import Any

# Parser config
parser: argparse.ArgumentParser = argparse.ArgumentParser(
    description="Make multi build",
)
parser.add_argument(
    "-s",
    "--scope",
    type=str,
    choices=(
        "admin",
        "partner",
        "all",
    ),
    default="all",
)
args: argparse.Namespace = parser.parse_args()

if __name__ == "__main__":
    if args.scope == "all":
        commands: tuple[tuple[str, ...], ...] = (
            ("npm", "run", "build", "--project", "project-0"),
            ("ng", "build", "--project", "project-1", "localize"),
        )
    else:
        raise AttributeError(f'Invalid scope value "{args.scope}"')

    shutil.rmtree(
        path="dist",
        ignore_errors=True,
    )

    subprocess.run(
        args=("npm", "cache", "clean", "--force"),
    )
    subprocess.run(
        args=("npm", "install", "--legacy-peer-deps"),
    )

    # run in parallel
    processes: list[Any] = [subprocess.Popen(args=cmd) for cmd in commands]
    # do other things here..
    # wait for completion
    for p in processes:
        p.wait()

    # Delete assets folder at dist by regex
    for folder_i in glob.glob(
        pathname="./dist/**/assets",
        recursive=True,
    ):
        shutil.rmtree(
            folder_i,
            ignore_errors=True,
        )

    # tar dist
    subprocess.run(
        args=("tar", "-czf", "dist.tar.gz", "dist"),
    )
