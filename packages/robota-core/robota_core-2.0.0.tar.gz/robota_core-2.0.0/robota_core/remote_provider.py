import datetime
from abc import abstractmethod
from typing import List, Union, Dict

from loguru import logger

from robota_core import gitlab_tools, config_readers
from robota_core.github_tools import GithubServer
from robota_core.merge_request import MergeRequest, MergeRequestCache


class RemoteProvider:
    """A remote provider is a cloud provider that a git repository can be synchronised to.
    Remote providers have some features that a basic git Repository does not including merge
    requests and teams.
    """
    def __init__(self):
        self._stored_merge_requests: List[MergeRequestCache] = []

    def get_merge_requests(self, start: datetime.datetime = datetime.datetime.fromtimestamp(1),
                           end: datetime.datetime = datetime.datetime.now()) -> List[MergeRequest]:
        cached_merge_requests = self._get_cached_merge_requests(start, end)
        if cached_merge_requests:
            return cached_merge_requests.merge_requests

        new_merge_requests = self._fetch_merge_requests(start, end)
        cache = MergeRequestCache(start, end, new_merge_requests)
        self._stored_merge_requests.append(cache)
        return new_merge_requests

    @abstractmethod
    def _fetch_merge_requests(self, start: datetime.datetime,
                              end: datetime.datetime) -> List[MergeRequest]:
        raise NotImplementedError("Not implemented in base class")

    def _get_cached_merge_requests(self, start: datetime.datetime,
                                   end: datetime.datetime) -> Union[MergeRequestCache, None]:
        """Check whether merge requests with the specified start and end date are already stored."""
        for cache in self._stored_merge_requests:
            if cache.start == start and cache.end == end:
                return cache
        else:
            return None

    @abstractmethod
    def get_members(self) -> Dict[str, str]:
        """Get a dictionary of names and corresponding usernames of members of this repository."""
        raise NotImplementedError("Not implemented in base class.")


class GithubRemoteProvider(RemoteProvider):
    def __init__(self, provider_source: dict):
        super().__init__()
        server = GithubServer(provider_source)
        self.repo = server.open_github_repo(provider_source["project"])

    def _fetch_merge_requests(self, start: datetime.datetime,
                              end: datetime.datetime) -> List[MergeRequest]:
        all_pulls = self.repo.get_pulls()
        filtered_pulls = [pull for pull in all_pulls if start < pull.created_at < end]
        return [MergeRequest(pull, "github") for pull in filtered_pulls]

    def get_members(self) -> Dict[str, str]:
        """This method returns names and usernames of repo collaborators since github doesn't
        have the idea of members in the same way as gitlab."""
        members = self.repo.get_collaborators()
        member_names = {member.name: member.login for member in members}
        return member_names


class GitlabRemoteProvider(RemoteProvider):
    def __init__(self, provider_source: dict):
        super().__init__()
        server = gitlab_tools.GitlabServer(provider_source["url"], provider_source["token"])
        self.project = server.open_gitlab_project(provider_source["project"])

        super().__init__()

    def _fetch_merge_requests(self, start: datetime.datetime,
                              end: datetime.datetime) -> List[MergeRequest]:
        """Get merge requests within a time period"""
        merge_requests = self.project.mergerequests.list(created_after=start, created_before=end)
        return [MergeRequest(merge_request, "gitlab") for merge_request in merge_requests]

    def get_members(self) -> Dict[str, str]:
        members = self.project.members.list()
        member_names = {member.attributes['name']: member.attributes['username']
                        for member in members}
        return member_names


def new_remote_provider(robota_config: dict) -> Union[RemoteProvider, None]:
    """Factory method for RemoteProvider."""
    provider_config = config_readers.get_data_source_info(robota_config, "remote_provider")
    if not provider_config:
        return None
    provider_type = provider_config["type"]

    logger.debug(f"Initialising {provider_type} remote provider.")

    if provider_type == "gitlab":
        return GitlabRemoteProvider(provider_config)
    elif provider_type == "github":
        return GithubRemoteProvider(provider_config)
    else:
        raise TypeError(f"Unknown remote provider type {provider_config['type']}.")
