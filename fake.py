"""
This script is used to generate fake data for Master Data Management (MDM) systems.

- CRM
  - Contacts
    - links to Organizations
    - links to HR Employees
    - links to Salesforce Contacts
  - Organizations
    - links to Salesforce Organizations
- HR
 - Departments
 - Employees
    - links to Departments (workplace)
    - links to Employees (managers)
    - links to Salesforce Contacts
- Salesforce
 - Contacts
 - Organizations
"""

import glob
import json
import os
import random
from dataclasses import dataclass

from faker import Faker

# CRM


@dataclass
class CRMContact:
    id: str
    first_name: str
    last_name: str
    email: str
    organization_id: str
    hr_employee_id: str
    salesforce_contact_id: str


@dataclass
class CRMOrganization:
    id: str
    name: str
    salesforce_organization_id: str

# HR


@dataclass
class HRDepartment:
    Id: str
    Name: str


@dataclass
class HREmployee:
    Id: str
    Name: str
    Surname: str
    Email: str
    DepartmentId: str
    ManagerId: str
    SalesforceContactId: str

# Salesforce


@dataclass
class SalesforceContact:
    ID: str
    FirstName: str
    LastName: str
    Email: str


@dataclass
class SalesforceOrganization:
    ID: str
    Name: str


def save_to_json(data, filename):
    with open(filename, 'w', encoding='utf8') as f:
        json.dump([d.__dict__ for d in data], f, indent=2)


def main():

    # Arrange

    if os.path.exists('./data'):
        for file in glob.glob('./data/*.json'):
            os.remove(file)
    else:
        os.makedirs('./data')

    crm_contacts = []
    crm_organizations = []
    hr_departments = []
    hr_employees = []
    salesforce_contacts = []
    salesforce_organizations = []

    # Config

    num_crm_contacts = 1_000
    num_crm_organizations = 100

    hr_department_names = [
        'Finance',
        'HR',
        'IT',
        'Marketing',
        'Sales',
        'Support',
        'Operations',
        'Legal',
        'R&D',
        'Production']
    num_hr_employees = 1_000

    num_salesforce_contacts = 1_000
    num_salesforce_organizations = 100

    num_crm_contacts_to_organizations = int(num_crm_contacts / 2)
    num_crm_contacts_to_hr_employees = int(num_crm_contacts / 2)
    num_crm_contacts_to_salesforce_contacts = int(num_crm_contacts / 2)

    num_crm_organizations_to_salesforce_organizations = int(
        num_crm_organizations / 2)

    num_hr_employees_to_salesforce_contacts = int(num_hr_employees / 2)

    fake = Faker()

    for _ in range(num_crm_contacts):
        crm_contacts.append(
            CRMContact(
                id=fake.uuid4(),
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                email=fake.email(),
                organization_id=None,
                hr_employee_id=None,
                salesforce_contact_id=None
            ))

    for _ in range(num_crm_organizations):
        crm_organizations.append(
            CRMOrganization(
                id=fake.uuid4(),
                name=fake.company(),
                salesforce_organization_id=None
            ))

    for hr_department_name in hr_department_names:
        hr_departments.append(
            HRDepartment(
                Id=fake.uuid4(),
                Name=hr_department_name
            ))

    for _ in range(num_hr_employees):
        hr_employees.append(
            HREmployee(
                Id=fake.uuid4(),
                Name=fake.first_name(),
                Surname=fake.last_name(),
                Email=fake.email(),
                DepartmentId=None,
                ManagerId=None,
                SalesforceContactId=None
            ))

    for _ in range(num_salesforce_contacts):
        salesforce_contacts.append(
            SalesforceContact(
                ID=fake.uuid4(),
                FirstName=fake.first_name(),
                LastName=fake.last_name(),
                Email=fake.email()
            ))

    for _ in range(num_salesforce_organizations):
        salesforce_organizations.append(
            SalesforceOrganization(
                ID=fake.uuid4(),
                Name=fake.company()
            ))

    for crm_contact in random.sample(crm_contacts, num_crm_contacts_to_organizations):
        crm_contact.organization_id = random.choice(crm_organizations).id

    for crm_contact in random.sample(crm_contacts, num_crm_contacts_to_hr_employees):
        crm_contact.hr_employee_id = random.choice(hr_employees).Id

    for crm_contact in random.sample(crm_contacts, num_crm_contacts_to_salesforce_contacts):
        crm_contact.salesforce_contact_id = random.choice(
            salesforce_contacts).ID

    for crm_organization in random.sample(
            crm_organizations, num_crm_organizations_to_salesforce_organizations):
        crm_organization.salesforce_organization_id = random.choice(
            salesforce_organizations).ID

    for hr_employee in random.sample(hr_employees, num_hr_employees_to_salesforce_contacts):
        hr_employee.SalesforceContactId = random.choice(
            salesforce_contacts).ID

    for hr_employee in hr_employees:
        hr_employee.DepartmentId = random.choice(hr_departments).Id

    for hr_department in hr_departments:
        department_employees = [
            employee for employee in hr_employees if employee.DepartmentId == hr_department.Id]
        for employee in department_employees:
            employee.ManagerId = random.choice(department_employees).Id

    # Save to json
    save_to_json(crm_contacts, './data/crm_contacts.json')
    save_to_json(crm_organizations, './data/crm_organizations.json')
    save_to_json(hr_departments, './data/hr_departments.json')
    save_to_json(hr_employees, './data/hr_employees.json')
    save_to_json(salesforce_contacts, './data/salesforce_contacts.json')
    save_to_json(salesforce_organizations,
                 './data/salesforce_organizations.json')


if __name__ == "__main__":
    main()
