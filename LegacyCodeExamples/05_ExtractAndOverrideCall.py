# 05_ExtractAndOverrideCall.py
# Real-life example: In a web scraper, extract HTTP request logic into a method, override in tests with mock responses.

class WebScraper:
    def scrape(self, url):
        html = self.fetch_html(url)  # Extracted
        return self.parse_html(html)

    def fetch_html(self, url):
        import requests
        return requests.get(url).text

    def parse_html(self, html):
        return html.upper()  # Simulate parsing

# Test subclass
class TestScraper(WebScraper):
    def fetch_html(self, url):
        return "<html>Test</html>"  # Mock

# scraper = TestScraper()
# assert scraper.scrape("dummy") == "<HTML>TEST</HTML>"

# Real-life example: For a calculation-heavy function, extract database queries into methods, override with in-memory data.

class ReportGenerator:
    def generate_report(self):
        data = self.query_data()  # Extracted
        return self.calculate_total(data)

    def query_data(self):
        # Simulate DB query
        return [100, 200, 300]

    def calculate_total(self, data):
        return sum(data)

# Test subclass
class TestReportGenerator(ReportGenerator):
    def query_data(self):
        return [1, 2, 3]  # Mock data

# gen = TestReportGenerator()
# assert gen.generate_report() == 6