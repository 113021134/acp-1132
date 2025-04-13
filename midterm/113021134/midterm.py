import scrapy
import xml.etree.ElementTree as ET

root = ET.Element("Repositories")
idCount = 0
currentDesc = None
currentLastUpdated = None

class GithubSpider(scrapy.Spider):
    name = "github"
    allowed_domains = ['github.com']
    start_urls = ['https://github.com/113021134?tab=repositories']

    def parse(self, response):
        global currentDesc, currentLastUpdated
        repos = response.css('li[itemprop="owns"]')

        for repo in repos:
            currentDesc = None if len(response.css('p[itemprop="description"]::text').get(default='').strip()) == 0 else response.css('p[itemprop="description"]::text').get(default='').strip()
            currentLastUpdated = repo.css('relative-time::attr(datetime)').get()
            
            relative_url = repo.css('a[itemprop="name codeRepository"]::attr(href)').get()

            if relative_url:
                full_url = response.urljoin(relative_url)
                yield scrapy.Request(full_url, callback=self.parse_repo)

    def parse_repo(self, response):
        global idCount, root, currentDesc, currentLastUpdated

        repoName = response.css('strong.mr-2.flex-self-stretch a::text').get(default='').strip()
        readmeDiv = response.css('article[itemprop="text"]')

        file_rows = response.css('thead.Box-sc-g0xbh4-0.jGKpsv')  # these are the file entries
        isEmpty = len(file_rows) == 0

        idCount += 1
        rep = ET.SubElement(root, "repository")
        rep.set("id", str(idCount))
        ET.SubElement(rep, "URL").text = response.url
        ET.SubElement(rep, "last_updated").text = currentLastUpdated

        if isEmpty:
            ET.SubElement(rep, "name").text = currentDesc
            ET.SubElement(rep, "languages").text = "Empty"
            ET.SubElement(rep, "commits").text = "Empty"
            return
        else:
            ET.SubElement(rep, "name").text = repoName
            readme = ET.SubElement(rep, "README")

            if readmeDiv:
                readmeText = ' '.join(readmeDiv.css('::text').getall()).replace("\n", "").strip()
                readme.text = readmeText
            else:
                readme.text = 'no README'

            languageStats = response.css('div.BorderGrid-row:contains("Languages")')
            commits_text = response.css('span.fgColor-default::text').get(default='').strip()

            langEl = ET.SubElement(rep, "languages")
            commitsEl = ET.SubElement(rep, "commits")

            if languageStats:
                lang_list = languageStats.css('span.color-fg-default::text').getall()
                for lang in lang_list:
                    lang = lang.strip()
                    if lang:
                        ET.SubElement(langEl, "language").text = lang
            else:
                langEl.text = "None"

            commitsEl.text = commits_text if commits_text else "None"

            yield {
                'repositoryUrl': response.url,
                'name': repoName,
            }

    def closed(self, reason):
        tree = ET.ElementTree(root)
        tree.write("repositories.xml", encoding="utf-8", xml_declaration=True)
