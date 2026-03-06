class CompanyNotFound(Exception):
    def __init__(self, company_id: int):
        super().__init__(f"Company not found: {company_id}")
        self.company_id = company_id

class CompanyNameNotFound(Exception):
    def __init__(self, company_name: str):
        super().__init__(f"Company Name not found: {company_name}")
        self.company_name = company_name