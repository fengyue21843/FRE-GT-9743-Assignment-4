from __future__ import annotations
from atexit import register
from typing import Any, Dict, List, Tuple
import pandas as pd
from functools import singledispatchmethod
from fixedincomelib.product.product_interfaces import Product, ProductVisitor
from fixedincomelib.product.product_portfolio import ProductPortfolio
from fixedincomelib.product.linear_products import (
    ProductBulletCashflow,
    ProductFixedAccrued,
    ProductOvernightIndexCashflow,
    ProductRFRSwap,
)


class ProductDisplayVisitor(ProductVisitor):

    def __init__(self) -> None:
        super().__init__()
        self.nvps_ = []

    @singledispatchmethod
    def visit(self, product: Product):
        raise NotImplementedError(f"No visitor for {Product._product_type}")

    def display(self) -> pd.DataFrame:
        return pd.DataFrame(self.nvps_, columns=["Name", "Value"])

    # TODO: ProductBulletCashflow
    @visit.register
    def _(self, product: ProductBulletCashflow):
        self.nvps_.append(("Product Type", product.product_type))
        self.nvps_.append(("Termination Date", product.termination_date.ISO()))
        self.nvps_.append(("Payment Date", product.payment_date.ISO()))
        self.nvps_.append(("Currency", product.currency.value_str))
        self.nvps_.append(("Notional", f"{product.notional:,.2f}"))
        self.nvps_.append(("Direction", product.long_or_short.to_string()))
        return self

    # TODO: ProductFixedAccrued
    @visit.register
    def _(self, product: ProductFixedAccrued):
        self.nvps_.append(("Product Type", product.product_type))
        self.nvps_.append(("Effective Date", product.effective_date.ISO()))
        self.nvps_.append(("Termination Date", product.termination_date.ISO()))
        self.nvps_.append(("Payment Date", product.payment_date.ISO()))
        self.nvps_.append(("Currency", product.currency.value_str))
        self.nvps_.append(("Notional", f"{product.notional:,.2f}"))
        self.nvps_.append(("Accrual Basis", product.accrual_basis.value_str))
        self.nvps_.append(("Business Day Convention", product.business_day_convention.value_str))
        self.nvps_.append(("Holiday Convention", product.holiday_convention.value_str))
        self.nvps_.append(("Accrued", f"{product.accrued:.6f}"))
        self.nvps_.append(("Direction", product.long_or_short.to_string()))
        return self

    # TODO: ProductOvernightIndexCashflow
    @visit.register
    def _(self, product: ProductOvernightIndexCashflow):
        self.nvps_.append(("Product Type", product.product_type))
        self.nvps_.append(("Effective Date", product.effective_date.ISO()))
        self.nvps_.append(("Termination Date", product.termination_date.ISO()))
        self.nvps_.append(("Payment Date", product.payment_date.ISO()))
        self.nvps_.append(("Overnight Index", product.on_index.name()))
        self.nvps_.append(("Currency", product.currency.value_str))
        self.nvps_.append(("Notional", f"{product.notional:,.2f}"))
        self.nvps_.append(("Compounding Method", product.compounding_method.to_string()))
        self.nvps_.append(("Spread", f"{product.spread:.4%}"))
        self.nvps_.append(("Direction", product.long_or_short.to_string()))
        return self

    # TODO: ProductRFRSwap
    @visit.register
    def _(self, product: ProductRFRSwap):
        self.nvps_.append(("Product Type", product.product_type))
        self.nvps_.append(("Effective Date", product.effective_date.ISO()))
        self.nvps_.append(("Termination Date", product.termination_date.ISO()))
        self.nvps_.append(("Overnight Index", product.on_index.name()))
        self.nvps_.append(("Fixed Rate", f"{product.fixed_rate:.4%}"))
        self.nvps_.append(("Pay or Receive", product.pay_or_rec.to_string()))
        self.nvps_.append(("Currency", product.currency.value_str))
        self.nvps_.append(("Notional", f"{product.notional:,.2f}"))
        self.nvps_.append(("Accrual Period", str(product.accrual_period)))
        self.nvps_.append(("Floating Leg Accrual Period", str(product.floating_leg_accrual_period)))
        self.nvps_.append(("Accrual Basis", product.accrual_basis.value_str))
        self.nvps_.append(("Spread", f"{product.spread:.4%}"))
        self.nvps_.append(("Compounding Method", product.compounding_method.to_string()))
        self.nvps_.append(("Payment Offset", str(product.pay_offset)))
        self.nvps_.append(("Fixed Leg Cashflows", product.fixed_leg_.num_cashflows()))
        self.nvps_.append(("Floating Leg Cashflows", product.floating_leg_.num_cashflows()))
        self.nvps_.append(("Direction", product.long_or_short.to_string()))
        return self
