#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
from datetime import date, timedelta
from odoo.tests.common import TransactionCase, tagged

@tagged('post_install', '-at_install')
class TestEOSCalculation(TransactionCase):
    def setUp(self):
        super(TestEOSCalculation, self).setUp()
        
        # Create test company
        self.company = self.env['res.company'].create({
            'name': 'Test Company',
            'currency_id': self.env.ref('base.KWD').id,
        })
        
        # Create test department
        self.department = self.env['hr.department'].create({
            'name': 'Test Department',
            'company_id': self.company.id,
        })
        
        # Create test job
        self.job = self.env['hr.job'].create({
            'name': 'Test Job',
            'company_id': self.company.id,
            'department_id': self.department.id,
        })
        
        # Create test employee
        self.employee = self.env['hr.employee'].create({
            'name': 'Test Employee',
            'company_id': self.company.id,
            'department_id': self.department.id,
            'job_id': self.job.id,
            'employee_number': 'EMP001',
        })
        
        # Create test contract
        self.contract = self.env['hr.contract'].create({
            'name': 'Test Contract',
            'employee_id': self.employee.id,
            'job_id': self.job.id,
            'department_id': self.department.id,
            'company_id': self.company.id,
            'wage': 1000.0,
            'date_start': date.today() - timedelta(days=365*6),  # 6 years ago
            'state': 'open',
        })
        
        # Get termination reasons
        self.reason_resignation_less_3 = self.env.ref('eos.reason_resignation_less_3_years')
        self.reason_resignation_3_to_5 = self.env.ref('eos.reason_resignation_3_to_5_years')
        self.reason_resignation_5_to_10 = self.env.ref('eos.reason_resignation_5_to_10_years')
        self.reason_resignation_more_10 = self.env.ref('eos.reason_resignation_more_10_years')
        self.reason_termination_less_5 = self.env.ref('eos.reason_termination_less_5_years')
        self.reason_termination_more_5 = self.env.ref('eos.reason_termination_more_5_years')
    
    def test_01_resignation_less_3_years(self):
        """Test EOS calculation for resignation with less than 3 years of service"""
        # Change contract start date to 2 years ago
        self.contract.write({
            'date_start': date.today() - timedelta(days=365*2),
        })
        
        # Create calculation wizard
        wizard = self.env['eos.calculation.wizard'].create({
            'employee_id': self.employee.id,
            'calculation_date': date.today(),
            'reason_id': self.reason_resignation_less_3.id,
        })
        
        # Check results
        self.assertAlmostEqual(wizard.service_years, 2.0, places=0)
        self.assertEqual(wizard.eos_days, 0)
        self.assertEqual(wizard.eos_amount, 0.0)
    
    def test_02_resignation_3_to_5_years(self):
        """Test EOS calculation for resignation with 3-5 years of service"""
        # Change contract start date to 4 years ago
        self.contract.write({
            'date_start': date.today() - timedelta(days=365*4),
        })
        
        # Create calculation wizard
        wizard = self.env['eos.calculation.wizard'].create({
            'employee_id': self.employee.id,
            'calculation_date': date.today(),
            'reason_id': self.reason_resignation_3_to_5.id,
        })
        
        # Check results
        self.assertAlmostEqual(wizard.service_years, 4.0, places=0)
        # 4 years * 15 days * 50% = 30 days
        self.assertEqual(wizard.eos_days, 30)
        # 30 days * (1000 / 30) = 1000
        self.assertEqual(wizard.eos_amount, 1000.0)
    
    def test_03_resignation_5_to_10_years(self):
        """Test EOS calculation for resignation with 5-10 years of service"""
        # Change contract start date to 7 years ago
        self.contract.write({
            'date_start': date.today() - timedelta(days=365*7),
        })
        
        # Create calculation wizard
        wizard = self.env['eos.calculation.wizard'].create({
            'employee_id': self.employee.id,
            'calculation_date': date.today(),
            'reason_id': self.reason_resignation_5_to_10.id,
        })
        
        # Check results
        self.assertAlmostEqual(wizard.service_years, 7.0, places=0)
        # 7 years * 15 days * 66.67% ≈ 70 days
        self.assertEqual(wizard.eos_days, 70)
        # 70 days * (1000 / 30) ≈ 2333.33
        self.assertAlmostEqual(wizard.eos_amount, 2333.33, places=2)
    
    def test_04_resignation_more_10_years(self):
        """Test EOS calculation for resignation with more than 10 years of service"""
        # Change contract start date to 12 years ago
        self.contract.write({
            'date_start': date.today() - timedelta(days=365*12),
        })
        
        # Create calculation wizard
        wizard = self.env['eos.calculation.wizard'].create({
            'employee_id': self.employee.id,
            'calculation_date': date.today(),
            'reason_id': self.reason_resignation_more_10.id,
        })
        
        # Check results
        self.assertAlmostEqual(wizard.service_years, 12.0, places=0)
        # First 5 years: 5 * 15 = 75 days
        # Remaining 7 years: 7 * 26 = 182 days
        # Total: 75 + 182 = 257 days
        self.assertEqual(wizard.eos_days, 257)
        # 257 days * (1000 / 30) ≈ 8566.67
        self.assertAlmostEqual(wizard.eos_amount, 8566.67, places=2)
    
    def test_05_termination_less_5_years(self):
        """Test EOS calculation for termination with less than 5 years of service"""
        # Change contract start date to 3 years ago
        self.contract.write({
            'date_start': date.today() - timedelta(days=365*3),
        })
        
        # Create calculation wizard
        wizard = self.env['eos.calculation.wizard'].create({
            'employee_id': self.employee.id,
            'calculation_date': date.today(),
            'reason_id': self.reason_termination_less_5.id,
        })
        
        # Check results
        self.assertAlmostEqual(wizard.service_years, 3.0, places=0)
        # 3 years * 15 days = 45 days
        self.assertEqual(wizard.eos_days, 45)
        # 45 days * (1000 / 30) = 1500
        self.assertEqual(wizard.eos_amount, 1500.0)
    
    def test_06_termination_more_5_years(self):
        """Test EOS calculation for termination with more than 5 years of service"""
        # Change contract start date to 8 years ago
        self.contract.write({
            'date_start': date.today() - timedelta(days=365*8),
        })
        
        # Create calculation wizard
        wizard = self.env['eos.calculation.wizard'].create({
            'employee_id': self.employee.id,
            'calculation_date': date.today(),
            'reason_id': self.reason_termination_more_5.id,
        })
        
        # Check results
        self.assertAlmostEqual(wizard.service_years, 8.0, places=0)
        # First 5 years: 5 * 15 = 75 days
        # Remaining 3 years: 3 * 26 = 78 days
        # Total: 75 + 78 = 153 days
        self.assertEqual(wizard.eos_days, 153)
        # 153 days * (1000 / 30) = 5100
        self.assertEqual(wizard.eos_amount, 5100.0)
    
    def test_07_create_eos_request(self):
        """Test creating an EOS request from calculation wizard"""
        # Create calculation wizard
        wizard = self.env['eos.calculation.wizard'].create({
            'employee_id': self.employee.id,
            'calculation_date': date.today(),
            'reason_id': self.reason_termination_more_5.id,
        })
        
        # Create EOS request
        result = wizard.action_create_request()
        
        # Check result
        self.assertEqual(result['res_model'], 'eos.request')
        
        # Get created request
        request_id = result['res_id']
        request = self.env['eos.request'].browse(request_id)
        
        # Check request data
        self.assertEqual(request.employee_id, self.employee)
        self.assertEqual(request.reason_id, self.reason_termination_more_5)
        self.assertEqual(request.termination_date, date.today())
        self.assertEqual(request.state, 'draft')
        
        # Test workflow
        request.action_submit()
        self.assertEqual(request.state, 'submitted')
        
        request.action_approve_manager()
        self.assertEqual(request.state, 'approved')
        
        request.action_approve_hr()
        self.assertEqual(request.state, 'hr_approved')
        
        request.action_pay()
        self.assertEqual(request.state, 'paid')

if __name__ == '__main__':
    unittest.main()
