import requests
import re
import os
import logging
import sys
import archieml
from bs4 import BeautifulSoup, NavigableString, Tag
import io
from urllib.parse import urlparse
from urllib.parse import parse_qs
import base64
import markdown
import jinja2
import yaml
import shutil

templateLoader = jinja2.FileSystemLoader(searchpath="./templates")
templateEnv = jinja2.Environment(loader=templateLoader)
story_template = templateEnv.get_template("story.html")
homepage_template = templateEnv.get_template("homepage.html")

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
logging.getLogger("urllib3").setLevel(logging.WARNING)

# Setup file structure
try:
    shutil.rmtree("docs")
except:
    pass

os.makedirs("docs")
shutil.copytree("style", "docs/style")

def to_base64(url):
    response = requests.get(url)
    encoded = base64.b64encode(response.content).decode("ascii")
    return f"data:{response.headers['Content-Type']}; base64,{encoded}"

def to_text(element):
    if element.name is None:
        return str(element)
    
    if element.name == 'div':
        return element.decode_contents()

    non_text_children = [c for c in element.children if c.name is not None]
    if len(non_text_children) > 0:
        content = "\n".join([to_text(c) for c in non_text_children])
        if element.name == 'h3':
            return f"<p class='label super-font'>{content}</p>"
        else:
            return content
    else:
        if element.name == 'img':
            b64_img = to_base64(element['src'])
            img_content = ""
            if element['title']:
                img_content += f"<p class='label super-font'>{element['title']}</p>"
            if element['alt']:
                img_content += f"<p class='label-text super-font'>{element['alt']}</p>"
            img_content += f"<p class='img'><img src='{b64_img}'></p>"
            return "\n" + img_content + "\n"

        elif element.name == 'a':
            return f"<a href='{element['href']}'>{element.text}</a>"
        elif element.name == 'h3':
            return f"<p class='label super-font'>{element.text}</p>"
        elif element.name == 'span':
            return element.text
        else:
            return element.decode_contents()

def rewrite_page(doc):
    # Rewrite google-edited URLs
    for link in doc.find_all('a'):
        if 'href' in link:
            parsed = urlparse(link['href'])
            actual_url = parse_qs(parsed.query)['q'][0]
            link['href'] = actual_url

    # Rewrite datawrapper links as embeds
    chart_links = doc.find_all('a', text=re.compile(r".*datawrapper.*"))
    for chart_link in chart_links:
        dw_code = None
        options = [
            r"https://datawrapper.dwcdn.net/(.+)/1/",
            r"datawrapper.de/_/(.*)/"
        ]
        for option in options:
            try:
                dw_code = re.search(option, chart_link.text).group(1)
            except:
                pass

        if dw_code is None:
            logging.warning(f"Could not find datawrapper code from {chart_link.text}")
        else:
            logging.info(f"Found datawrapper code {dw_code}, adding embed")
            embed_code = """
            <div>
            <iframe title="A DataWrapper chart" 
                    aria-label="chart" id="datawrapper-chart-""" + dw_code + """"
                    src="https://datawrapper.dwcdn.net/""" + dw_code + """/1/"
                    scrolling="no"
                    frameborder="0" style="width: 0; min-width: 100% !important; border: none;" height="431">
            </iframe>
            <script type="text/javascript">!function(){"use strict";window.addEventListener("message",(function(a){if(void 0!==a.data["datawrapper-height"])for(var e in a.data["datawrapper-height"]){var t=document.getElementById("datawrapper-chart-"+e)||document.querySelector("iframe[src*='"+e+"']");t&&(t.style.height=a.data["datawrapper-height"][e]+"px")}}))}();</script>
            </div>
            """
            embed_doc = BeautifulSoup(embed_code, 'lxml')
            embed_div = embed_doc.html.body.div
            chart_link.replace_with(embed_div)

class Project:

    def __init__(self, url):
        logging.info(f"Initializing project from {url}")

        self.code = re.search(r"/d/([^/]*)", url).group(1)
        logging.info(f"Using code {self.code}")

        self.process_archieml()
        self.process_html()

    def process_archieml(self):
        logging.info("Processing text content")
        text_url = f"https://docs.google.com/document/d/{self.code}/export?format=txt"
        text = requests.get(text_url).text \
            .replace("http:","httpCOLON") \
            .replace("https:", "httpsCOLON")

        self.details = archieml.loads(text)
        for key, value in self.details.items():
            self.details[key] = value.replace("COLON", ":")

    def process_html(self):
        logging.info("Processing HTML content")

        html_url = f"https://docs.google.com/document/d/{self.code}/export?format=html"
        logging.info(f"Processing html content from {html_url}")
        
        response = requests.get(html_url)
        doc = BeautifulSoup(response.content, 'lxml')
        rewrite_page(doc)

        # Find the content section
        content_start = doc.find('span', text="content:").parent

        lines = []
        for sibling in content_start.next_siblings:
            if sibling.text == ":end":
                break

            if sibling.name == 'table':
                contents = "<div class='fake-table'>"
                for row in sibling.find_all("tr"):
                    contents += "<div>"
                    for cell in row.find_all("td"):
                        contents += f"<div>\n{markdown.markdown(to_text(cell))}\n</div>\n"
                    contents += "</div>"
                contents += "</div>"
            else:
                contents = " ".join([to_text(c) for c in sibling.children]).strip()

                if sibling.name == "ul":
                    contents = f"* {contents}"
                elif sibling.name == "ol":
                    contents = f"1. {contents}"
                elif sibling.name == 'h1':
                    contents = f"## {contents}"
                elif sibling.name == 'h2':
                    contents = f"### {contents}"
                elif sibling.name == 'h3':
                    contents = f"<p class='label super-font'>{contents}</p>"
                elif sibling.name == 'h4':
                    contents = f"<p class='label-text super-font'>{contents}</p>"

            lines.append(contents.strip())
        
        content = "\n".join(lines)
        self.raw_content = re.sub("\n+", "\n\n", content)
    
    def write_page(self):
        if 'slug' in self.details:
            self.foldername = self.details['slug']
        else:
            self.foldername = self.code

        os.makedirs(f"docs/{self.foldername}", exist_ok=True)
        filepath = f"docs/{self.foldername}/index.html"

        with open(filepath, 'w') as fp:
            content = markdown.markdown(self.raw_content)
            output = story_template.render(**self.details, processed_content=content)
            fp.write(output)

# Get all of the URLs from the text file
with open("details.yaml") as fp:
    details = yaml.load(fp, Loader=yaml.FullLoader)
    projects = [Project(url) for url in details['projects']]
    for project in projects:
        project.write_page()
    
    with open('docs/index.html', 'w') as fp:
        details['projects'] = projects
        hp_content = homepage_template.render(**details)
        fp.write(hp_content)
