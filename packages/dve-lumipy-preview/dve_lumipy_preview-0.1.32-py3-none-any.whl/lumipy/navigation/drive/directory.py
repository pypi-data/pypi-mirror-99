from lumipy.navigation.drive.read import DriveRead
from lumipy.navigation.drive.save import DriveSave
from typing import Optional
import pandas as pd
from lumipy.common.lockable import Lockable
from lumipy.navigation.atlas import Atlas


class DriveDirectory(Lockable):
    """Class that represents a directory in drive with functionality around listing contents, file read data source
    for use in fluent query syntax and batch saving of table variables.

    """

    def __init__(self, atlas: Atlas, working_dir: Optional[str] = '/'):
        """__init__ method of the DriveDirectory class

        Args:
            atlas (Atlas): luminesce data providers atlas. Must contain Drive.File.
            working_dir (Optional[str]): working directory. Defaults to root: '/'.
        """
        self._client = atlas.get_client()
        self._atlas = atlas

        if not hasattr(atlas, 'drive_file'):
            raise ValueError("Atlas has no Drive.File provider - check permissions.")

        self._drive_files_cls = self._atlas.drive_file.get_class()
        self._pwd = working_dir

        super().__init__()

    def use_csv_file(self, file_path: str) -> DriveRead:
        """Use a CSV file in drive as a data provider.

        Args:
            file_path (str): File path in drive. If path str doesn't start with '/' (relative path) it will
            be relative to the current directory.

        Returns:
            DriveRead: DriveRead source table instance that represents the drive CSV data file.

        """

        if not file_path.endswith('.csv'):
            raise ValueError(f"Drive path input doesn't end in .csv: {file_path}")
        if not file_path.startswith('/'):
            in_path = f"{self._pwd}/{file_path}"
        else:
            in_path = file_path
        return DriveRead(in_path, self._client, 'csv')

    def use_excel_file(self, file_path: str, range_arg: str) -> DriveRead:
        """Use an excel file in drive as a data provider.

        Args:
            file_path (str): File path in drive. If path str doesn't start with '/' (relative path) it will
            be relative to the current directory.
            range_arg (str): Cell range or table in the excel document to return (e.g. 'A1:E9' or 'table_name')

        Returns:
            DriveRead: DriveRead source table instance that represents the drive excel data file.

        """
        if not file_path.endswith('.xlsx'):
            raise ValueError(f"Drive path input doesn't end in .xlsx: {file_path}")
        if not file_path.startswith('/'):
            in_path = f"{self._pwd}/{file_path}"
        else:
            in_path = file_path
        return DriveRead(in_path, self._client, 'excel', range_arg)

    def use_sqlite_file(self, file_path: str) -> DriveRead:
        """Use a sqlite in drive as a data provider.

        Args:
            file_path (str): File path in drive. If path str doesn't start with '/' (relative path) it will
            be relative to the current directory.

        Returns:
            DriveRead: DriveRead source table instance that represents the drive sqlite data file.

        """
        if not file_path.endswith('.sqlite'):
            raise ValueError(f"Drive path input doesn't end in .xlsx: {file_path}")
        if not file_path.startswith('/'):
            in_path = f"{self._pwd}/{file_path}"
        else:
            in_path = file_path
        return DriveRead(in_path, self._client, 'sqlite')

    def _list_content(self, path: Optional[str] = None, content_type=None, depth=0):
        if isinstance(path, str) and path.startswith('/'):
            in_path = path
        elif isinstance(path, str):
            in_path = self._pwd + path + '/'
        elif path is None:
            in_path = self._pwd
        else:
            raise ValueError("???")

        content = self._drive_files_cls(
            recurse_depth=depth,
            root_path=in_path
        )

        qry = content.select(
            content.full_path,
            content.type,
            content.size,
            content.created_on,
            content.updated_on
        )
        if content_type is not None:
            qry = qry.where(
                content.type == content_type
            )

        return qry.order_by(
            content.path.ascending(),
            content.name.ascending()
        ).go()

    def list_files(self, path: Optional[str] = None) -> pd.DataFrame:
        """Get information on the files in a drive folder

        Args:
            path (Optional[str]): path to the folder to list files from. Defaults to current location.

        Returns:
            DataFrame: dataframe containing data on files in the folder and their metadata.

        """
        return self._list_content(path, 'File')

    def list_folders(self, path=None) -> pd.DataFrame:
        """Get information on the folders in a drive folder

        Args:
            path (Optional[str]): path to the folder to list folders from. Defaults to current location.

        Returns:
            DataFrame: dataframe containing data on folders in the folder and their metadata.

        """
        return self._list_content(path, 'Folder')

    def list_all(self, path: Optional[str] = None) -> pd.DataFrame:
        """Get information on the files and folders in a drive folder

        Args:
            path (Optional[str]): path to the folder to list content from. Defaults to current location.

        Returns:
            DataFrame: dataframe containing data on all content in the folder and their metadata.

        """
        return self._list_content(path)

    def move_to_folder(self, path: str) -> 'DriveDirectory':
        """Change the current drive location to another drive folder.

        Args:
            path (str): path of the folder to change to. Can be a relative or absolute path.

        Returns:
            DriveDirectory: new directory object representing the folder you've moved into.

        """
        if path.startswith('/'):
            in_path = path
        else:
            in_path = self._pwd + path + '/'
        return DriveDirectory(self._atlas, in_path)

    def current_folder(self) -> str:
        """Return the current folder

        Returns:
            str: the path of the current folder
        """
        return self._pwd

    def search(self, target: str, path: Optional[str] = None) -> pd.DataFrame:
        """Search drive for paths that contain a target string (case-insensitive) and return these data as a DataFrame.

        Args:
            path (Optional[str]): path to search on. Can be relative or absolute path. Optional: will default to current
            location.
            target (str): the string to search the paths of the files and folders for.

        Returns:
            DataFrame: dataframe containing the search result data.
        """
        if path is None:
            search_dir = self._pwd
        elif path.startswith('/'):
            search_dir = path
        else:
            search_dir = self._pwd + '/' + path

        content = self._drive_files_cls(
            recurse_depth=99,
            root_path=search_dir
        )
        return content.select(
            content.full_path,
            content.type,
            content.size,
            content.created_on,
            content.updated_on
        ).where(
            content.full_path.like(f'%{target}%')
        ).order_by(
            content.path.ascending(),
            content.name.ascending()
        ).go()

    def batch_save(self, path: Optional[str] = None, file_type: Optional[str] = 'csv', **batch) -> DriveSave:
        """Create a drive save as expression that will save a collection of table variables to a directory as a given
        file format.

        Args:
            path (Optional[str]): path to where to save the data to - can be an absolute or relative path. Defaults to
            the current location.
            file_type: file type to save the table variables as (valid types are csv, sqlite and xlsx)
            **batch: batch of table variable expressions specified as keyword args. The keyword is to be the name of the
            file saved in drive.

        Returns:
            DriveSave: DriveSave instance representing the save as call to drive.
        """
        if len(batch) == 0:
            raise ValueError()

        if path is None:
            in_path = self._pwd
        elif path.startswith('/'):
            in_path = path
        else:
            in_path = self._pwd + path + '/'

        return DriveSave(in_path, self._client, file_type, **batch)
