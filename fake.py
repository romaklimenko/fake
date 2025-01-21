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
    - links to Organizations
 - Organizations
"""

import glob
import os
import random
from typing import List

from dotenv import load_dotenv
from faker import Faker

from data_classes import (CRMContact, CRMOrganization, HRDepartment,
                          HREmployee, SalesforceContact,
                          SalesforceOrganization)
from utils import mess_up_email, save_to_json, typo

load_dotenv()


def main():

    # Arrange

    if os.path.exists('./data'):
        for file in glob.glob('./data/*.json'):
            os.remove(file)
    else:
        os.makedirs('./data')

    crm_contacts: List[CRMContact] = []
    crm_organizations: List[CRMOrganization] = []
    hr_departments: List[HRDepartment] = []
    hr_employees: List[HREmployee] = []
    salesforce_contacts: List[SalesforceContact] = []
    salesforce_organizations: List[SalesforceOrganization] = []

    # Config

    num_crm_contacts: int = int(os.getenv('NUM_CRM_CONTACTS', '1000'))
    num_crm_organizations: int = int(os.getenv('NUM_CRM_ORGANIZATIONS', '100'))

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
    num_hr_employees: int = int(os.getenv('NUM_HR_EMPLOYEES', '1000'))

    num_salesforce_contacts: int = int(
        os.getenv('NUM_SALESFORCE_CONTACTS', '1000'))
    num_salesforce_organizations: int = int(
        os.getenv('NUM_SALESFORCE_ORGANIZATIONS', '100'))

    num_crm_contacts_to_organizations: int = int(
        os.getenv('NUM_CRM_CONTACTS_TO_ORGANIZATIONS', num_crm_contacts // 2))
    num_crm_contacts_to_hr_employees: int = int(
        os.getenv('NUM_CRM_CONTACTS_TO_HR_EMPLOYEES', num_crm_contacts // 2))
    num_crm_contacts_to_salesforce_contacts: int = int(
        os.getenv('NUM_CRM_CONTACTS_TO_SALESFORCE_CONTACTS', num_crm_contacts // 2))

    num_crm_organizations_to_salesforce_organizations: int = int(
        os.getenv('NUM_CRM_ORGANIZATIONS_TO_SALESFORCE_ORGANIZATIONS', num_crm_organizations // 2))

    num_hr_employees_to_salesforce_contacts: int = int(
        os.getenv('NUM_HR_EMPLOYEES_TO_SALESFORCE_CONTACTS', num_hr_employees // 2))

    fake = Faker()

    def random_date_pair():
        date1 = fake.date_time_between(start_date='-1y', end_date='now')
        date2 = fake.date_time_between(start_date=date1, end_date='now')
        return date1.isoformat(), date2.isoformat()

    for _ in range(num_crm_contacts):
        created_at, modified_at = random_date_pair()
        crm_contacts.append(
            CRMContact(
                id=fake.uuid4(),
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                email=mess_up_email(fake.email()),
                organization_id=None,
                hr_employee_id=None,
                salesforce_contact_id=None,
                created_at=created_at,
                modified_at=modified_at,
            ))

    for _ in range(num_crm_organizations):
        created_at, modified_at = random_date_pair()
        crm_organizations.append(
            CRMOrganization(
                id=fake.uuid4(),
                name=fake.company(),
                salesforce_organization_id=None,
                created_at=created_at,
                modified_at=modified_at,
            ))

    for hr_department_name in hr_department_names:
        created_at, modified_at = random_date_pair()
        hr_departments.append(
            HRDepartment(
                Id=fake.uuid4(),
                Name=hr_department_name,
                created_at=created_at,
                modified_at=modified_at,
            ))

    for _ in range(num_hr_employees):
        created_at, modified_at = random_date_pair()
        hr_employees.append(
            HREmployee(
                Id=fake.uuid4(),
                Name=fake.first_name(),
                Surname=fake.last_name(),
                Email=mess_up_email(fake.email()),
                DepartmentId=None,
                ManagerId=None,
                SalesforceContactId=None,
                created_at=created_at,
                modified_at=modified_at,
            ))

    for _ in range(num_salesforce_contacts):
        сreated_at, modified_at = random_date_pair()
        salesforce_contacts.append(
            SalesforceContact(
                ID=fake.uuid4(),
                FirstName=fake.first_name(),
                LastName=fake.last_name(),
                Email=mess_up_email(fake.email()),
                Address=fake.address(),
                OrganizationID=None,
                created_at=сreated_at,
                modified_at=modified_at,
            ))

    for _ in range(num_salesforce_organizations):
        created_at, modified_at = random_date_pair()
        salesforce_organizations.append(
            SalesforceOrganization(
                ID=fake.uuid4(),
                Name=fake.company(),
                Address=fake.address(),
                created_at=created_at,
                modified_at=modified_at,
            ))

    # Mix it up

    used_ids = set()

    # CRM Contacts

    # organization_id: Optional[str]
    for crm_contact in random.sample(crm_contacts, num_crm_contacts_to_organizations):
        crm_contact.organization_id = random.choice(crm_organizations).id

    # hr_employee_id: Optional[str]
    for crm_contact in random.sample(
            [contact for contact in crm_contacts if contact.id not in used_ids],
            num_crm_contacts_to_hr_employees):

        hr_employee = random.choice(hr_employees)

        if hr_employee.Id in used_ids:
            continue

        used_ids.add(crm_contact.id)
        used_ids.add(hr_employee.Id)

        crm_contact.hr_employee_id = hr_employee.Id
        crm_contact.first_name = typo(hr_employee.Name)
        crm_contact.last_name = typo(hr_employee.Surname)
        if random.random() > 0.5:
            crm_contact.email = typo(
                hr_employee.Email, unchanged_probability=0.9)

    # salesforce_contact_id: Optional[str]
    for crm_contact in random.sample(
            [contact for contact in crm_contacts if contact.id not in used_ids],
            num_crm_contacts_to_salesforce_contacts):

        if crm_contact.id in used_ids:
            continue

        used_ids.add(crm_contact.id)
        used_ids.add(crm_contact.id)

        salesforce_contact = random.choice(salesforce_contacts)
        crm_contact.salesforce_contact_id = salesforce_contact.ID
        crm_contact.first_name = typo(salesforce_contact.FirstName)
        crm_contact.last_name = typo(salesforce_contact.LastName)
        crm_contact.email = mess_up_email(
            typo(
                salesforce_contact.Email,
                unchanged_probability=0.9),
            unchanged_probability=0.9)

    # CRM Organizations

    # salesforce_organization_id: Optional[str]
    for crm_organization in random.sample(
            [organization for organization in crm_organizations if organization.id not in used_ids],
            num_crm_organizations_to_salesforce_organizations):

        salesforce_organization = random.choice(salesforce_organizations)

        if salesforce_organization.ID in used_ids:
            continue

        used_ids.add(crm_organization.id)
        used_ids.add(salesforce_organization.ID)

        crm_organization.salesforce_organization_id = salesforce_organization.ID
        crm_organization.name = typo(salesforce_organization.Name)

    # HR Employees

    # DepartmentId: Optional[str]
    for hr_employee in hr_employees:
        hr_employee.DepartmentId = random.choice(hr_departments).Id

    # ManagerId: Optional[str]
    for hr_department in hr_departments:
        department_employees = [
            employee for employee in hr_employees if employee.DepartmentId == hr_department.Id]
        for employee in department_employees:
            employee.ManagerId = random.choice(department_employees).Id

    # SalesforceContactId: Optional[str]
    for hr_employee in random.sample(
            [employee for employee in hr_employees if employee.Id not in used_ids],
            num_hr_employees_to_salesforce_contacts):

        salesforce_contact = random.choice(salesforce_contacts)

        if salesforce_contact.ID in used_ids:
            continue

        used_ids.add(hr_employee.Id)
        used_ids.add(salesforce_contact.ID)

        hr_employee.SalesforceContactId = salesforce_contact.ID
        hr_employee.Name = typo(salesforce_contact.FirstName)
        hr_employee.Surname = typo(salesforce_contact.LastName)
        hr_employee.Email = mess_up_email(
            typo(
                salesforce_contact.Email,
                unchanged_probability=0.9),
            unchanged_probability=0.9)

    # Salesforce Contacts
    for salesforce_contact in salesforce_contacts:
        salesforce_contact.OrganizationID = random.choice(
            salesforce_organizations).ID

    # Save to json
    save_to_json(crm_contacts, './data/crm_contacts.json')
    save_to_json(crm_organizations, './data/crm_organizations.json')
    save_to_json(hr_departments, './data/hr_departments.json')
    save_to_json(hr_employees, './data/hr_employees.json')
    save_to_json(salesforce_contacts, './data/salesforce_contacts.json')
    save_to_json(salesforce_organizations,
                 './data/salesforce_organizations.json')


if __name__ == '__main__':
    main()
