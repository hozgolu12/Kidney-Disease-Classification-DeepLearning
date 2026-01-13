import os
from box.exceptions import BoxValueError
from box import ConfigBox
import yaml
from cnnClassifier import logger
import json
import joblib
from ensure import ensure_annotations
from typing import Any
from pathlib import Path
import base64

@ensure_annotations
def read_yaml(path_to_yaml: Path) -> ConfigBox:
    """Reads a yaml file and returns a ConfigBox object

    Args:
        path_to_yaml (Path): Path to the yaml file

    Raises:
        e: Raises an exception if the file is not found or if there is an error in reading the file

    Returns:
        ConfigBox: ConfigBox object containing the contents of the yaml file
    """
    try:
        with open(path_to_yaml, "r") as yaml_file:
            content = yaml.safe_load(yaml_file)
            logger.info(f"yaml file: {path_to_yaml} loaded successfully")
            return ConfigBox(content)
    except BoxValueError as e:
        raise e
    except Exception as e:
        raise e

def write_yaml(path_to_yaml: Path, content: Any) -> None:
    """Writes a dictionary to a yaml file

    Args:
        path_to_yaml (Path): Path to the yaml file
        content (Any): Content to be written to the yaml file

    Raises:
        e: Raises an exception if there is an error in writing the file
    """
    try:
        os.makedirs(os.path.dirname(path_to_yaml), exist_ok=True)
        with open(path_to_yaml, "w") as yaml_file:
            yaml.safe_dump(content, yaml_file)
            logger.info(f"yaml file: {path_to_yaml} written successfully")
    except Exception as e:
        raise e

def save_json(path_to_json: Path, data: dict) -> None:  
    """Saves a dictionary to a json file

    Args:
        path_to_json (Path): Path to the json file
        data (dict): Dictionary to be saved to the json file

    Raises:
        e: Raises an exception if there is an error in writing the file
    """
    try:
        dir_name = os.path.dirname(path_to_json)
        if dir_name:
            os.makedirs(dir_name, exist_ok=True)
        with open(path_to_json, "w") as json_file:
            json.dump(data, json_file, indent=4)
            logger.info(f"json file: {path_to_json} saved successfully")
    except Exception as e:
        raise e
    
def create_directories(path_to_directories: list) -> None:
    """Creates directories

    Args:
        path_to_directories (list): List of paths to the directories to be created
    """
    for path in path_to_directories:
        os.makedirs(path, exist_ok=True)
        logger.info(f"Directory: {path} created successfully")

@ensure_annotations
def load_json(path_to_json: Path) -> dict:
    """Loads a json file and returns its contents as a dictionary

    Args:
        path_to_json (Path): Path to the json file

    Raises:
        e: Raises an exception if the file is not found or if there is an error in reading the file

    Returns:
        dict: Dictionary containing the contents of the json file
    """
    try:
        with open(path_to_json, "r") as json_file:
            content = json.load(json_file)
            logger.info(f"json file: {path_to_json} loaded successfully")
            return content
    except Exception as e:
        raise e
    
def save_bin(data: Any, path: Path) -> None:
    """Saves data to a binary file using joblib

    Args:
        data (Any): Data to be saved
        path (Path): Path to the binary file

    Raises:
        e: Raises an exception if there is an error in writing the file
    """
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        joblib.dump(data, path)
        logger.info(f"binary file: {path} saved successfully")
    except Exception as e:
        raise e
    
@ensure_annotations
def load_bin(path: Path) -> Any:
    """Loads data from a binary file using joblib

    Args:
        path (Path): Path to the binary file

    Raises:
        e: Raises an exception if the file is not found or if there is an error in reading the file

    Returns:
        Any: Data loaded from the binary file
    """
    try:
        with open(path, "rb") as f:
            content = joblib.load(f)
            logger.info(f"binary file: {path} loaded successfully")
            return content
    except Exception as e:
        raise e
    
@ensure_annotations
def get_size(path: Path) -> str:
    """Returns the size of a file in KB

    Args:
        path (Path): Path to the file

    Raises:
        e: Raises an exception if the file is not found or if there is an error in getting the file size

    Returns:
        str: Size of the file in KB
    """
    try:
        size_in_kb = round(os.path.getsize(path) / 1024)
        logger.info(f"File: {path} has size: {size_in_kb} KB")
        return f"~ {size_in_kb} KB"
    except Exception as e:
        raise e
    
@ensure_annotations
def decodeImage(imgstring: str, fileName: str):
    imgdata = base64.b64decode(imgstring)
    with open(fileName, 'wb') as f:
        f.write(imgdata)
        f.close()
    
@ensure_annotations
def encodeImageInBase64(image_path: Path) -> str:
    """Encodes an image to a base64 string

    Args:
        image_path (Path): Path to the image file

    Returns:
        str: Base64 encoded image string
    """
    try:
        with open(image_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
            return encoded_string
    except Exception as e:
        raise e