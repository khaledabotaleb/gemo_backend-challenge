from datetime import datetime, timedelta

import requests
from rest_framework.decorators import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny


class ListReposLanguages(APIView):
    permissions_classes = [AllowAny]

    def get(self, request):
        """
            Dict of languages used in top 100 trending repositories on Github(GH),
            with following attributes:
            + the number of repos using the language
            + list of repos' urls (api + html urls)
            I chose to return repo urls instead the entire repos object because the
            response was too big and ugly
        """
        today = datetime.now()
        thirty_days_ago = (today - timedelta(days=30)).strftime("%Y-%m-%d")
        # api call to list of 100 trending repositories in GH sorted by stars
        # in descending order
        url = "https://api.github.com/search/repositories?q=created:>{0}&sort=stars&order=desc&page=1&per_page=100".format(
            thirty_days_ago)
        response = requests.get(url)
        if response.status_code == 200:
            trending_repositories = response.json()['items']
            list_languages = {}
            NO_OF_REPOS = "No of repos"
            LIST_OF_REPOS = "List of repos"
            url = "url"
            html_url = "html_url"

            for repo in trending_repositories:
                language = repo['language']
                languages = list_languages.setdefault(language,
                                                      {NO_OF_REPOS: 0,
                                                       LIST_OF_REPOS: []})

                list_languages[language][NO_OF_REPOS] = languages[NO_OF_REPOS] + 1
                languages[LIST_OF_REPOS].append({repo[url], repo[html_url]})

            return Response(list_languages)

        return Response(response, status=response.status_code)
