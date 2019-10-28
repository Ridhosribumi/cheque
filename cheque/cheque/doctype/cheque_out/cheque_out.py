# -*- coding: utf-8 -*-
# Copyright (c) 2019, Ridhosribumi and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.utils import get_fullname, flt, cstr, formatdate
from frappe.model.document import Document
from erpnext.accounts.general_ledger import make_gl_entries
from erpnext.controllers.accounts_controller import AccountsController

class ChequeOut(AccountsController):

    def validate(self):
        self.validate_qty_is_not_zero()

    def validate_qty_is_not_zero(self):
        try:
            if self.items:
                pass
        except:
            pass

    def on_cancel(self):
        self.make_gl_entries(1)

    def make_gl_entries(self,cancel = 0, adv_adj=0):
        if flt(self.nominal_cheque) > 0 :
            gl_entries = self.get_gl_entries()
            make_gl_entries(gl_entries,cancel=cancel, adv_adj=adv_adj)

    def get_gl_entries(self):
        gl_entry = []
        gl_entry.append(
            self.get_gl_dict({
                "account": self.account_paid_from,
                "debit": self.nominal_cheque,
                "debit_in_account_currency": self.nominal_cheque,
                "against": self.bank_pay,
                "party_type": self.party_type,
                "party": self.party,
                "against_voucher_type": 'Payment Entry',
                "against_voucher": self.payment_entry,
                "remarks": 'Reference# {0} {1} dated {2} Note: {3}'.format(self.cheque_no,self.cheque_bank,formatdate(self.posting_date),self.payment_entry)
            })
        )
        gl_entry.append(
            self.get_gl_dict({
                "account": self.bank_pay,
                "credit": self.nominal_cheque,
                "credit_in_account_currency": self.nominal_cheque,
                "against": self.account_paid_from,
                "party_type": self.party_type,
                "party": self.party,
                "against_voucher_type": 'Payment Entry',
                "against_voucher": self.payment_entry,
                "remarks": 'Reference# {0} {1} dated {2} Note: {3}'.format(self.cheque_no,self.cheque_bank,formatdate(self.posting_date),self.payment_entry)
            })
        )
        return gl_entry

    def cancelled_check(self, cheque_status,invalid_date):
        self.disbursment_date = None
        self.bank_pay = None
        self.reference_no = None
        self.reference_date = None
        frappe.db.set(self,'cheque_status',cheque_status)
        frappe.db.set(self, 'invalid_date', invalid_date)
        self.make_gl_entries(1)

    def accepted_check(self, cheque_status,disbursment_date,bank_pay,reference_no,reference_date):
        self.invalid_date = None
        frappe.db.set(self,'cheque_status',cheque_status)
        frappe.db.set(self, 'disbursment_date', disbursment_date)
        frappe.db.set(self,'bank_pay',bank_pay)
        frappe.db.set(self,'reference_no',reference_no)
        frappe.db.set(self,'reference_date',reference_date)
        self.make_gl_entries()

    def rejected_check(self, cheque_status,rejected_date):
        frappe.db.set(self,'cheque_status',cheque_status)
        frappe.db.set(self, 'rejected_date', rejected_date)
        frappe.db.set(self,'bank_pay','')

@frappe.whitelist()
def delete_pe(pe):
    pe = frappe.get_doc("Payment Entry", {"name": pe})
    pe.flags.ignore_permissions = True
    pe.cancel()
    frappe.msgprint(_("Payment Entry {0} has been cancelled").format(pe))

@frappe.whitelist()
def status_cancel(name):
    x = frappe.db.sql("""UPDATE `tabCheque Out` SET docstatus = '2' WHERE name = %s""", name)
    return x
