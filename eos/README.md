# End of Service (EOS) Module for Odoo 17

## Overview
This module implements end-of-service benefits calculation and management according to Kuwaiti labor law. It provides a comprehensive solution for managing employee terminations, calculating end-of-service benefits, and processing settlements.

## Features
- End-of-service benefit calculation based on Kuwaiti labor law
- Support for different termination reasons with specific calculation methods
- Configurable calculation formulas based on service periods
- Complete workflow for EOS requests (draft, submitted, approved, HR approved, paid)
- Integration with HR and accounting modules
- Comprehensive reporting and analysis tools
- Multi-company support
- Security access control with dedicated user groups

## Installation

### Prerequisites
- Odoo 17.0
- HR module installed
- Accounting module installed (optional, for accounting integration)

### Installation Steps
1. Download the module
2. Extract the module to your Odoo addons directory
3. Update the module list in Odoo
4. Install the "End of Service" module

## Configuration

### Initial Setup
1. Go to End of Service > Configuration > EOS Settings
2. Configure the default settings for EOS calculations
3. Go to End of Service > Configuration > Termination Reasons
4. Review and adjust the predefined termination reasons and calculation formulas
5. Go to End of Service > Configuration > Payment Methods
6. Configure payment methods for EOS settlements

### User Access Rights
The module provides two user groups:
- **EOS User**: Can create and view their own EOS requests
- **EOS Manager**: Can manage all EOS requests, approve requests, and configure the module

Assign users to these groups based on their responsibilities.

## Usage

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

## Technical Information

### Models
- `eos.settings`: Configuration settings for the module
- `eos.payment.method`: Payment methods for EOS settlements
- `eos.reason`: Termination reasons with calculation methods
- `eos.reason.formula`: Calculation formulas for different service periods
- `eos.request`: EOS requests with calculation results and workflow
- `eos.calculation.wizard`: Wizard for calculating EOS benefits

### Integration Points
- HR module: Employee and contract data
- Accounting module: Journal entries for EOS settlements

## Support
For support or customization requests, please contact the developer.

## License
This module is licensed under LGPL-3.

## Author
Developed by Manus AI
