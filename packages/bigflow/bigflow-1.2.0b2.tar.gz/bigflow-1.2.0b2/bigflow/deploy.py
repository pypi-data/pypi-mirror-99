import logging
from pathlib import Path

from google.cloud.storage import Bucket
from google.oauth2 import credentials
from subprocess import run, CompletedProcess
import requests
from typing import List
from google.cloud import storage

import bigflow.commons as bf_commons
from .commons import decode_version_number_from_file_name, remove_docker_image_from_local_registry, build_docker_image_tag


logger = logging.getLogger(__name__)


def load_image_from_tar(image_tar_path: str) -> str:
    logger.info("Load docker image from %s...", image_tar_path)
    for line in bf_commons.run_process(['docker', 'load', '-i', image_tar_path]).split('\n'):
        if 'Loaded image ID:' in line:
            return line.split()[-1].split(':')[-1]
    raise ValueError(f"Can't load image: {image_tar_path}")


def tag_image(image_id, repository, tag):
    return bf_commons.run_process(["docker", "tag", image_id,  f"{repository}:{tag}"])


def deploy_docker_image(
        image_tar_path: str,
        docker_repository: str,
        auth_method: str = 'local_account',
        vault_endpoint: str = None,
        vault_secret: str = None):
    build_ver = decode_version_number_from_file_name(Path(image_tar_path))
    build_ver = build_ver.replace("+", "-")  # fix local version separator
    image_id = load_image_from_tar(image_tar_path)
    try:
        return _deploy_image_loaded_to_local_registry(build_ver, docker_repository, image_id, auth_method,
                                                      vault_endpoint, vault_secret)
    finally:
        remove_docker_image_from_local_registry(build_docker_image_tag(docker_repository, build_ver))


def _deploy_image_loaded_to_local_registry(build_ver, docker_repository, image_id, auth_method, vault_endpoint,
                                           vault_secret):
    tag_image(image_id, docker_repository, build_ver)
    docker_image = docker_repository + ":" + build_ver
    print(f"Deploying docker image tag={docker_image} auth_method={auth_method}")
    if auth_method == 'local_account':
        bf_commons.run_process(['gcloud', 'auth', 'configure-docker'])

    elif auth_method == 'vault':
        oauthtoken = get_vault_token(vault_endpoint, vault_secret)
        bf_commons.run_process(
            ['docker', 'login', '-u', 'oauth2accesstoken', '--password-stdin', 'https://eu.gcr.io'],
            input=oauthtoken,
        )

    else:
        raise ValueError('unsupported auth_method: ' + auth_method)
    bf_commons.run_process(['docker', 'push', docker_image])

    return docker_image


def deploy_dags_folder(dags_dir: str, dags_bucket: str, project_id: str, clear_dags_folder: bool = False,
                       auth_method: str = 'local_account', vault_endpoint: str = None, vault_secret: str = None,
                       gs_client=None):

    print(f"Deploying DAGs folder, auth_method={auth_method}, clear_dags_folder={clear_dags_folder}, dags_dir={dags_dir}")

    client = gs_client or create_storage_client(auth_method, project_id, vault_endpoint, vault_secret)
    bucket = client.bucket(dags_bucket)

    if clear_dags_folder:
        clear_remote_dags_bucket(bucket)

    upload_dags_folder(dags_dir, bucket)
    return dags_bucket


def clear_remote_dags_bucket(bucket: Bucket):
    i = 0
    for blob in bucket.list_blobs(prefix='dags'):
        if not blob.name in ['dags/', 'dags/airflow_monitoring.py']:
            print(f"deleting file {_blob_uri(blob)}")
            blob.delete()
            i += 1

    print(f"{i} files deleted")


def _blob_uri(blob):
    return f"gs://{blob.bucket.name}/{blob.name}"


def upload_dags_folder(dags_dir: str, bucket: Bucket):
    dags_dir_path = Path(dags_dir)

    def upload_file(local_file_path, target_file_name):
        blob = bucket.blob(target_file_name)
        blob.upload_from_filename(local_file_path, content_type='application/octet-stream')
        print(f"uploading file {local_file_path} to {_blob_uri(blob)}")

    files = list(filter(Path.is_file, dags_dir_path.iterdir()))
    for f in files:
        upload_file(f.as_posix(), 'dags/' + f.name)

    print(f"{len(files)} files uploaded")


def create_storage_client(auth_method: str, project_id: str, vault_endpoint: str, vault_secret: str):
    if auth_method == 'local_account':
        return storage.Client(project=project_id)
    elif auth_method == 'vault':
        oauthtoken = get_vault_token(vault_endpoint, vault_secret)
        return storage.Client(project=project_id, credentials=credentials.Credentials(oauthtoken))
    else:
        raise ValueError('unsupported auth_method: ' + auth_method)


def get_vault_token(vault_endpoint: str, vault_secret: str):
    if not vault_endpoint:
        raise ValueError('vault_endpoint is required')
    if not vault_secret:
        raise ValueError('vault_secret is required')

    headers = {'X-Vault-Token': vault_secret}
    response = requests.get(vault_endpoint, headers=headers, verify=False)

    if response.status_code != 200:
        print(response.text)
        raise ValueError(
            'Could not get vault token, response code: {}'.format(
                response.status_code))

    print(f"get oauth token from {vault_endpoint} status_code={response.status_code}")
    return response.json()['data']['token']
