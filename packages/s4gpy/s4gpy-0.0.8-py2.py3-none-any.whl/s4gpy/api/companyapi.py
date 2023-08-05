from munch import munchify

from s4gpy.api.utils import expand_links


class CompanyAPI:
    """This class wraps the company-mapper api."""

    def __init__(self, session):
        """Initialize a new CompanyAPI.

        It works by inheriting from the session object of a S4GAPI.
        """
        self.session = session

    def get_root(self):
        """Get the root of the company mapping api"""

        """return a list of companies links"""
        company_links = self.session.get("/").json()
        expand_links(self.session, company_links)
        return munchify(company_links)

    def get_companies(self):
        """Get all the companies in the system"""
        return self.get_root().companies()

    def get_contents(self):
        """Get all the contents in the systel"""
        return self.get_root().contents()

    def get_company(self, id):
        """retreives information from a particular company, identified by its cc_code"""
        r = self.session.get(f"/company/{id}")
        if r.status_code > 299:
            return None
        company_links = r.json()
        expand_links(self.session, company_links)
        return munchify(company_links)

    def get_content(self, id):
        """retreives information form a particular content, identified by its cc_code"""
        r = self.session.get(f"/content/{id}")
        if r.status_code > 299:
            return None
        content_links = r.json()
        expand_links(self.session, content_links)
        return munchify(content_links)

    def push_company(self, id, name, link):
        """Publish a new company."""
        self.session.post(f'/company/{id}',
                          json={'name': name, 'link': link})

    def push_content(self, id, company_names):
        """Publish a new content associated with some company names."""
        self.session.post(f'/content/{id}',
                          json={'company_names': [name for name in company_names]})

