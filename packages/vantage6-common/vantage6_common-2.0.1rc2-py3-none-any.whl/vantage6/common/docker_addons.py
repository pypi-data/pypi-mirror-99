import logging
import re
import docker
import requests
import base64
import json

from dateutil.parser import parse
from requests.api import request

from vantage6.common import logger_name
from vantage6.common import ClickLogger

logger = logger_name(__name__)
log = logging.getLogger(logger)

docker_client = docker.from_env()

def registry_basic_auth_header(docker_client, registry):
    """Obtain credentials for registry

    This is a wrapper around docker-py to obtain the credentials used
    to access a registry. Normally communication to the registry goes
    through the Docker deamon API (locally), therefore we have to take
    extra steps in order to communicate with the (Harbor) registry
    directly.

    Note that this has only been tested for the harbor registries.

    Parameters
    ----------
    registry : str
        registry name (e.g. harbor.vantage6.ai)

    Returns
    -------
    dict
        Containing a basic authorization header
    """

    # Obtain the header used to be send to the docker deamon. We
    # communicate directly with the registry therefore we need to
    # change this headers.
    header = docker.auth.get_config_header(docker_client.api, registry)
    if not header:
        log.debug(f'No credentials found for {registry}')
        return

    # decode header
    header_json = json.loads(base64.b64decode(header))

    # Extract username and password
    try:
        username = header_json.get('username')
    except KeyError:
        username = header_json.get('Username')

    try:
        password = header_json['password']
    except KeyError:
        password = header_json['Password']

    basic_auth = f"{username}:{password}"

    # Encode them back to base64 and as a dict
    bytes_basic_auth = basic_auth.encode("utf-8")
    b64_basic_auth = base64.b64encode(bytes_basic_auth).decode("utf-8")

    return {'authorization': f'Basic {b64_basic_auth}'}


def inspect_remote_image_timestamp(docker_client, image: str, log=ClickLogger):
    """
    Obtain creation timestamp object from remote image.

    Parameters
    ----------
    reg : str
        registry where the image is hosted
    rep : str
        repository in the registry
    img : str
        image name
    tag : str, optional
        image tag to be used, by default "latest"

    Returns
    -------
    datetime
        timestamp object containing the creation date and time of the image
    """
    # check if a tag has been profided

    image_tag = re.split(":", image)
    img = image_tag[0]
    tag = image_tag[1] if len(image_tag) == 2 else "latest"

    try:
        reg, rep, img_ = re.split("/", img)
    except ValueError:
        log.warn("Could not construct remote URL, "
                 "are you using a local image?")
        log.warn("Or an image from docker hub?")
        log.warn("We'll make an final attemt when running the image to pull"
                 " it without any checks...")
        return

    # figure out API of the docker repo
    v1_check = requests.get(f"https://{reg}/api/health")
    v1 = v1_check.status_code == 200
    v2 = False
    if not v1:
        v2_check = requests.get(f"https://{reg}/api/v2.0/health")
        v2 = v2_check.status_code == 200

    if not v1 and not v2:
        log.error(f"Could not determine version of the registry! {reg}")
        log.error(f"Is this a Harbor registry?")
        log.error(f"Or is the harbor server offline?")
        return

    if v1:
        image = f"https://{reg}/api/repositories/{rep}/{img_}/tags/{tag}"
    else:
        image = f"https://{reg}/api/v2.0/projects/{rep}/repositories/" \
                f"{img_}/artifacts/{tag}"

    # retrieve info from the Harbor server
    result = requests.get(image, headers=\
        registry_basic_auth_header(docker_client, reg))

    # verify that we got an result
    if result.status_code == 404:
        log.warn(f"Remote image not found! {image}")
        return

    if result.status_code != 200:
        log.warn(f"Remote info could not be fetched! ({result.status_code}) "
                 f"{image}")
        return

    if v1:
        timestamp = parse(result.json().get("created"))
    else:
        timestamp = parse(result.json().get("extra_attrs").get("created"))
    return timestamp


def inspect_local_image_timestamp(docker_client, image: str, log=ClickLogger):
    """
    Obtain creation timestamp object from local image.

    Parameters
    ----------
    reg : str
        registry where the image is hosted
    rep : str
        repository in the registry
    img : str
        image name
    tag : str, optional
        image tag to be used, by default "latest"

    Returns
    -------
    datetime
        timestamp object containing the creation date and time of the image
    """
    # p = re.split(r"[/:]", image)
    # if len(p) == 4:
    #     image = f"{p[0]}/{p[1]}/{p[2]}:{p[3]}"

    try:
        img = docker_client.images.get(image)
    except docker.errors.ImageNotFound:
        log.debug(f"Local image does not exist! {image}")
        return None
    except docker.errors.APIError:
        log.debug(f"Local info not available! {image}")
        return None

    timestamp = img.attrs.get("Created")
    timestamp = parse(timestamp)
    return timestamp


def pull_if_newer(docker_client, image: str, log=ClickLogger):
    """
    Docker pull only if the remote image is newer.

    Parameters
    ----------
    image : str
        image to be pulled
    """

    local_ = inspect_local_image_timestamp(docker_client, image, log=log)
    remote_ = inspect_remote_image_timestamp(docker_client, image, log=log)
    pull = False
    if local_ and remote_:
        if remote_ > local_:
            log.debug(f"Remote image is newer: {image}")
            pull = True
        elif remote_ == local_:
            log.debug(f"Local image is up-to-date: {image}")
        elif remote_ < local_:
            log.warn(f"Local image is newer! Are you testing? {image}")
    elif local_:
        log.warn(f"Only a local image has been found! {image}")
    elif remote_:
        log.debug("No local image found, pulling from remote!")
        pull = True
    elif not local_ and not remote_:
        log.error(f"Cannot locate image {image}")

    if pull:
        try:
            docker_client.images.pull(image)
        except docker.errors.APIError as e:
            log.error(f"Failed to pull image! {image}")
            log.debug(e)
