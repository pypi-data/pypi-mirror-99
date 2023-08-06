# encoding: utf-8
import os
import json
import copy

import requests

from requests_toolbelt import MultipartEncoder

from ..compat import OK, BAD_REQUEST, NOT_FOUND, UNAUTHORIZED, CREATED, ACCEPTED, NO_CONTENT
from ..config import config

from . import authHeaders
from .TeamAPI import TeamAPI
from .exceptions.CxError import BadRequestError, NotFoundError, CxError
from .sast.projects.dto import CxUpdateProjectNameTeamIdRequest, CxCreateProjectResponse, \
    CxIssueTrackingSystemDetail, CxSharedRemoteSourceSettingsRequest, CxIssueTrackingSystemField, \
    CxSharedRemoteSourceSettingsResponse, CxGitSettings, \
    CxIssueTrackingSystemType, CxIssueTrackingSystemFieldAllowedValue, \
    CxCreateProjectRequest, CxIssueTrackingSystem, CxLink, CxCustomRemoteSourceSettings, \
    CxUpdateProjectRequest, CxProjectExcludeSettings, CxCredential, CxSVNSettings, CxURI, CxPerforceSettings, \
    CxTFSSettings, CxIssueTrackingSystemJira, CxPreset
from .sast.projects.dto import construct_cx_project


