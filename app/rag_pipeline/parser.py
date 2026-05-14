from collections import defaultdict
from bs4 import BeautifulSoup, Tag


class Parser:
    def __init__(self):
        self.paragraphs = defaultdict(list)

    def get_paragraphs(self, page: str) -> dict | None:
        soup = BeautifulSoup(page, "html.parser")
        container = soup.select_one(".mw-parser-output")
        if not container:
            container = soup
        if container.find("div", class_="redirectMsg"):
            return None

        facts = self.__parse_info_box(container)
        if facts:
            self.paragraphs["Facts"].append(facts)
        header = ["Overview"]
        ignored_headings = [
            "Portraits",
            "Quotes",
            "Questions",
            "Timeline",
            "Gallery",
            "History",
            "Fish Infograph",
            "Location Tables",
            "Fishing Zones",
        ]
        for node in container.children:
            if node.name == "h2":
                new_heading = self.__get_heading(node)
                if new_heading is None:
                    raise Exception("heading not found")
                header = [new_heading]

            if not isinstance(node, Tag) or header in ignored_headings:
                continue

            if node.name == "h3":
                new_sub_heading = self.__get_heading(node)
                if not new_sub_heading:
                    continue
                if len(header) > 1:
                    header.pop()
                header.append(new_sub_heading)
            elif node.name == "p":
                if header in ["Schedule", "Gifts"]:
                    continue
                self.__update_content(header, node.get_text(" ", strip=True))

            # table parsing
            elif node.name == "table":
                content = None
                classes = node.get("class", [])
                if header == "Schedule":
                    content = self.__parse_schedule(node)
                elif "wikitable" in classes or "mw-collapsible" in classes:
                    content = self.__parse_table(node)
                self.__update_content(header, content)
            elif node.name == "ul":
                text = self.__parse_list(node)
                self.__update_content(header, text)

        return self.paragraphs

    def __get_heading(self, el: Tag) -> str | None:
        text = el.select_one("span.mw-headline")
        if text:
            return text.get_text(strip=True)

    def __parse_table(self, el: Tag) -> str | None:
        """
        Output contract:
        TABLE_START
        CSV format table
        TABLE_END
        """
        body = el.select_one("tbody")
        if body is None:
            return None

        table_id = (el.get("id") or "").lower()
        classes = {c.lower() for c in (el.get("class") or [])}
        if table_id == "navbox" or "navbox" in classes:
            return None

        headers = [th.get_text(" ", strip=True) for th in body.select("tr th")]
        lines: list[str] = []

        for tr in body.select("tr"):
            tds = tr.select("td")
            if not tds:
                continue

            cells = [td.get_text(" ", strip=True) for td in tds]
            if not cells:
                continue

            lines.append("; ".join(cells))

        block: list[str] = ["TABLE_START"]
        if headers:
            block.append("; ".join(headers))
        block.append("\n".join(lines))
        block.append("TABLE_END")
        return "\n".join(block)

    def __parse_schedule(self, el: Tag) -> str:
        if el.find("table") is None:
            return self.__parse_table(el)
        body = el.select_one("tbody")
        title = body.select_one("tr th").get_text(strip=True)
        content = body.select_one("tr td")
        headers = [title]
        tables = []
        for node in content.children:
            if node.name == "p":
                if len(headers) > 1:
                    headers.pop()
                headers.append(node.get_text(strip=True))
                continue
            if node.name == "table":
                table = self.__parse_table(node)
                if table is None:
                    return
                tables.append(f"{"\n".join(headers)}\n{table}")
        return " ".join(tables)

    def __parse_info_box(self, soup: BeautifulSoup) -> str:
        infobox = soup.select_one("table#infoboxtable")
        if infobox is None:
            return None
        facts = ""
        for row in infobox.select("tr"):
            section = row.select_one("td#infoboxsection")
            detail = row.select_one("td#infoboxdetail")
            if section and detail:
                key = section.get_text(strip=True)
                value = self.__parse_detail(detail)
                facts += f"{key}:{value}. "
        return facts

    def __parse_detail(self, detail: Tag) -> str:
        nametemplate_spans = detail.select("span.nametemplate")
        if nametemplate_spans:
            return ", ".join([s.find("a").get_text(strip=True) for s in nametemplate_spans])

        paragraphs = detail.select("p")
        if paragraphs:
            return ", ".join([p.get_text(separator=" ", strip=True) for p in paragraphs])

        return detail.get_text(separator=" ", strip=True)

    def __parse_list(self, el: Tag) -> str:
        return " ".join(item.get_text(" ", strip=True) for item in el.find_all("li"))

    def __update_content(self, headings: list[str], text: str):
        if text:
            self.paragraphs[f"{'|'.join(headings)}"].append(text)
