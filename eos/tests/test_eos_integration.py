#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import unittest
from odoo.tests.common import SavepointCase

class TestEOSIntegration(SavepointCase):
    @classmethod
    def setUpClass(cls):
        super(TestEOSIntegration, cls).setUpClass()
        
        # Create test data for integration testing
        cls.env = cls.env(context=dict(cls.env.context, tracking_disable=True))
        
        # Create test user with EOS manager rights
        cls.eos_manager = cls.env['res.users'].create({
            'name': 'EOS Manager',
            'login': 'eos_manager',
            'email': 'eos_manager@example.com',
            'groups_id': [(6, 0, [
                cls.env.ref('eos.group_eos_manager').id,
                cls.env.ref('base.group_user').id
            ])]
        })
        
        # Create test user with EOS user rights
        cls.eos_user = cls.env['res.users'].create({
            'name': 'EOS User',
            'login': 'eos_user',
            'email': 'eos_user@example.com',
            'groups_id': [(6, 0, [
                cls.env.ref('eos.group_eos_user').id,
                cls.env.ref('base.group_user').id
            ])]
        })
        
        # Create test employees
        cls.employee1 = cls.env['hr.employee'].create({
            'name': 'Test Employee 1',
            'employee_number': 'EMP001',
            'user_id': cls.eos_user.id,
        })
        
        cls.employee2 = cls.env['hr.employee'].create({
            'name': 'Test Employee 2',
            'employee_number': 'EMP002',
        })
        
        # Create test contracts
        cls.contract1 = cls.env['hr.contract'].create({
            'name': 'Contract for Employee 1',
            'employee_id': cls.employee1.id,
            'wage': 1200.0,
            'date_start': '2020-01-01',
            'state': 'open',
        })
        
        cls.contract2 = cls.env['hr.contract'].create({
            'name': 'Contract for Employee 2',
            'employee_id': cls.employee2.id,
            'wage': 1500.0,
            'date_start': '2015-01-01',
            'state': 'open',
        })
    
    def test_01_security_access_rights(self):
        """Test security access rights for EOS module"""
        # Test as EOS user
        eos_request_model = self.env['eos.request'].with_user(self.eos_user)
        eos_reason_model = self.env['eos.reason'].with_user(self.eos_user)
        eos_settings_model = self.env['eos.settings'].with_user(self.eos_user)
        
        # EOS user should be able to read reasons but not create
        reasons = eos_reason_model.search([])
        self.assertTrue(reasons, "EOS user should be able to read reasons")
        
        # EOS user should be able to read settings but not create
        settings = eos_settings_model.search([])
        self.assertTrue(settings, "EOS user should be able to read settings")
        
        # EOS user should be able to create requests for themselves
        request = eos_request_model.create({
            'employee_id': self.employee1.id,
            'request_date': '2025-03-23',
            'termination_date': '2025-04-23',
            'reason_id': self.env.ref('eos.reason_resignation_more_10_years').id,
        })
        self.assertTrue(request, "EOS user should be able to create requests for themselves")
        
        # EOS user should not be able to create requests for others
        with self.assertRaises(Exception):
            eos_request_model.create({
                'employee_id': self.employee2.id,
                'request_date': '2025-03-23',
                'termination_date': '2025-04-23',
                'reason_id': self.env.ref('eos.reason_resignation_more_10_years').id,
            })
        
        # Test as EOS manager
        eos_request_model_mgr = self.env['eos.request'].with_user(self.eos_manager)
        eos_reason_model_mgr = self.env['eos.reason'].with_user(self.eos_manager)
        eos_settings_model_mgr = self.env['eos.settings'].with_user(self.eos_manager)
        
        # EOS manager should be able to create reasons
        reason = eos_reason_model_mgr.create({
            'name': 'Test Reason',
            'code': 'test_reason',
            'calculation_method': 'none',
        })
        self.assertTrue(reason, "EOS manager should be able to create reasons")
        
        # EOS manager should be able to create settings
        setting = eos_settings_model_mgr.create({
            'name': 'Test Settings',
            'default_days_per_year': 30,
            'default_days_per_month': 30,
        })
        self.assertTrue(setting, "EOS manager should be able to create settings")
        
        # EOS manager should be able to create requests for any employee
        request2 = eos_request_model_mgr.create({
            'employee_id': self.employee2.id,
            'request_date': '2025-03-23',
            'termination_date': '2025-04-23',
            'reason_id': self.env.ref('eos.reason_resignation_more_10_years').id,
        })
        self.assertTrue(request2, "EOS manager should be able to create requests for any employee")
    
    def test_02_workflow_integration(self):
        """Test the complete workflow of an EOS request"""
        # Create request as manager
        eos_request_model = self.env['eos.request'].with_user(self.eos_manager)
        
        request = eos_request_model.create({
            'employee_id': self.employee2.id,
            'request_date': '2025-03-23',
            'termination_date': '2025-04-23',
            'reason_id': self.env.ref('eos.reason_termination_more_5_years').id,
        })
        
        # Check initial state
        self.assertEqual(request.state, 'draft', "Initial state should be draft")
        
        # Submit request
        request.action_submit()
        self.assertEqual(request.state, 'submitted', "State should be submitted after submission")
        
        # Manager approval
        request.action_approve_manager()
        self.assertEqual(request.state, 'approved', "State should be approved after manager approval")
        
        # HR approval
        request.action_approve_hr()
        self.assertEqual(request.state, 'hr_approved', "State should be hr_approved after HR approval")
        
        # Mark as paid
        request.action_pay()
        self.assertEqual(request.state, 'paid', "State should be paid after payment")
        
        # Test cancellation and reset to draft
        request2 = eos_request_model.create({
            'employee_id': self.employee1.id,
            'request_date': '2025-03-23',
            'termination_date': '2025-04-23',
            'reason_id': self.env.ref('eos.reason_termination_less_5_years').id,
        })
        
        request2.action_submit()
        self.assertEqual(request2.state, 'submitted', "State should be submitted after submission")
        
        request2.action_cancel()
        self.assertEqual(request2.state, 'cancelled', "State should be cancelled after cancellation")
        
        request2.action_draft()
        self.assertEqual(request2.state, 'draft', "State should be draft after reset")
    
    def test_03_calculation_wizard_integration(self):
        """Test the integration of calculation wizard with EOS request creation"""
        # Create calculation wizard
        wizard = self.env['eos.calculation.wizard'].with_user(self.eos_manager).create({
            'employee_id': self.employee2.id,
            'calculation_date': '2025-04-23',
            'reason_id': self.env.ref('eos.reason_termination_more_5_years').id,
        })
        
        # Check calculation results
        self.assertTrue(wizard.service_years > 10, "Service years should be more than 10")
        self.assertTrue(wizard.eos_days > 0, "EOS days should be calculated")
        self.assertTrue(wizard.eos_amount > 0, "EOS amount should be calculated")
        
        # Create request from wizard
        result = wizard.action_create_request()
        self.assertEqual(result['res_model'], 'eos.request', "Should return an EOS request")
        
        # Check created request
        request = self.env['eos.request'].browse(result['res_id'])
        self.assertEqual(request.employee_id.id, self.employee2.id, "Employee should match")
        self.assertEqual(request.termination_date, wizard.calculation_date, "Termination date should match")
        self.assertEqual(request.reason_id.id, wizard.reason_id.id, "Reason should match")
        self.assertEqual(request.eos_days, wizard.eos_days, "EOS days should match")
        self.assertEqual(request.eos_amount, wizard.eos_amount, "EOS amount should match")

if __name__ == '__main__':
    unittest.main()
