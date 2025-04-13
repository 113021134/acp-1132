import scrapy
import re
import json

class GithubSpider(scrapy.Spider):
    name = "github"
    allowed_domains = ["github.com", "api.github.com"]
    start_urls = ["https://github.com/SatelitKaca?tab=repositories"]

    def parse(self, response):
        for repo in response.css('li[itemprop="owns"]'):
            repo_name = repo.css('a[itemprop="name codeRepository"]::text').get()
            repo_name = repo_name.strip() if repo_name else None

            repo_href = repo.css('a[itemprop="name codeRepository"]::attr(href)').get()
            repo_url = response.urljoin(repo_href)

            about = repo.css('p[itemprop="description"]::text').get()
            if about:
                about = about.strip()
            if not about:
                about = repo_name

            last_updated = repo.css('relative-time::attr(datetime)').get()

           
            match = re.match(r'https://github.com/([^/]+)/([^/]+)', repo_url)
            if match:
                owner = match.group(1)
                repo = match.group(2)
            else:
                owner = "unknown"
                repo = "unknown"

            commits_api = f'https://api.github.com/repos/{owner}/{repo}/commits'
            languages_api = f'https://api.github.com/repos/{owner}/{repo}/languages'

            yield scrapy.Request(
                commits_api,
                callback=self.parse_commits,
                meta={
                    'repo_name': repo_name,
                    'repo_url': repo_url,
                    'about': about,
                    'last_updated': last_updated,
                    'languages_api': languages_api
                },
                headers={"Accept": "application/vnd.github+json"}
            )

    def parse_commits(self, response):
        repo_name = response.meta['repo_name']
        repo_url = response.meta['repo_url']
        about = response.meta['about']
        last_updated = response.meta['last_updated']
        languages_api = response.meta['languages_api']

        try:
            commits = json.loads(response.text)
            num_commits = len(commits)
        except Exception:
            num_commits = None

        yield scrapy.Request(
            languages_api,
            callback=self.parse_languages,
            meta={
                'repo_name': repo_name,
                'repo_url': repo_url,
                'about': about,
                'last_updated': last_updated,
                'num_commits': num_commits
            },
            headers={"Accept": "application/vnd.github+json"}
        )

    def parse_languages(self, response):
        repo_name = response.meta['repo_name']
        repo_url = response.meta['repo_url']
        about = response.meta['about']
        last_updated = response.meta['last_updated']
        num_commits = response.meta['num_commits']

        try:
            languages_json = json.loads(response.text)
            languages = list(languages_json.keys())
        except Exception:
            languages = None

        yield {
            'repo_name': repo_name,
            'repo_url': repo_url,
            'about': about,
            'last_updated': last_updated,
            'languages': languages,
            'num_commits': num_commits
        }
