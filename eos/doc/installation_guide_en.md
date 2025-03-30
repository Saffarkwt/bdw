# Installation and Configuration Guide - End of Service (EOS) Module

## System Requirements
- Odoo 17.0
- HR module installed
- Accounting module installed (optional, for accounting integration)

## Installation Steps

### Manual Installation
1. Download the module
2. Extract the module to your Odoo addons directory
3. Update the module list in Odoo
4. Install the "End of Service" module

### Installation Using Git
```bash
cd /path/to/odoo/addons
git clone https://github.com/your-repository/eos.git
```

Then update the module list in Odoo and install the "End of Service" module.

## Initial Configuration

### System Setup
1. Go to End of Service > Configuration > EOS Settings
2. Configure the default settings for EOS calculations:
   - Default days per year: 30 (adjustable)
   - Default days per month: 30 (adjustable)
   - EOS expense account (if accounting integration is enabled)
   - EOS payable account (if accounting integration is enabled)
   - EOS journal (if accounting integration is enabled)

### Setting Up Termination Reasons
1. Go to End of Service > Configuration > Termination Reasons
2. Review and adjust the predefined termination reasons:
   - Resignation (Less than 3 years)
   - Resignation (3-5 years)
   - Resignation (5-10 years)
   - Resignation (More than 10 years)
   - Termination during probation
   - Termination (Less than 5 years)
   - Termination (More than 5 years)
   - Partial EOS withdrawal

3. For each reason, ensure the calculation method and associated calculation formulas are correct.

### Setting Up Payment Methods
1. Go to End of Service > Configuration > Payment Methods
2. Review and adjust the predefined payment methods:
   - Cash
   - Check
   - Bank Transfer

### Setting Up User Permissions
1. Go to Settings > Users & Companies > Users
2. Select the user you want to grant EOS permissions to
3. Go to the "Technical Access Rights" tab
4. Assign the user to one of the following groups:
   - EOS User: For employees who need to create and view their own EOS requests
   - EOS Manager: For managers who need to manage all EOS requests, approve requests, and configure the module

## Integration with Other Modules

### HR Module Integration
The EOS module fully integrates with the HR module:
- Uses employee and contract data for EOS calculations
- Adds an "End of Service" tab to the employee contract form
- Adds an "EOS Requests" button to the employee form

### Accounting Module Integration (Optional)
If the accounting module is installed, the EOS module can be configured to create automatic accounting entries:
1. Go to End of Service > Configuration > EOS Settings
2. Configure the accounts and journal for EOS
3. When an EOS request is paid, an accounting entry will be automatically created

## Maintenance and Updates

### Backup
Before updating the module, it is recommended to create a backup of the database:
```bash
pg_dump -U odoo_user -d odoo_database > eos_backup.sql
```

### Updating
To update the module:
1. Download the latest version of the module
2. Replace the existing files with the new files
3. Update the module from the Odoo interface

## Troubleshooting

### Installation Issues
- Ensure the module version is compatible with your Odoo version
- Check that all required dependencies are installed
- Review Odoo logs for specific error messages

### Configuration Issues
- Ensure all required settings are configured
- Check the calculation formulas for termination reasons
- Make sure users have the appropriate permissions

### Calculation Issues
- Ensure employee contract data is correct
- Check the configuration of termination reasons and calculation formulas
- Review the Kuwaiti labor law to ensure calculations are correct

## Technical Support
For technical support or customization requests, please contact the development team.
