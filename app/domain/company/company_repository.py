from abc import ABC, abstractmethod
from typing import List, Optional
from app.domain.company.company import Company

class CompanyRepository(ABC):

    @abstractmethod
    def find_all(self) -> List[Company]:
        pass

    @abstractmethod
    def find_by_id(self, company_id: int) -> Optional[Company]:
        pass

    @abstractmethod
    def find_by_name(self, keyword: str) -> List[Company]:
        pass

    @abstractmethod
    def find_all_by_name(self, keyword: str) -> List[Company]:
        pass