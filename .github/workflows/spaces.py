"""Module spaces.py"""
import logging

import fire
import huggingface_hub


def main(repo_id: str, token: str, repo_type: str, folder_path: str):
    """

    :param repo_id:
    :param token:
    :param repo_type:
    :param folder_path:
    :return:
    """

    url = huggingface_hub.create_repo(
        repo_id=repo_id, token=token, private=False, repo_type=repo_type, exist_ok=True, space_sdk='gradio')
    logging.info(url)

    destination = huggingface_hub.upload_folder(
        repo_id=repo_id, folder_path=folder_path, commit_message='Updating', token=token, repo_type=repo_type,
        ignore_patterns=["*.safetensors", ".gitattributes"]
    )
    logging.info(destination)

    for element in ['app.py', 'README.md', 'requirements.txt']:
        element_ = huggingface_hub.upload_file(
            path_or_fileobj=element, path_in_repo=element,repo_id=repo_id, token=token, repo_type=repo_type )
        logging.info(element_)


if __name__ == '__main__':

    fire.Fire(main)
