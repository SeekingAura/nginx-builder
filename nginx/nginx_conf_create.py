import os
from pathlib import Path
from typing import (
    Any,
    Union,
)

from dotenv import (
    find_dotenv,
    load_dotenv,
)

# Get root of repository
BASE_DIR: Path = Path(__file__).resolve().parent.parent
load_dotenv(
    find_dotenv(
        filename=os.path.join(
            BASE_DIR,
            ".env_nginx_py",
        ),
    ),
)

DIST_DIR: str = "dist"
NGINX_DIR: str = os.path.join(BASE_DIR, "nginx")
CONFS_DIR: str = os.path.join(NGINX_DIR, "confs")
CONFS_TEMPLATE_DIR: str = os.path.join(NGINX_DIR, "confs_template")

# Template config
with open(file=os.path.join(CONFS_TEMPLATE_DIR, "single_language.conf"), mode="r") as inp:
    single_language_template_conf = inp.read()
# .format(
#     main_domains="www.example.com example.com",
#     main_host="example.com",
#     project_name="sample_name",
#     additional_conf="",
# )

with open(file=os.path.join(CONFS_TEMPLATE_DIR, "multi_language.conf"), mode="r") as inp:
    multi_language_template_conf = inp.read()

# .format(
#     main_domains="www.example.com example.com",
#     main_host="example.com",
#     project_name="sample_name",
#     additional_conf="",
# )
additional_conf: dict[str, str] = {}

with open(os.path.join(CONFS_TEMPLATE_DIR, "additional_landing.conf"), "r") as inp:
    additional_conf["landing"] = inp.read()

with open(os.path.join(CONFS_TEMPLATE_DIR, "redirect.conf"), "r") as inp:
    redirect_template_conf = inp.read()

# .format(
#     redirect_domains="",
#     main_domain="",
#     redirect_host="",
# )

main_conf_mandatory: tuple[str, ...] = (
    "main_hosts",
    "main_domain",
    "project_name",
)
MAIN_CONF_EXTRA: str = "additional_conf"

redirect_conf_mandatory: tuple[str, ...] = (
    "redirect_hosts",
    "main_host",
    "redirect_domain",
)

languages: tuple[str, ...] = (
    "es",
    "en",
    "pt",
)

def main_get_config(
    main_conf_mandatory: tuple[str, ...],
    main_config_dict: dict[str, Union[str, None]],
    project_names_i: str,
    project_names_env_i: str,
):
    for conf_i in main_conf_mandatory:
        main_config_dict[conf_i] = os.getenv(f"{project_names_env_i}_{conf_i.upper()}", None)
        if main_config_dict.get(conf_i) is None:
            raise NameError(f"Not found env var for {project_names_env_i}_{conf_i.upper()}")
    main_config_dict[MAIN_CONF_EXTRA] = additional_conf.get(project_names_i, "").format()


def redirect_get_conf(
    redirect_conf_mandatory: tuple[str, ...],
    redirect_config_list: list[dict[str, str]],
    project_names_env_i: str,
):
    """
    examples

    - ADMIN_BETENLACE_REDIRECT_HOST_COUNT
    - ADMIN_BETENLACE_REDIRECT_0_VAR
    """
    redirect_hosts_count = int(os.getenv(f"{project_names_env_i}_REDIRECT_HOST_COUNT", 0))
    for redirect_number in range(redirect_hosts_count):
        config_dict_i: dict[str, str] = {}
        for conf_i in redirect_conf_mandatory:
            env_key_i = f"{project_names_env_i}_REDIRECT_{redirect_number}_{conf_i.upper()}"
            env_value_i: Union[str, None] = os.getenv(env_key_i, None)
            if env_value_i is None:
                checks = [key_i in redirect_conf_mandatory for key_i in config_dict_i.keys()]
                if any(checks):
                    raise NameError(f"Has incomplete config for Redirect cases for {env_key_i}")
                raise NameError(f"Not found env var for {env_key_i} check redirect counts")
            config_dict_i[conf_i] = env_value_i

        redirect_config_list.append(config_dict_i)


def multi_language_check(
    dist_dir: str,
    project_name: str,
):
    dist_path: str = os.path.join(dist_dir, project_name)
    dist_languages: list[str] = os.listdir(dist_path)
    if (len(dist_languages) == 0):
        return False
    return bool(dist_languages[1] in languages)
    


def build_config(
    template_conf: str,
    project_name: str,
    config_dict: dict[str, str],
    path: str = "",
    config_name: str = "main",
):
    file_full_path: str = os.path.join(path, f"{project_name}_{config_name}.conf")
    with open(file_full_path, "w") as out:
        out.write(
            template_conf.format(
                **config_dict,
            )
        )


def build_config_multiple(
    template_conf: str,
    project_name: str,
    config_list: list[dict[str, str]],
    path: str = "",
    config_name: str = "main",
):
    file_full_path = os.path.join(path, f"{project_name}_{config_name}.conf")
    with open(file_full_path, "w") as out:
        for config_i in config_list:
            out.write(
                template_conf.format(
                    **config_i,
                )
            )


if __name__ == "__main__":
    # Delete current conf files
    for f in Path(os.path.join(NGINX_DIR, "confs")).glob("*.conf"):
        os.remove(f)
    project_names: list[str] = os.listdir(DIST_DIR)
    project_names_env = list(map(lambda x: x.replace("-", "_").upper(), project_names))
    # dict[str, dict[str, Union[dict[str, Union[str, None, ], ], list[dict[str, Union[str, None, ], ]], ]]]
    project_data: dict[str, dict[str, Any]] = {}
    # Main domains
    for project_names_i, project_names_env_i in zip(project_names, project_names_env):
        project_data[project_names_i] = {}
        project_data[project_names_i]["main_config"] = {}

        # Main host
        main_get_config(
            main_conf_mandatory=main_conf_mandatory,
            main_config_dict=project_data[project_names_i]["main_config"],
            project_names_i=project_names_i,
            project_names_env_i=project_names_env_i,
        )
        project_data[project_names_i]["redirect_configs"] = []
        # Redirect cases
        redirect_get_conf(
            redirect_conf_mandatory=redirect_conf_mandatory,
            redirect_config_list=project_data[project_names_i]["redirect_configs"],
            project_names_env_i=project_names_env_i,
        )
        # Build config
        is_multi_language = multi_language_check(DIST_DIR, project_names_i)
        if is_multi_language:
            template_conf = multi_language_template_conf
        else:
            template_conf = single_language_template_conf
        build_config(
            template_conf=template_conf,
            project_name=project_names_i,
            config_dict=project_data[project_names_i]["main_config"],
            path=CONFS_DIR,
            config_name="main",
        )

        for redirect_conf_i in project_data[project_names_i]["redirect_configs"]:
            build_config_multiple(
                template_conf=redirect_template_conf,
                project_name=project_names_i,
                config_list=project_data[project_names_i]["redirect_configs"],
                path=CONFS_DIR,
                config_name="redirect",
            )
