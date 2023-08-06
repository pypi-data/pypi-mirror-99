## ``gen_doc`` - library for creating documentation

### Installation

```commandline
pip install gen_doc
```

### What for?
+ aggregates all `.py` files to one (or same hierarchy folder) `.md` files
+ collects all classes and methods with information about them


### Details
```commandline
>>> gen_doc -h
usage: Documentation builder [-h] [-p PATH_TO_ROOT_FOLDER]
                             [-r REPOSITORY_MAIN_URL] [-t TITLE]
                             [-p2s PATH_TO_SAVE] [-f2s FILE_TO_SAVE]
                             [-hi EXTRACT_WITH_SAME_HIERARCHY]
                             [-o OVERWRITE_IF_FILE_EXISTS]
                             {py}

positional arguments:
  {py}                  for which language to create documentation
optional arguments:
  -h, --help            show this help message and exit
  -p PATH_TO_ROOT_FOLDER, --path_to_root_folder PATH_TO_ROOT_FOLDER
                        path to the directory for which documentation should
                        be compiled
  -r REPOSITORY_MAIN_URL, --repository_main_url REPOSITORY_MAIN_URL
                        url of the repository where this project is located
  -t TITLE, --title TITLE
                        title for header (if `-hi False`)
  -p2s PATH_TO_SAVE, --path_to_save PATH_TO_SAVE
                        path to the directory where to save
  -f2s FILE_TO_SAVE, --file_to_save FILE_TO_SAVE
                        name_file to save (if `-hi False`)
  -hi EXTRACT_WITH_SAME_HIERARCHY, --extract_with_same_hierarchy EXTRACT_WITH_SAME_HIERARCHY
                        if False extract all to one file if True create file
                        for every file
  -o OVERWRITE_IF_FILE_EXISTS, --overwrite_if_file_exists OVERWRITE_IF_FILE_EXISTS
                        for overwriting if file exist
```