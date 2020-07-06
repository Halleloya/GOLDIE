from .models import ThingDescription, DirectoryNameToURL, TargetToChildName, TypeToChildrenNames
from flask_pymongo import PyMongo

mongo = PyMongo()

def clear_database() -> None:
    """Drop collections in the mongodb database in order to initialize it.
    
    """
    ThingDescription.drop_collection()
    DirectoryNameToURL.drop_collection()
    TypeToChildrenNames.drop_collection()


def init_dir_to_url(level: str) -> None:
    """Initialize name-to-URL mappings for the current directory using contents specified by 'level'
    
    Args:
        level(str): it specifies the level of current directory
    """

    DirectoryNameToURL.drop_collection()
    if level == "level1":
        DirectoryNameToURL(directory_name='master',
                           url=f'http://localhost:5001', relationship='master').save()
        DirectoryNameToURL(directory_name='level2',
                           url='http://localhost:5002', relationship='child').save()
    elif level == 'level2':
        DirectoryNameToURL(directory_name='master',
                           url=f'http://localhost:5001', relationship='master').save()
        DirectoryNameToURL(directory_name='level1',
                           url=f'http://localhost:5001', relationship='parent').save()
        DirectoryNameToURL(directory_name='level3',
                           url=f'http://localhost:5003', relationship='child').save()
    elif level == 'level3':
        DirectoryNameToURL(directory_name='master',
                           url=f'http://localhost:5001', relationship='master').save()
        DirectoryNameToURL(directory_name='level2',
                           url=f'http://localhost:5002', relationship='parent').save()
        DirectoryNameToURL(directory_name='level4a',
                           url=f'http://localhost:5004', relationship='child').save()
        DirectoryNameToURL(directory_name='level4b',
                           url=f'http://localhost:5005', relationship='child').save()
    elif level == 'level4a':
        DirectoryNameToURL(directory_name='master',
                           url=f'http://localhost:5001', relationship='master').save()
        DirectoryNameToURL(directory_name='level3',
                           url=f'http://localhost:5003', relationship='parent').save()
        DirectoryNameToURL(directory_name='level5a',
                           url=f'http://localhost:5006', relationship='child').save()
    elif level == 'level4b':
        DirectoryNameToURL(directory_name='master',
                           url=f'http://localhost:5001', relationship='master').save()
        DirectoryNameToURL(directory_name='level3',
                           url=f'http://localhost:5003', relationship='parent').save()
        DirectoryNameToURL(directory_name='level5b',
                           url=f'http://localhost:5007', relationship='child').save()
    elif level == 'level5a':
        DirectoryNameToURL(directory_name='master',
                           url=f'http://localhost:5001', relationship='master').save()
        DirectoryNameToURL(directory_name='level4a',
                           url=f'http://localhost:5004', relationship='parent').save()
    elif level == 'level5b':
        DirectoryNameToURL(directory_name='master',
                           url=f'http://localhost:5001', relationship='master').save()
        DirectoryNameToURL(directory_name='level4b',
                           url=f'http://localhost:5005', relationship='parent').save()


def init_target_to_child_name(level: str) -> None:
    """Initialize the target-to-child mappings for the current directory

    Args:
        level(str): it specifies the level of current directory
    """
    if level == 'level1':
        TargetToChildName(target_name='level3', child_name='level2').save()
        TargetToChildName(target_name='level4a', child_name='level2').save()
        TargetToChildName(target_name='level4b', child_name='level2').save()
        TargetToChildName(target_name='level5a', child_name='level2').save()
        TargetToChildName(target_name='level5b', child_name='level2').save()
    elif level == 'level2':
        TargetToChildName(target_name='level4a', child_name='level3').save()
        TargetToChildName(target_name='level4b', child_name='level3').save()
        TargetToChildName(target_name='level5a', child_name='level3').save()
        TargetToChildName(target_name='level5b', child_name='level3').save()
    elif level == 'level3':
        TargetToChildName(target_name='level5a', child_name='level4a').save()
        TargetToChildName(target_name='level5b', child_name='level4b').save()
    elif level == 'level4a':
        pass
    elif level == 'level4b':
        pass
    elif level == 'level5a':
        pass
    elif level == 'level5b':
        pass
