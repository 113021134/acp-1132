import scrapy
import json
import re
from github_scraper.items import RepositoryItem

last_updated = None
class GithubSpider(scrapy.Spider):
    name = "github_spider"
    allowed_domains = ["github.com", "api.github.com"]
    start_urls = ["https://github.com/113021130?tab=repositories"]

    def parse(self, response):
        global last_updated
        repo_links = response.css("div.d-inline-block.mb-1 a::attr(href)").getall()

        for link in repo_links:
            last_updated = response.css('relative-time::attr(datetime)').get()
            full_url = response.urljoin(link)
            yield scrapy.Request(full_url, callback=self.parse_repo)

    def parse_repo(self, response):
        global last_updated
        item = RepositoryItem()
        item['url'] = response.url

        about = response.css('p.f4.my-3::text').get()
        if about:
            item['about'] = about.strip()
        else:
            is_empty = response.css('div.Box-body.p-6.py-3').re_first(r'This repository is empty')
            if not is_empty:
                repo_name = response.url.strip('/').split('/')[-1]
                about = repo_name
            else:
                about = None

        item['about'] = about
        item['last_updated'] = last_updated 


        

        match = re.match(r'https://github.com/([^/]+)/([^/]+)', response.url)
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
                'repo_name': repo,
                'repo_url': response.url,
                'about': item['about'],
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
