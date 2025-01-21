from dataclasses import dataclass
from typing import Optional


@dataclass
class BaseModel:
    created_at: str
    modified_at: str

# CRM


@dataclass
class CRMContact(BaseModel):
    id: str
    first_name: str
    last_name: str
    email: str
    organization_id: Optional[str]
    hr_employee_id: Optional[str]
    salesforce_contact_id: Optional[str]


@dataclass
class CRMOrganization(BaseModel):
    id: str
    name: str
    salesforce_organization_id: Optional[str]

# HR


@dataclass
class HRDepartment(BaseModel):
    Id: str
    Name: str


@dataclass
class HREmployee(BaseModel):
    Id: str
    Name: str
    Surname: str
    Email: str
    DepartmentId: Optional[str]
    ManagerId: Optional[str]
    SalesforceContactId: Optional[str]

# Salesforce


@dataclass
class SalesforceContact(BaseModel):
    ID: str
    FirstName: str
    LastName: str
    Email: str
    Address: str
    OrganizationID: Optional[str]


@dataclass
class SalesforceOrganization(BaseModel):
    ID: str
    Name: str
    Address: str
