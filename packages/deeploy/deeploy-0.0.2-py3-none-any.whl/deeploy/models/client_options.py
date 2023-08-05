from typing import Optional, List, Any

from pydantic import BaseModel


class ClientConfig(BaseModel):
    """
    Class containing the Deeploy client options

    Attributes:
      access_key: string representing the personal access key
      secret_key: string representing the personal secret key
      host: string representing the domain on which Deeploy is hosted
      workspace_id: string representing the workspace id in which to create
        deployments
      local_repository_path: string representing the relative or absolute path
        to the local git repository
      branch_name: string representing the branch name on which to commit. Defaults
        to the local active branch
    """
    access_key: str
    secret_key: str
    host: str
    workspace_id: str
    local_repository_path: str
    repository_id: str
    branch_name: Optional[str]
