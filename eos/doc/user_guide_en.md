# User Guide - End of Service (EOS) Module

## Introduction
The End of Service module is a comprehensive solution for managing and calculating end-of-service benefits for employees according to Kuwaiti labor law. This module provides an easy mechanism for calculating end-of-service benefits based on the reason for termination and the employee's length of service.

## Key Features
- End-of-service benefit calculation according to Kuwaiti labor law
- Support for different termination reasons with specific calculation methods
- Configurable calculation formulas based on service periods
- Complete workflow for EOS requests (draft, submitted, approved, HR approved, paid)
- Integration with HR and accounting modules
- Comprehensive reporting and analysis tools
- Multi-company support
- Security access control with dedicated user groups

## Initial Setup

### System Configuration
1. Go to End of Service > Configuration > EOS Settings
2. Configure the default settings for EOS calculations
3. Go to End of Service > Configuration > Termination Reasons
4. Review and adjust the predefined termination reasons and calculation formulas
5. Go to End of Service > Configuration > Payment Methods
6. Configure payment methods for EOS settlements

### User Permissions
The module provides two user groups:
- **EOS User**: Can create and view their own EOS requests
- **EOS Manager**: Can manage all EOS requests, approve requests, and configure the module

Assign users to these groups based on their responsibilities.

## Usage Guide

### Calculating EOS Benefits
1. Go to End of Service > Requests > Calculate EOS
2. Select the employee, calculation date, and termination reason
3. Review the calculated benefits
4. Click "Create EOS Request" to create a formal request

### Managing EOS Requests
1. Go to End of Service > Requests > End of Service Requests
2. Create a new request or view existing requests
3. Follow the workflow: Draft > Submitted > Approved > HR Approved > Paid

### Reporting
1. Go to End of Service > Reporting > EOS Analysis
2. Use the pivot, graph, and calendar views to analyze EOS data

## Kuwaiti Labor Law Implementation

### Resignation Scenarios
- **Less than 3 years of service**: No EOS benefit
- **3-5 years of service**: Half of the full benefit (15 days per year)
- **5-10 years of service**: Two-thirds of the full benefit (15 days per year)
- **More than 10 years of service**: Full benefit (15 days per year for first 5 years, 26 days per year thereafter)

### Termination Scenarios
- **During probation period**: No EOS benefit
- **Less than 5 years of service**: 15 days per year
- **More than 5 years of service**: 15 days per year for first 5 years, 26 days per year thereafter

## Frequently Asked Questions

### How is the end-of-service benefit calculated?
The end-of-service benefit is calculated based on the employee's basic salary, length of service, and reason for termination. Different formulas are applied depending on the termination reason and service period according to Kuwaiti labor law.

### Can an employee request a partial withdrawal of end-of-service benefits?
Yes, the system supports partial withdrawal of end-of-service benefits during the employee's employment period. The amount available for withdrawal is calculated based on the length of service up to the request date.

### How are unpaid leaves handled in the service period calculation?
Unpaid leave days are excluded from the total service period when calculating end-of-service benefits.

### Can EOS reports be exported?
Yes, all reports can be exported in various formats such as PDF, Excel, and CSV.

## Troubleshooting

### Incorrect Calculations
- Ensure the employee's contract start date is correct
- Check the termination reason settings and calculation formulas
- Make sure the employee's basic salary is up to date

### Workflow Error
- Ensure the user has the appropriate permissions
- Check the current request status before attempting to move to the next state

### Reporting Issues
- Ensure there is sufficient data for the selected period
- Check the filtering and grouping settings in the report

## Technical Support
For technical support or customization requests, please contact the development team.