class ProjectsAPI(object):
    """
    the projects API
    """

    def __init__(self):
        """

        """
        self.retry = 0

    def get_all_project_details(self, project_name=None, team_id=None):
        """
        REST API: get all project details.
        For argument team_id, please consider using TeamAPI.get_team_id_by_full_name(team_full_name)

        Args:
            project_name (str, optional): Unique name of a specific project or projects
            team_id (int, str, optional): Unique Id of a specific team or teams.
                            default to id of the corresponding team full name in config.ini

        Returns:
            :obj:`list` of :obj:`CxProject`

        Raises:
            BadRequestError
            NotFoundError
            CxError
        """
        all_projects = []

        projects_url = config.get("base_url") + "/cxrestapi/projects"

        optionals = []
        if project_name:
            optionals.append("projectName=" + str(project_name))
        if team_id:
            optionals.append("teamId=" + str(team_id))
        if optionals:
            projects_url += "?" + "&".join(optionals)

        r = requests.get(
            url=projects_url,
            headers=authHeaders.get_v2_headers(),
            verify=config.get("verify")
        )
        if r.status_code == OK:
            a_list = r.json()
            all_projects = [
                construct_cx_project(item) for item in a_list
            ]
        elif r.status_code == BAD_REQUEST:
            raise BadRequestError(r.text)
        elif r.status_code == NOT_FOUND:
            response = r.json()
            raise CxError(response.get("messageDetails"), response.get("messageCode"))
        elif (r.status_code == UNAUTHORIZED) and (self.retry < config.get("max_try")):
            authHeaders.update_auth_headers()
            self.retry += 1
            self.get_all_project_details()
        else:
            raise CxError(r.text, r.status_code)

        self.retry = 0

        return all_projects

    def create_project_with_default_configuration(self, project_name, team_id=None, is_public=True):
        """
        REST API: create project

        Args:
            project_name (str):  Specifies the name of the project
            team_id (int, str): Specifies the id of the team that owns the project
                                default to the id of the team full name in config.ini
            is_public (boolean): Specifies whether the project is public or not
                                default True

        Returns:
            :obj:`CxCreateProjectResponse`

        Raises:
            BadRequestError
            NotFoundError
            CxError
        """
        project = None

        projects_url = config.get("base_url") + "/cxrestapi/projects"

        req_data = CxCreateProjectRequest(project_name, team_id, is_public).get_post_data()
        r = requests.post(
            url=projects_url,
            data=req_data,
            headers=authHeaders.auth_headers,
            verify=config.get("verify")
        )
        if r.status_code == CREATED:
            d = r.json()
            project = CxCreateProjectResponse(
                d.get("id"),
                CxLink(
                    rel=(d.get("link", {}) or {}).get("rel"),
                    uri=(d.get("link", {}) or {}).get("uri")
                )
            )
        elif r.status_code == BAD_REQUEST:
            raise BadRequestError(r.text)
        elif r.status_code == NOT_FOUND:
            raise NotFoundError()
        elif (r.status_code == UNAUTHORIZED) and (self.retry < config.get("max_try")):
            authHeaders.update_auth_headers()
            self.retry += 1
            self.create_project_with_default_configuration(project_name, team_id, is_public)
        else:
            raise CxError(r.text, r.status_code)

        self.retry = 0

        return project

    def get_project_id_by_project_name_and_team_full_name(self, project_name,
                                                          team_full_name=config.get("team_full_name")):
        """
        utility provided by SDK: get project id by project name, and team full name

        Args:
            project_name (str): project name under one team, different teams may have projects of the same name
            team_full_name (str): for example "/CxServer/SP/Company/Users"

        Returns:
            int: project id， if project not exists, return None
        """

        project_id = None

        team_id = TeamAPI().get_team_id_by_team_full_name(team_full_name=team_full_name)

        try:
            all_projects = self.get_all_project_details(project_name=project_name, team_id=team_id)

            if all_projects and len(all_projects) == 1:
                project_id = all_projects[0].project_id

        except CxError:
            pass

        return project_id

    def get_project_details_by_id(self, project_id):
        """
        REST API: get project details by project id

        Args:
            project_id (int):  Unique Id of the project

        Returns:
            :obj:`CxProject`

        Raises:
            BadRequestError
            NotFoundError
            CxError

        """
        project = None

        project_url = config.get("base_url") + "/cxrestapi/projects/{id}".format(id=project_id)

        r = requests.get(
            url=project_url,
            headers=authHeaders.get_v2_headers(),
            verify=config.get("verify")
        )
        if r.status_code == OK:
            a_dict = r.json()
            project = construct_cx_project(a_dict)
        elif r.status_code == BAD_REQUEST:
            raise BadRequestError(r.text)
        elif r.status_code == NOT_FOUND:
            raise NotFoundError()
        elif (r.status_code == UNAUTHORIZED) and (self.retry < config.get("max_try")):
            authHeaders.update_auth_headers()
            self.retry += 1
            self.get_project_details_by_id(project_id)
        else:
            raise CxError(r.text, r.status_code)

        self.retry = 0

        return project

    def update_project_by_id(self, project_id, project_name, team_id=None, custom_fields=None):
        """
        update project info by project id

        Args:
            project_id (int): Unique Id of the project
            project_name (str, optional): Specifies the name of the project
            team_id (int, str, optional): Specifies the Id of the team that owns the project
            custom_fields (:obj:`list` of :obj:`CxCustomField`, optional):  specifies the custom field details

        Returns:
            boolean: True means successful, False means not successful

        Raises:
            BadRequestError
            NotFoundError
            CxError
        """
        is_successful = False

        project_url = config.get("base_url") + "/cxrestapi/projects/{id}".format(id=project_id)

        request_body = CxUpdateProjectRequest(
            name=project_name,
            team_id=team_id,
            custom_fields=custom_fields
        ).get_post_data()

        r = requests.put(
            url=project_url,
            data=request_body,
            headers=authHeaders.auth_headers,
            verify=config.get("verify")
        )

        # In Python http module, HTTP status ACCEPTED is 202
        if r.status_code == NO_CONTENT:
            is_successful = True
        elif r.status_code == BAD_REQUEST:
            raise BadRequestError(r.text)
        elif r.status_code == NOT_FOUND:
            raise NotFoundError()
        elif (r.status_code == UNAUTHORIZED) and (self.retry < config.get("max_try")):
            authHeaders.update_auth_headers()
            self.retry += 1
            self.update_project_by_id(project_id, project_name, team_id, custom_fields)
        else:
            raise CxError(r.text, r.status_code)

        self.retry = 0

        return is_successful

    def update_project_name_team_id(self, project_id, project_name, team_id=None):
        """
        REST API: update project name, team id

        Args:
            project_id (int):  consider using ProjectsAPI.get_project_id_by_name
            project_name (str, optional): Specifies the name of the project
            team_id (int, str, optional): Specifies the Id of the team that owns the project

        Returns:
            boolean

        Raises:
            BadRequestError
            NotFoundError
            CxError
        """

        is_successful = False

        project_url = config.get("base_url") + "/cxrestapi/projects/{id}".format(id=project_id)

        request_body = CxUpdateProjectNameTeamIdRequest(
            project_name=project_name,
            owning_team=team_id
        ).get_post_data()

        r = requests.patch(
            url=project_url,
            data=request_body,
            headers=authHeaders.auth_headers,
            verify=config.get("verify")
        )

        # In Python http module, HTTP status ACCEPTED is 202
        if r.status_code == NO_CONTENT:
            is_successful = True
        elif r.status_code == BAD_REQUEST:
            raise BadRequestError(r.text)
        elif r.status_code == NOT_FOUND:
            raise NotFoundError()
        elif (r.status_code == UNAUTHORIZED) and (self.retry < config.get("max_try")):
            authHeaders.update_auth_headers()
            self.retry += 1
            self.update_project_name_team_id(project_id, project_name, team_id)
        else:
            raise CxError(r.text, r.status_code)

        self.retry = 0

        return is_successful

    def delete_project_by_id(self, project_id, delete_running_scans=False):
        """
        REST API: delete project by id

        Args:
            project_id (int):  Unique Id of the project
            delete_running_scans (boolean): Specifies whether running scans are to be deleted. Options are false/true.
                                Default=False, if not specified.

        Returns:
            boolean

        Raises:
            BadRequestError
            NotFoundError
            CxError
        """
        is_successful = False

        project_url = config.get("base_url") + "/cxrestapi/projects/{id}".format(id=project_id)

        request_body = json.dumps({"deleteRunningScans": delete_running_scans})

        r = requests.delete(
            url=project_url,
            data=request_body,
            headers=authHeaders.auth_headers,
            verify=config.get("verify")
        )

        # In Python http module, HTTP status ACCEPTED is 202
        if r.status_code == ACCEPTED:
            is_successful = True
        elif r.status_code == BAD_REQUEST:
            raise BadRequestError(r.text)
        elif r.status_code == NOT_FOUND:
            raise NotFoundError()
        elif (r.status_code == UNAUTHORIZED) and (self.retry < config.get("max_try")):
            authHeaders.update_auth_headers()
            self.retry += 1
            self.delete_project_by_id(project_id, delete_running_scans)
        else:
            raise CxError(r.text, r.status_code)

        self.retry = 0

        return is_successful

    def create_project_if_not_exists_by_project_name_and_team_full_name(
            self, project_name, team_full_name=config.get("team_full_name")
    ):
        """
        create a project if it not exists by project name and a team full name

        Args:
            project_name (str):
            team_full_name (str):

        Returns:
            int: project id
        """
        team_id = TeamAPI().get_team_id_by_team_full_name(team_full_name)

        project_id = self.get_project_id_by_project_name_and_team_full_name(project_name, team_full_name)

        if not project_id:
            project = self.create_project_with_default_configuration(project_name, team_id, True)
            if project:
                project_id = project.id

        return project_id

    def delete_project_if_exists_by_project_name_and_team_full_name(
            self, project_name, team_full_name=config.get("team_full_name")
    ):
        """

        Args:
            project_name (str):
            team_full_name (str): for example "/CxServer/SP/Company/Users"

        Returns:
            boolean

        """
        is_successful = False

        project_id = self.get_project_id_by_project_name_and_team_full_name(project_name, team_full_name)
        if project_id:
            is_successful = self.delete_project_by_id(project_id)

        return is_successful

    def create_branched_project(self, project_id, branched_project_name):
        """
        Create a branch of an existing project.

        Args:
            project_id (int): Unique Id of the project
            branched_project_name (str): specifies the name of the branched project
        Returns:
            :obj:`CxCreateProjectResponse`

        Raises:
            BadRequestError
            NotFoundError
            CxError

        """
        project = None

        project_branch_url = config.get("base_url") + "/cxrestapi/projects/{id}/branch".format(id=project_id)

        request_body = json.dumps({"name": branched_project_name})

        r = requests.post(
            url=project_branch_url,
            data=request_body,
            headers=authHeaders.auth_headers,
            verify=config.get("verify")
        )

        if r.status_code == CREATED:
            a_dict = r.json()
            project = CxCreateProjectResponse(
                project_id=a_dict.get("id"),
                link=CxLink(
                    rel=(a_dict.get("link", {}) or {}).get("rel"),
                    uri=(a_dict.get("link", {}) or {}).get("uri")
                )
            )
        elif r.status_code == BAD_REQUEST:
            raise BadRequestError(r.text)
        elif r.status_code == NOT_FOUND:
            raise NotFoundError()
        elif (r.status_code == UNAUTHORIZED) and (self.retry < config.get("max_try")):
            authHeaders.update_auth_headers()
            self.retry += 1
            self.create_branched_project(project_id, branched_project_name)
        else:
            raise CxError(r.text, r.status_code)

        self.retry = 0

        return project

    def get_all_issue_tracking_systems(self):
        """
        Get details of all issue tracking systems (e.g. Jira) currently registered to CxSAST.

        Returns:
            :obj:`list` of :obj:`CxIssueTrackingSystem`

        Raises:
            BadRequestError
            NotFoundError
            CxError

        """
        issue_tracking_systems = []

        issue_tracking_systems_url = config.get("base_url") + "/cxrestapi/issueTrackingSystems"

        r = requests.get(
            url=issue_tracking_systems_url,
            headers=authHeaders.auth_headers,
            verify=config.get("verify")
        )

        if r.status_code == OK:
            a_list = r.json()
            issue_tracking_systems = [
                CxIssueTrackingSystem(
                    tracking_system_id=item.get("id"),
                    name=item.get("name"),
                    tracking_system_type=item.get("type"),
                    url=item.get("url")
                ) for item in a_list
            ]
        elif r.status_code == BAD_REQUEST:
            raise BadRequestError(r.text)
        elif r.status_code == NOT_FOUND:
            raise NotFoundError()
        elif (r.status_code == UNAUTHORIZED) and (self.retry < config.get("max_try")):
            authHeaders.update_auth_headers()
            self.retry += 1
            self.get_all_issue_tracking_systems()
        else:
            raise CxError(r.text, r.status_code)

        self.retry = 0

        return issue_tracking_systems

    def get_issue_tracking_system_id_by_name(self, name):
        """
        get issue tracking system id by name

        Args:
            name (str): issue tracking system name

        Returns:
            int: issue_tracking_system id
        """
        issue_tracking_systems = self.get_all_issue_tracking_systems()
        a_dict = {item.name: item.id for item in issue_tracking_systems}
        return a_dict.get(name)

    def get_issue_tracking_system_details_by_id(self, issue_tracking_system_id):
        """
        Get metadata for a specific issue tracking system (e.g. Jira) according to the Issue Tracking System Id.

        Args:
            issue_tracking_system_id (int):  Unique Id of the issue tracking system

        Returns:
            dict

        Raises:
            BadRequestError
            NotFoundError
            CxError
        """
        issue_tracking_system = None

        issue_tracking_systems_metadata_url = config.get(
            "base_url") + "/cxrestapi/issueTrackingSystems/{id}/metadata".format(
            id=issue_tracking_system_id
        )

        r = requests.get(
            url=issue_tracking_systems_metadata_url,
            headers=authHeaders.auth_headers,
            verify=config.get("verify")
        )

        if r.status_code == OK:
            a_list = r.json().get("projects")
            if a_list:
                a_dict = a_list[0]
                issue_types = a_dict.get("issueTypes")
                issue_type = issue_types[0] if issue_types else {}
                fields = issue_type.get("fields")
                field = fields[0] if fields else {}
                allowed_values = field.get("allowedValues", []) or []

                issue_tracking_system = {
                    "projects": [
                        CxIssueTrackingSystemDetail(
                            tracking_system_detail_id=a_dict.get("id"),
                            name=a_dict.get("name"),
                            issue_types=[
                                CxIssueTrackingSystemType(
                                    issue_tracking_system_type_id=issue_type.get("id"),
                                    name=issue_type.get("name"),
                                    sub_task=issue_type.get("subtask"),
                                    fields=[
                                        CxIssueTrackingSystemField(
                                            tracking_system_field_id=field.get("id"),
                                            name=field.get("name"),
                                            multiple=field.get("multiple"),
                                            required=field.get("required"),
                                            supported=field.get("supported"),
                                            allowed_values=[
                                                CxIssueTrackingSystemFieldAllowedValue(
                                                    allowed_value_id=item.get("id"),
                                                    name=item.get("name")
                                                ) for item in allowed_values
                                            ]
                                        )
                                    ]
                                )
                            ]
                        )
                    ]
                }
        elif r.status_code == BAD_REQUEST:
            raise BadRequestError(r.text)
        elif r.status_code == NOT_FOUND:
            raise NotFoundError()
        elif (r.status_code == UNAUTHORIZED) and (self.retry < config.get("max_try")):
            authHeaders.update_auth_headers()
            self.retry += 1
            self.get_issue_tracking_system_details_by_id(issue_tracking_system_id)
        else:
            raise CxError(r.text, r.status_code)

        self.retry = 0

        return issue_tracking_system

    def get_project_exclude_settings_by_project_id(self, project_id):
        """
        get details of a project's exclude folders/files settings according to the project Id.

        Args:
            project_id (int): Unique Id of the project

        Returns:
            :obj:`CxProjectExcludeSettings`

        Raises:
            BadRequestError
            NotFoundError
            CxError
        """

        project_exclude_settings = None

        exclude_settings_url = config.get("base_url") + "/cxrestapi/projects/{id}/sourceCode/excludeSettings".format(
            id=project_id)

        r = requests.get(
            url=exclude_settings_url,
            headers=authHeaders.auth_headers,
            verify=config.get("verify")
        )

        if r.status_code == OK:
            a_dict = r.json()
            project_exclude_settings = CxProjectExcludeSettings(
                project_id=a_dict.get("projectId"),
                exclude_folders_pattern=a_dict.get("excludeFoldersPattern"),
                exclude_files_pattern=a_dict.get("excludeFilesPattern"),
                link=CxLink(
                    rel=(a_dict.get("link", {}) or {}).get("rel"),
                    uri=(a_dict.get("link", {}) or {}).get("uri")
                )
            )
        elif r.status_code == BAD_REQUEST:
            raise BadRequestError(r.text)
        elif r.status_code == NOT_FOUND:
            raise NotFoundError()
        elif (r.status_code == UNAUTHORIZED) and (self.retry < config.get("max_try")):
            authHeaders.update_auth_headers()
            self.retry += 1
            self.get_project_exclude_settings_by_project_id(project_id)
        else:
            raise CxError(r.text, r.status_code)

        self.retry = 0

        return project_exclude_settings

    def set_project_exclude_settings_by_project_id(self, project_id, exclude_folders_pattern, exclude_files_pattern):
        """
        set a project's exclude folders/files settings according to the project Id.

        Args:
            project_id (int):  Unique Id of the project
            exclude_folders_pattern (str, optional): comma separated list of folders,
                        including wildcard patterns to exclude (e.g. add-ons, connectors, doc, CheckmarxPythonSDK, lib)
            exclude_files_pattern (str, optional): comma separated list of files,
                        including wildcard patterns to exclude (e.g. cvc3.js, spass.js, z3.js, readme.txt,
                        smt_solver.js, readme.txt, find_sql_injections.js, jquery.js, logic.js)

        Returns:
            boolean

        Raises:
            BadRequestError
            NotFoundError
            CxError
        """
        is_successful = False

        exclude_settings_url = config.get("base_url") + "/cxrestapi/projects/{id}/sourceCode/excludeSettings".format(
            id=project_id)

        body_data = json.dumps(
            {
                "excludeFoldersPattern": exclude_folders_pattern,
                "excludeFilesPattern": exclude_files_pattern
            }
        )
        r = requests.put(
            url=exclude_settings_url,
            data=body_data,
            headers=authHeaders.auth_headers,
            verify=config.get("verify")
        )
        if r.status_code == OK:
            is_successful = True
        elif r.status_code == BAD_REQUEST:
            raise BadRequestError(r.text)
        elif r.status_code == NOT_FOUND:
            raise NotFoundError()
        elif (r.status_code == UNAUTHORIZED) and (self.retry < config.get("max_try")):
            authHeaders.update_auth_headers()
            self.retry += 1
            self.set_project_exclude_settings_by_project_id(project_id, exclude_folders_pattern, exclude_files_pattern)
        else:
            raise CxError(r.text, r.status_code)

        self.retry = 0

        return is_successful

    def get_remote_source_settings_for_git_by_project_id(self, project_id):
        """
        Get a specific project's remote source settings for a GIT repository according to the Project Id.

        Args:
            project_id (int): Unique Id of the project

        Returns:
            :obj:`CxGitSettings`

        Raises:
            BadRequestError
            NotFoundError
            CxError
        """
        git_settings = None

        remote_settings_git_url = config.get(
            "base_url") + "/cxrestapi/projects/{id}/sourceCode/remoteSettings/git".format(
            id=project_id)

        r = requests.get(
            url=remote_settings_git_url,
            headers=authHeaders.auth_headers,
            verify=config.get("verify")
        )

        if r.status_code == OK:
            a_dict = r.json()
            git_settings = CxGitSettings(
                url=a_dict.get("url"),
                branch=a_dict.get("branch"),
                use_ssh=a_dict.get("useSsh"),
                link=CxLink(
                    rel=(a_dict.get("link", {}) or {}).get("rel"),
                    uri=(a_dict.get("link", {}) or {}).get("uri")
                )
            )
        elif r.status_code == BAD_REQUEST:
            raise BadRequestError(r.text)
        elif r.status_code == NOT_FOUND:
            raise NotFoundError()
        elif (r.status_code == UNAUTHORIZED) and (self.retry < config.get("max_try")):
            authHeaders.update_auth_headers()
            self.retry += 1
            self.get_remote_source_settings_for_git_by_project_id(project_id)
        else:
            raise CxError(r.text, r.status_code)

        self.retry = 0

        return git_settings

    def set_remote_source_setting_to_git(self, project_id, url, branch, private_key=None):
        """
        Set a specific project's remote source location to a GIT repository using SSH protocol.

        Args:
            project_id (int): Unique Id of the project
            url (str): The url which is used to connect to the GIT repository (e.g. git@github.com:test/repo.git)
            branch (str): The branch of a GIT repository (e.g. refs/heads/master)
            private_key (str, optional): The private key (optional) which is used to connect to the GIT repository using
                                SSH protocol
                                (e.g. -----BEGIN RSA PRIVATE KEY-----
                                MIIJKgIBAAKCAgEahM6IR0lb4Rag4s5JM+xyEfKiUotGlHx
                                SkeRjzXyWwjX5dAfR3K7pzHzn0rSMN7yUYlhZDLKff6R
                                      -----END RSA PRIVATE KEY-----)

        Returns:
            boolean

        Raises:
            BadRequestError
            NotFoundError
            CxError
        """

        is_successful = False

        remote_settings_git_url = config.get(
            "base_url") + "/cxrestapi/projects/{id}/sourceCode/remoteSettings/git".format(
            id=project_id)

        post_body = CxGitSettings(
            url=url, branch=branch, private_key=private_key
        ).get_post_data()

        r = requests.post(
            url=remote_settings_git_url,
            data=post_body,
            headers=authHeaders.auth_headers,
            verify=config.get("verify")
        )

        if r.status_code == NO_CONTENT:
            is_successful = True
        elif r.status_code == BAD_REQUEST:
            raise BadRequestError(r.text)
        elif r.status_code == NOT_FOUND:
            raise NotFoundError()
        elif (r.status_code == UNAUTHORIZED) and (self.retry < config.get("max_try")):
            authHeaders.update_auth_headers()
            self.retry += 1
            self.set_remote_source_setting_to_git(project_id, url, branch, private_key)
        else:
            raise CxError(r.text, r.status_code)

        self.retry = 0

        return is_successful

    def get_remote_source_settings_for_svn_by_project_id(self, project_id):
        """
        get a specific project's remote source location settings for SVN repository according to the Project Id.

        Args:
            project_id (int):  Unique Id of the project

        Returns:
            :obj:`CxSVNSettings`

        Raises:
            BadRequestError
            NotFoundError
            CxError
        """

        svn_settings = None

        remote_settings_svn_url = config.get(
            "base_url") + "/cxrestapi/projects/{id}/sourceCode/remoteSettings/svn".format(
            id=project_id)

        r = requests.get(
            url=remote_settings_svn_url,
            headers=authHeaders.auth_headers,
            verify=config.get("verify")
        )

        if r.status_code == OK:
            a_dict = r.json()
            svn_settings = CxSVNSettings(
                uri=CxURI(
                    absolute_url=(a_dict.get("uri", {}) or {}).get("absoluteUrl"),
                    port=(a_dict.get("uri", {}) or {}).get("port")
                ),
                paths=a_dict.get("paths", []),
                use_ssh=a_dict.get("useSsh", False),
                link=CxLink(
                    rel=(a_dict.get("link", {}) or {}).get("rel"),
                    uri=(a_dict.get("link", {}) or {}).get("uri")
                )
            )
        elif r.status_code == BAD_REQUEST:
            raise BadRequestError(r.text)
        elif r.status_code == NOT_FOUND:
            raise NotFoundError()
        elif (r.status_code == UNAUTHORIZED) and (self.retry < config.get("max_try")):
            authHeaders.update_auth_headers()
            self.retry += 1
            self.get_remote_source_settings_for_svn_by_project_id(project_id)
        else:
            raise CxError(r.text, r.status_code)

        self.retry = 0

        return svn_settings

    def set_remote_source_settings_to_svn(self, project_id, absolute_url, port, paths, username, password,
                                          private_key=None):
        """
        set a specific project's remote source location to a SVN repository using SSH protocol.

        Args:
            project_id (int):  Unique Id of the project
            absolute_url (str):  Specifies the absolute url (e.g. http://<server_ip>/svn/testrepo)
            port (int):  Specifies the port number of the uri (e.g. 8080)
            paths (:obj:`list` of :obj:`str`):  Specifies the list of paths to scan at SVN repository (e.g. /trunk )
            username (str):
            password (str):
            private_key (str, optional):  The private key (optional) which is used to connect to the SVN repository
                using SSH protocol
                (e.g. -----BEGIN RSA PRIVATE KEY-----
                MIIJKgIBAAKCAgEahM6IR0lb4Rag4s5JM+xyEfKiUotGlHx
                SkeRjzXyWwjX5dAfR3K7pzHzn0rSMN7yUYlhZDLKff6R
                     -----END RSA PRIVATE KEY-----)

        Returns:
            boolean

        Raises:
            BadRequestError
            NotFoundError
            CxError
        """
        is_successful = False

        remote_settings_svn_url = config.get(
            "base_url") + "/cxrestapi/projects/{id}/sourceCode/remoteSettings/svn".format(
            id=project_id)

        post_body_data = CxSVNSettings(
            uri=CxURI(
                absolute_url=absolute_url,
                port=port
            ),
            paths=paths,
            credentials=CxCredential(
                username=username,
                password=password
            ),
            private_key=private_key
        ).get_post_data()

        r = requests.post(
            url=remote_settings_svn_url,
            data=post_body_data,
            headers=authHeaders.auth_headers,
            verify=config.get("verify")
        )

        if r.status_code == NO_CONTENT:
            is_successful = True
        elif r.status_code == BAD_REQUEST:
            raise BadRequestError(r.text)
        elif r.status_code == NOT_FOUND:
            raise NotFoundError()
        elif (r.status_code == UNAUTHORIZED) and (self.retry < config.get("max_try")):
            authHeaders.update_auth_headers()
            self.retry += 1
            self.set_remote_source_settings_to_svn(project_id, absolute_url, port, paths, username, password,
                                                   private_key)
        else:
            raise CxError(r.text, r.status_code)

        self.retry = 0

        return is_successful

    def get_remote_source_settings_for_tfs_by_project_id(self, project_id):
        """
        Get a specific project's remote source location settings for TFS repository according to the Project Id.

        Args:
            project_id (int):  Unique Id of the project

        Returns:
            :obj:`CxTFSSettings`

        Raises:
            BadRequestError
            NotFoundError
            CxError
        """

        tfs_settings = None

        remote_settings_tfs_url = config.get(
            "base_url") + "/cxrestapi/projects/{id}/sourceCode/remoteSettings/tfs".format(
            id=project_id)

        r = requests.get(
            url=remote_settings_tfs_url,
            headers=authHeaders.auth_headers,
            verify=config.get("verify")
        )
        if r.status_code == OK:
            a_dict = r.json()
            tfs_settings = CxTFSSettings(
                uri=CxURI(
                    absolute_url=(a_dict.get("uri", {}) or {}).get("absoluteUrl"),
                    port=(a_dict.get("uri", {}) or {}).get("port"),
                ),
                paths=a_dict.get("paths"),
                link=CxLink(
                    rel=(a_dict.get("link", {}) or {}).get("rel"),
                    uri=(a_dict.get("link", {}) or {}).get("uri")
                )
            )
        elif r.status_code == BAD_REQUEST:
            raise BadRequestError(r.text)
        elif r.status_code == NOT_FOUND:
            raise NotFoundError()
        elif (r.status_code == UNAUTHORIZED) and (self.retry < config.get("max_try")):
            authHeaders.update_auth_headers()
            self.retry += 1
            self.get_remote_source_settings_for_tfs_by_project_id(project_id)
        else:
            raise CxError(r.text, r.status_code)

        self.retry = 0

        return tfs_settings

    def set_remote_source_settings_to_tfs(self, project_id, username, password, absolute_url, port, paths):
        """
        Set a specific project's remote source location to a TFS repository.

        Args:
            project_id (int):  Unique Id of the project
            username (str):
            password (str):
            absolute_url (str):  Specifies the absolute url (e.g. http://<site_name>/tfs/DefaultCollection)
            port (int):  Specifies the port number of the uri (e.g. 8080)
            paths (:obj:`list` of :obj:`str`): Specifies the list of paths to scan at TFS repository
                                    (e.g. /Root/Optimization/V6.2.2.9-branch/CSharp/Graph, /Root/test)

        Returns:
            boolean

        Raises:
            BadRequestError
            NotFoundError
            CxError
        """
        is_successful = False

        remote_settings_tfs_url = config.get(
            "base_url") + "/cxrestapi/projects/{id}/sourceCode/remoteSettings/tfs".format(
            id=project_id)

        post_data = CxTFSSettings(
            credentials=CxCredential(
                username=username,
                password=password
            ),
            uri=CxURI(
                absolute_url=absolute_url,
                port=port
            ),
            paths=paths
        ).get_post_data()

        r = requests.post(
            url=remote_settings_tfs_url,
            headers=authHeaders.auth_headers,
            data=post_data,
            verify=config.get("verify")
        )
        if r.status_code == NO_CONTENT:
            is_successful = True
        elif r.status_code == BAD_REQUEST:
            raise BadRequestError(r.text)
        elif r.status_code == NOT_FOUND:
            raise NotFoundError()
        elif (r.status_code == UNAUTHORIZED) and (self.retry < config.get("max_try")):
            authHeaders.update_auth_headers()
            self.retry += 1
            self.set_remote_source_settings_to_tfs(project_id, username, password, absolute_url, port, paths)
        else:
            raise CxError(r.text, r.status_code)

        self.retry = 0

        return is_successful

    def get_remote_source_settings_for_custom_by_project_id(self, project_id):
        """
        Get a specific project's remote source location settings for custom repository (e.g. source pulling)
         according to the Project Id.
        :param project_id:
        :return:

        Args:
            project_id (int):  Unique Id of the project

        Returns:
            :obj:`CxCustomRemoteSourceSettings`

        Raises:
            BadRequestError
            NotFoundError
            CxError
        """
        custom_remote_setting = None

        remote_settings_custom_url = config.get(
            "base_url") + "/cxrestapi/projects/{id}/sourceCode/remoteSettings/custom".format(
            id=project_id
        )

        r = requests.get(
            url=remote_settings_custom_url,
            headers=authHeaders.auth_headers,
            verify=config.get("verify")
        )

        if r.status_code == OK:
            a_dict = r.json()
            custom_remote_setting = CxCustomRemoteSourceSettings(
                path=a_dict.get("path"),
                pulling_command_id=a_dict.get("pullingCommandId"),
                link=CxLink(
                    rel=(a_dict.get("link", {}) or {}).get("rel"),
                    uri=(a_dict.get("link", {}) or {}).get("uri")
                )
            )
        elif r.status_code == BAD_REQUEST:
            raise BadRequestError(r.text)
        elif r.status_code == NOT_FOUND:
            raise NotFoundError()
        elif (r.status_code == UNAUTHORIZED) and (self.retry < config.get("max_try")):
            authHeaders.update_auth_headers()
            self.retry += 1
            self.get_remote_source_settings_for_custom_by_project_id(project_id)
        else:
            raise CxError(r.text, r.status_code)

        self.retry = 0

        return custom_remote_setting

    def set_remote_source_setting_for_custom_by_project_id(self, project_id, path,
                                                           pre_scan_command_id, username, password):
        """
        Set a specific project's remote source location settings for custom repository
        (e.g. source pulling) according to the Project Id.


        Args:
            project_id (int): Unique Id of the project
            path (str): Path to the network folders containing the project code
            pre_scan_command_id (int): Unique Id of script that pulls the source code
            username (str):
            password (str):

        Returns:
            boolean

        Raises:
            BadRequestError
            NotFoundError
            CxError
        """
        is_successful = False

        remote_settings_custom_url = config.get(
            "base_url") + "/cxrestapi/projects/{id}/sourceCode/remoteSettings/custom".format(
            id=project_id
        )

        request_body_data = CxCustomRemoteSourceSettings(
            path=path,
            pulling_command_id=pre_scan_command_id,
            credentials=CxCredential(
                username=username,
                password=password
            )
        ).get_post_data()

        r = requests.post(
            url=remote_settings_custom_url,
            data=request_body_data,
            headers=authHeaders.auth_headers,
            verify=config.get("verify")
        )
        if r.status_code == NO_CONTENT:
            is_successful = True
        elif r.status_code == BAD_REQUEST:
            raise BadRequestError(r.text)
        elif r.status_code == NOT_FOUND:
            raise NotFoundError()
        elif (r.status_code == UNAUTHORIZED) and (self.retry < config.get("max_try")):
            authHeaders.update_auth_headers()
            self.retry += 1
            self.set_remote_source_setting_for_custom_by_project_id(project_id, path,
                                                                    pre_scan_command_id, username, password)
        else:
            raise CxError(r.text, r.status_code)

        self.retry = 0

        return is_successful

    def get_remote_source_settings_for_shared_by_project_id(self, project_id):
        """
        Get a specific project's remote source location settings for shared repository according to the Project Id.

        Args:
            project_id (int):  Unique Id of the project

        Returns:
            :obj:`CxSharedRemoteSourceSettingsResponse`

        Raises:
            BadRequestError
            NotFoundError
            CxError
        """
        shared_source_setting = None

        remote_settings_shared_url = config.get(
            "base_url") + "/cxrestapi/projects/{id}/sourceCode/remoteSettings/shared".format(
            id=project_id
        )

        r = requests.get(
            url=remote_settings_shared_url,
            headers=authHeaders.auth_headers,
            verify=config.get("verify")
        )
        if r.status_code == OK:
            a_dict = r.json()
            shared_source_setting = CxSharedRemoteSourceSettingsResponse(
                paths=a_dict.get("paths"),
                link=CxLink(
                    rel=(a_dict.get("link", {}) or {}).get("rel"),
                    uri=(a_dict.get("link", {}) or {}).get("uri")
                )
            )
        elif r.status_code == BAD_REQUEST:
            raise BadRequestError(r.text)
        elif r.status_code == NOT_FOUND:
            raise NotFoundError()
        elif (r.status_code == UNAUTHORIZED) and (self.retry < config.get("max_try")):
            authHeaders.update_auth_headers()
            self.retry += 1
            self.get_remote_source_settings_for_shared_by_project_id(project_id)
        else:
            raise CxError(r.text, r.status_code)

        self.retry = 0

        return shared_source_setting

    def set_remote_source_settings_to_shared(self, project_id, paths, username, password):
        """
        Set a specific project's remote source location to a shared repository.

        Args:
            project_id (int):  Unique Id of the project
            paths (:obj:`list` of :obj:`str`):  Specifies the list of paths to scan at the shared repository
                            (e.g. \\\\storage\\qa\\projects_new\\CPP\\1_Under_70k\\cpp_22_LOC)
            username (str):
            password (sr):

        Returns:
            boolean

        Raises:
            BadRequestError
            NotFoundError
            CxError
        """
        is_successful = False

        remote_settings_shared_url = config.get(
            "base_url") + "/cxrestapi/projects/{id}/sourceCode/remoteSettings/shared".format(
            id=project_id
        )

        post_body_data = CxSharedRemoteSourceSettingsRequest(
            paths=paths,
            credentials=CxCredential(
                username=username,
                password=password
            )
        ).get_post_data()

        r = requests.post(
            url=remote_settings_shared_url,
            data=post_body_data,
            headers=authHeaders.auth_headers,
            verify=config.get("verify")
        )

        if r.status_code == NO_CONTENT:
            is_successful = True
        elif r.status_code == BAD_REQUEST:
            raise BadRequestError(r.text)
        elif r.status_code == NOT_FOUND:
            raise NotFoundError()
        elif (r.status_code == UNAUTHORIZED) and (self.retry < config.get("max_try")):
            authHeaders.update_auth_headers()
            self.retry += 1
            self.set_remote_source_settings_to_shared(project_id, paths, username, password)
        else:
            raise CxError(r.text, r.status_code)

        self.retry = 0

        return is_successful

    def get_remote_source_settings_for_perforce_by_project_id(self, project_id):
        """
        Get a specific project's remote source location settings for Perforce repository according to the Project Id.

        Args:
            project_id (int):  Unique Id of the specific project

        Returns:
            :obj:`CxPerforceSettings`

        Raises:
            BadRequestError
            NotFoundError
            CxError
        """
        perforce_settings = None

        remote_settings_perforce_url = config.get(
            "base_url") + "/cxrestapi/projects/{id}/sourceCode/remoteSettings/perforce".format(
            id=project_id
        )

        r = requests.get(
            url=remote_settings_perforce_url,
            headers=authHeaders.auth_headers,
            verify=config.get("verify")
        )

        if r.status_code == OK:
            a_dict = r.json()
            perforce_settings = CxPerforceSettings(
                uri=CxURI(
                    absolute_url=(a_dict.get("uri", {}) or {}).get("absoluteUrl"),
                    port=(a_dict.get("uri", {}) or {}).get("port")
                ),
                paths=a_dict.get("paths"),
                browse_mode=a_dict.get("browseMode"),
                link=CxLink(
                    rel=(a_dict.get("link", {}) or {}).get("rel"),
                    uri=(a_dict.get("link", {}) or {}).get("uri")
                )
            )
        elif r.status_code == BAD_REQUEST:
            raise BadRequestError(r.text)
        elif r.status_code == NOT_FOUND:
            raise NotFoundError()
        elif (r.status_code == UNAUTHORIZED) and (self.retry < config.get("max_try")):
            authHeaders.update_auth_headers()
            self.retry += 1
            self.get_remote_source_settings_for_perforce_by_project_id(project_id)
        else:
            raise CxError(r.text, r.status_code)

        self.retry = 0

        return perforce_settings

    def set_remote_source_settings_to_perforce(self, project_id, username, password, absolute_url, port, paths,
                                               browse_mode):
        """
        Set a specific project's remote source location to a Perforce repository.

        Args:
            project_id (int): Unique Id of the specific project
            username (str):
            password (str):
            absolute_url (str):  Specifies the absolute url (e.g. <server_ip>)
            port (int):  Specifies the port number of this Uri (e.g. 8080)
            paths (:obj:`list` of :obj:`str`): Specifies the list of paths to scan at Perforce repository
                                                (e.g. ////depot)
            browse_mode (str):  Specifies the browsing mode of the Perforce repository
                                (depot for shared or workspace for grouped).

        Returns:
            boolean

        Raises:
            BadRequestError
            NotFoundError
            CxError
        """

        is_successful = False

        remote_settings_perforce_url = config.get(
            "base_url") + "/cxrestapi/projects/{id}/sourceCode/remoteSettings/perforce".format(
            id=project_id
        )

        post_data = CxPerforceSettings(
            credentials=CxCredential(
                username=username,
                password=password,
            ),
            uri=CxURI(
                absolute_url=absolute_url,
                port=port
            ),
            paths=paths,
            browse_mode=browse_mode
        ).get_post_data()

        r = requests.post(
            url=remote_settings_perforce_url,
            headers=authHeaders.auth_headers,
            data=post_data,
            verify=config.get("verify")
        )
        if r.status_code == NO_CONTENT:
            is_successful = True
        elif r.status_code == BAD_REQUEST:
            raise BadRequestError(r.text)
        elif r.status_code == NOT_FOUND:
            raise NotFoundError()
        elif (r.status_code == UNAUTHORIZED) and (self.retry < config.get("max_try")):
            authHeaders.update_auth_headers()
            self.retry += 1
            self.set_remote_source_settings_to_perforce(project_id, username, password, absolute_url, port, paths,
                                                        browse_mode)
        else:
            raise CxError(r.text, r.status_code)

        self.retry = 0

        return is_successful

    def set_remote_source_setting_to_git_using_ssh(self, project_id, url, branch, private_key_file_path):
        """
        Set a specific project's remote source location to a GIT repository using the SSH protocol

        Args:
            project_id (int):  Unique Id of the project
            url (str):  The URL which is used to connect to the GIT repository (e.g. git@github.com:test_repo/test.git)
            branch (str): The branch of a GIT repository (e.g. refs/heads/master)
            private_key_file_path (str): The SSH certificate which is used to connect to the GIT repository
                                    using SSH protocol (multipart/form-data)

        Returns:
            boolean

        Raises:
            BadRequestError
            NotFoundError
            CxError
        """
        is_successful = False

        remote_settings_git_ssh_url = config.get(
            "base_url") + "/cxrestapi/projects/{id}/sourceCode/remoteSettings/git/ssh".format(
            id=project_id
        )

        headers = copy.deepcopy(authHeaders.auth_headers)

        file_name = os.path.basename(private_key_file_path)

        with open(private_key_file_path, "rb") as a_file:
            file_content = a_file.read()

        m = MultipartEncoder(
            fields={
                "url": url,
                "branch": branch,
                "privateKey": (file_name, file_content, "text/plain")
            }
        )
        headers.update({"Content-Type": m.content_type})

        r = requests.post(
            url=remote_settings_git_ssh_url,
            headers=headers,
            data=m,
            verify=config.get("verify")
        )
        if r.status_code == NO_CONTENT:
            is_successful = True
        elif r.status_code == BAD_REQUEST:
            raise BadRequestError(r.text)
        elif r.status_code == NOT_FOUND:
            raise NotFoundError()
        elif (r.status_code == UNAUTHORIZED) and (self.retry < config.get("max_try")):
            authHeaders.update_auth_headers()
            self.retry += 1
            self.set_remote_source_setting_to_git_using_ssh(project_id, url, branch, private_key_file_path)
        else:
            raise CxError(r.text, r.status_code)

        self.retry = 0

        return is_successful

    def set_remote_source_setting_to_svn_using_ssh(self, project_id, absolute_url, port, paths, private_key_file_path):
        """
        Set a specific project's remote source location to a SVN repository which uses the SSH protocol

        Args:
            project_id (int): Unique Id of the specific project
            absolute_url (str):  The URL which is used to connect to the SVN repository
                                (e.g. http://<server_ip>/svn/testrepo)
            port (int): Specifies the port number of SVN repository url
            paths (:obj:`list` of :obj:`str`): Specifies the paths of the SVN repository (e.g. /trunk)
            private_key_file_path (str): The SSH certificate which is used to connect to the SVN repository
                                         using SSH protocol (multipart/form-data)

        Returns:
            boolean

        Raises:
            BadRequestError
            NotFoundError
            CxError
        """
        is_successful = False
        # TODO check, when have svn + ssh
        remote_settings_svn_ssh_url = config.get(
            "base_url") + "/cxrestapi/projects/{id}/sourceCode/remoteSettings/svn/ssh".format(
            id=project_id
        )

        headers = copy.deepcopy(authHeaders.auth_headers)

        file_name = os.path.basename(private_key_file_path)
        m = MultipartEncoder(
            fields={
                "absoluteUrl": absolute_url,
                "port": str(port),
                "paths": str(paths),
                "privateKey": (file_name, open(private_key_file_path, "rb"), "text/plain")
            }
        )
        headers.update({"Content-Type": m.content_type})

        r = requests.post(
            url=remote_settings_svn_ssh_url,
            headers=headers,
            data=m,
            verify=config.get("verify")
        )
        if r.status_code == NO_CONTENT:
            is_successful = True
        elif r.status_code == BAD_REQUEST:
            raise BadRequestError(r.text)
        elif r.status_code == NOT_FOUND:
            raise NotFoundError()
        elif (r.status_code == UNAUTHORIZED) and (self.retry < config.get("max_try")):
            authHeaders.update_auth_headers()
            self.retry += 1
            self.set_remote_source_setting_to_svn_using_ssh(project_id, absolute_url, port, paths,
                                                            private_key_file_path)
        else:
            raise CxError(r.text, r.status_code)

        self.retry = 0

        return is_successful

    def upload_source_code_zip_file(self, project_id, zip_file_path):
        """
        Upload a zip file that contains the source code for scanning.

        Args:
            project_id (int):  Unique Id of the project
            zip_file_path (str): absolute file path

        Returns:
            boolean

        Raises:
            BadRequestError
            NotFoundError
            CxError
        """
        is_successful = False

        attachments_url = config.get("base_url") + "/cxrestapi/projects/{id}/sourceCode/attachments".format(
            id=project_id)

        headers = copy.deepcopy(authHeaders.auth_headers)

        file_name = os.path.basename(zip_file_path)
        m = MultipartEncoder(
            fields={
                "zippedSource": (file_name, open(zip_file_path, 'rb'), "application/zip")
            }
        )
        headers.update({"Content-Type": m.content_type})

        r = requests.post(
            url=attachments_url,
            headers=headers,
            data=m,
            verify=config.get("verify")
        )
        if r.status_code == NO_CONTENT:
            is_successful = True
        elif r.status_code == BAD_REQUEST:
            raise BadRequestError(r.text)
        elif r.status_code == NOT_FOUND:
            raise NotFoundError()
        elif (r.status_code == UNAUTHORIZED) and (self.retry < config.get("max_try")):
            authHeaders.update_auth_headers()
            self.retry += 1
            self.upload_source_code_zip_file(project_id, zip_file_path)
        else:
            raise CxError(r.text, r.status_code)

        self.retry = 0

        return is_successful

    def set_data_retention_settings_by_project_id(self, project_id, scans_to_keep=10):
        """
        Set the data retention settings according to Project Id.

        Args:
            project_id (int):  Unique Id of the project
            scans_to_keep (int): The amount of scans to keep before they are deleted (1-1000 or null)

        Returns:
            boolean

        Raises:
            BadRequestError
            NotFoundError
            CxError
        """
        is_successful = False

        data_retention_settings_url = config.get("base_url") + "/cxrestapi/projects/{id}/dataRetentionSettings".format(
            id=project_id)

        post_body = json.dumps(
            {
                "scansToKeep": scans_to_keep
            }
        )

        r = requests.post(
            url=data_retention_settings_url,
            data=post_body,
            headers=authHeaders.auth_headers,
            verify=config.get("verify")
        )

        if r.status_code == NO_CONTENT:
            is_successful = True
        elif r.status_code == BAD_REQUEST:
            raise BadRequestError(r.text)
        elif r.status_code == NOT_FOUND:
            raise NotFoundError()
        elif (r.status_code == UNAUTHORIZED) and (self.retry < config.get("max_try")):
            authHeaders.update_auth_headers()
            self.retry += 1
            self.set_data_retention_settings_by_project_id(project_id, scans_to_keep)
        else:
            raise CxError(r.text, r.status_code)

        self.retry = 0

        return is_successful

    def set_issue_tracking_system_as_jira_by_id(self, project_id, issue_tracking_system_id, jira_project_id,
                                                issue_type_id, jira_fields):
        """
        Set a specific issue tracking system as Jira according to Project Id.

        Args:
            project_id (int):  Unique Id of the project
            issue_tracking_system_id (int): Specifies the issue tracking system Id
            jira_project_id (str): Specifies the specific Id of Jira project
            issue_type_id (str): Specifies the Id of issue type
            jira_fields (:obj:`list` of :obj:`CxIssueTrackingSystemJiraField`) Specifies the list of fields associated
                                                        with the issue type

        Returns:
            boolean

        Raises:
            BadRequestError
            NotFoundError
            CxError
        """
        # TODO, check when have jira

        is_successful = False

        jira_url = config.get("base_url") + "/cxrestapi/projects/{id}/issueTrackingSettings/jira".format(id=project_id)

        post_data = CxIssueTrackingSystemJira(
            issue_tracking_system_id=issue_tracking_system_id,
            jira_project_id=jira_project_id,
            issue_type_id=issue_type_id,
            fields=jira_fields
        ).get_post_data()

        r = requests.post(
            url=jira_url,
            headers=authHeaders.auth_headers,
            data=post_data,
            verify=config.get("verify")
        )

        if r.status_code == NO_CONTENT:
            is_successful = True
        elif r.status_code == BAD_REQUEST:
            raise BadRequestError(r.text)
        elif r.status_code == NOT_FOUND:
            raise NotFoundError()
        elif (r.status_code == UNAUTHORIZED) and (self.retry < config.get("max_try")):
            authHeaders.update_auth_headers()
            self.retry += 1
            self.set_issue_tracking_system_as_jira_by_id(project_id, issue_tracking_system_id, jira_project_id,
                                                         issue_type_id, jira_fields)
        else:
            raise CxError(r.text, r.status_code)

        self.retry = 0

        return is_successful

    def get_all_preset_details(self):
        """
        get details of all presets

        Returns:
            :obj:`list` of :obj:`CxPreset`

        Raises:
            BadRequestError
            NotFoundError
            CxError

        """
        all_preset_details = []

        presets_url = config.get("base_url") + "/cxrestapi/sast/presets"

        r = requests.get(
            url=presets_url,
            headers=authHeaders.auth_headers,
            verify=config.get("verify")
        )

        if r.status_code == OK:
            a_list = r.json()
            all_preset_details = [
                CxPreset(
                    preset_id=item.get("id"),
                    name=item.get("name"),
                    owner_name=item.get("ownerName"),
                    link=CxLink(
                        rel=(item.get("link", {}) or {}).get("rel"),
                        uri=(item.get("link", {}) or {}).get("uri")
                    )
                ) for item in a_list
            ]
        elif r.status_code == BAD_REQUEST:
            raise BadRequestError(r.text)
        elif r.status_code == NOT_FOUND:
            raise NotFoundError()
        elif (r.status_code == UNAUTHORIZED) and (self.retry < config.get("max_try")):
            authHeaders.update_auth_headers()
            self.retry += 1
            self.get_all_preset_details()
        else:
            raise CxError(r.text, r.status_code)

        self.retry = 0

        return all_preset_details

    def get_preset_id_by_name(self, preset_name=config.get("scan_preset")):
        """

        Args:
            preset_name (str):

        Returns:
            int: preset id
        """
        all_presets = self.get_all_preset_details()
        a_dict_preset_name_id = {item.name: item.id for item in all_presets}
        return a_dict_preset_name_id.get(preset_name)

    def get_preset_details_by_preset_id(self, preset_id):
        """
        Get details of a specified preset by Id.

        Args:
            preset_id (int): Unique Id of the preset

        Returns:
            :obj:`CxPreset`

        Raises:
            BadRequestError
            NotFoundError
            CxError
        """
        preset = None

        preset_url = config.get("base_url") + "/cxrestapi/sast/presets/{id}".format(id=preset_id)

        r = requests.get(
            url=preset_url,
            headers=authHeaders.auth_headers,
            verify=config.get("verify")
        )

        if r.status_code == OK:
            a_dict = r.json()
            preset = CxPreset(
                preset_id=a_dict.get("id"),
                name=a_dict.get("name"),
                owner_name=a_dict.get("ownerName"),
                link=CxLink(
                    rel=(a_dict.get("link", {}) or {}).get("rel"),
                    uri=(a_dict.get("link", {}) or {}).get("uri")
                ),
                query_ids=a_dict.get("queryIds")
            )
        elif r.status_code == BAD_REQUEST:
            raise BadRequestError(r.text)
        elif r.status_code == NOT_FOUND:
            raise NotFoundError()
        elif (r.status_code == UNAUTHORIZED) and (self.retry < config.get("max_try")):
            authHeaders.update_auth_headers()
            self.retry += 1
            self.get_preset_details_by_preset_id(preset_id)
        else:
            raise CxError(r.text, r.status_code)

        self.retry = 0

        return preset
