from __future__ import annotations
import numpy as np
from typing import Dict, List, Set, Tuple
from nesy_mbst.core.state_machine import MarkovChain
from nesy_mbst.symbolic.constraint_solver import ConstraintSolver, SolverConfig
from nesy_mbst.neural.constraint_extractor import ConstraintExtractor
from nesy_mbst.symbolic.closed_loop import ClosedLoopAdapter, TelemetrySample
from nesy_mbst.testing.test_generator import StatisticalTestGenerator
from nesy_mbst.testing.metrics import Metrics


def build_ecommerce_user_model() -> Dict:
    states = [
        "Home", "BrowseProducts", "ProductDetail", "AddToCart",
        "ViewCart", "Checkout", "Payment", "OrderConfirmation",
        "SearchResults", "UserProfile", "Wishlist", "Reviews",
        "CompareProducts", "CategoryBrowse", "FilterResults",
        "ShippingInfo", "PaymentMethod", "OrderHistory",
        "ReturnRequest", "CustomerSupport", "Logout",
        "ErrorPage", "LoadingState", "SessionTimeout",
    ]
    transitions = [
        ("Home", "BrowseProducts"), ("Home", "SearchResults"),
        ("Home", "UserProfile"), ("Home", "Wishlist"),
        ("Home", "OrderHistory"), ("Home", "Logout"),
        ("BrowseProducts", "ProductDetail"), ("BrowseProducts", "CategoryBrowse"),
        ("BrowseProducts", "CompareProducts"), ("BrowseProducts", "Home"),
        ("ProductDetail", "AddToCart"), ("ProductDetail", "Reviews"),
        ("ProductDetail", "BrowseProducts"), ("ProductDetail", "Home"),
        ("AddToCart", "ViewCart"), ("AddToCart", "ProductDetail"),
        ("AddToCart", "BrowseProducts"),
        ("ViewCart", "Checkout"), ("ViewCart", "BrowseProducts"),
        ("ViewCart", "Home"), ("ViewCart", "Wishlist"),
        ("Checkout", "Payment"), ("Checkout", "ShippingInfo"),
        ("Checkout", "ViewCart"),
        ("Payment", "PaymentMethod"), ("Payment", "OrderConfirmation"),
        ("Payment", "Checkout"),
        ("OrderConfirmation", "Home"), ("OrderConfirmation", "OrderHistory"),
        ("SearchResults", "ProductDetail"), ("SearchResults", "FilterResults"),
        ("SearchResults", "Home"),
        ("UserProfile", "OrderHistory"), ("UserProfile", "Home"),
        ("Wishlist", "ProductDetail"), ("Wishlist", "AddToCart"),
        ("Wishlist", "Home"),
        ("Reviews", "ProductDetail"), ("Reviews", "Home"),
        ("CompareProducts", "ProductDetail"), ("CompareProducts", "BrowseProducts"),
        ("CategoryBrowse", "BrowseProducts"), ("CategoryBrowse", "FilterResults"),
        ("CategoryBrowse", "Home"),
        ("FilterResults", "ProductDetail"), ("FilterResults", "BrowseProducts"),
        ("ShippingInfo", "Checkout"), ("ShippingInfo", "Home"),
        ("PaymentMethod", "Payment"), ("PaymentMethod", "Home"),
        ("OrderHistory", "Home"), ("OrderHistory", "ReturnRequest"),
        ("ReturnRequest", "CustomerSupport"), ("ReturnRequest", "Home"),
        ("CustomerSupport", "Home"), ("CustomerSupport", "ReturnRequest"),
        ("ErrorPage", "Home"), ("ErrorPage", "BrowseProducts"),
        ("LoadingState", "BrowseProducts"), ("LoadingState", "Home"),
        ("SessionTimeout", "Home"), ("SessionTimeout", "Logout"),
        ("Logout", "Home"),
    ]
    requirements = (
        "E-commerce user flow: Users typically browse products rather than searching directly. "
        "After viewing a product detail, users usually add to cart rather than leaving. "
        "Checkout is more common than returning to browse from the cart. "
        "Payment is typically completed rather than abandoned. "
        "Order confirmation usually leads to browsing again. "
        "Error pages and loading states are rare."
    )
    return {
        "name": "E-Commerce User Model",
        "states": states,
        "transitions": transitions,
        "requirements": requirements,
        "terminal_states": {"Logout", "SessionTimeout"},
    }


def build_ecommerce_admin_model() -> Dict:
    states = [
        "AdminLogin", "Dashboard", "ProductManagement", "OrderManagement",
        "UserManagement", "Analytics", "InventoryManagement",
        "AddProduct", "EditProduct", "ViewOrders", "ProcessRefund",
        "ManageUsers", "Reports", "Settings", "Logout",
        "ErrorState", "LoadingState",
    ]
    transitions = [
        ("AdminLogin", "Dashboard"),
        ("Dashboard", "ProductManagement"), ("Dashboard", "OrderManagement"),
        ("Dashboard", "UserManagement"), ("Dashboard", "Analytics"),
        ("Dashboard", "Settings"), ("Dashboard", "Logout"),
        ("ProductManagement", "AddProduct"), ("ProductManagement", "EditProduct"),
        ("ProductManagement", "Dashboard"), ("ProductManagement", "InventoryManagement"),
        ("OrderManagement", "ViewOrders"), ("OrderManagement", "ProcessRefund"),
        ("OrderManagement", "Dashboard"),
        ("UserManagement", "ManageUsers"), ("UserManagement", "Dashboard"),
        ("Analytics", "Reports"), ("Analytics", "Dashboard"),
        ("InventoryManagement", "ProductManagement"), ("InventoryManagement", "Dashboard"),
        ("AddProduct", "ProductManagement"), ("AddProduct", "Dashboard"),
        ("EditProduct", "ProductManagement"), ("EditProduct", "Dashboard"),
        ("ViewOrders", "OrderManagement"), ("ViewOrders", "ProcessRefund"),
        ("ProcessRefund", "OrderManagement"), ("ProcessRefund", "Dashboard"),
        ("ManageUsers", "UserManagement"), ("ManageUsers", "Dashboard"),
        ("Reports", "Analytics"), ("Reports", "Dashboard"),
        ("Settings", "Dashboard"), ("Settings", "Logout"),
        ("Logout", "AdminLogin"),
        ("ErrorState", "Dashboard"), ("ErrorState", "AdminLogin"),
        ("LoadingState", "Dashboard"),
    ]
    requirements = (
        "Admin workflow: After login, admins typically check the dashboard first. "
        "Product management is more common than order management. "
        "Analytics reports are viewed less frequently than product updates. "
        "Error states are rare. "
        "Logout typically ends the session."
    )
    return {
        "name": "E-Commerce Admin Model",
        "states": states,
        "transitions": transitions,
        "requirements": requirements,
        "terminal_states": {"Logout"},
    }


def build_and_evaluate_model(
    scenario: Dict, use_closed_loop: bool = False
) -> Dict:
    print(f"\n=== {scenario['name']} ===")
    print(f"  States: {len(scenario['states'])}")
    print(f"  Transitions: {len(scenario['transitions'])}")

    print("[1/3] Constraint Extraction...")
    extractor = ConstraintExtractor()
    constraints = extractor.extract(scenario["requirements"])

    print("[2/3] Convex Optimization (Entropy-Maximizing)...")
    solver = ConstraintSolver(SolverConfig(max_entropy=True))
    mc = solver.solve(
        states=scenario["states"],
        structural_edges=set(scenario["transitions"]),
        constraints=constraints,
        terminal_states=scenario["terminal_states"],
    )
    mc.start_state = scenario["states"][0]
    print(f"  States: {mc.num_states}, Transitions: {mc.num_transitions}")
    print(f"  Row-stochastic: {mc.validate_row_stochastic()}")

    print("[3/3] Test Generation & Coverage...")
    generator = StatisticalTestGenerator(mc, max_path_length=500)
    suite = generator.generate_coverage_suite(target_coverage=1.0)
    stats = StatisticalTestGenerator.coverage_statistics(suite, mc)
    print(f"  Generated {len(suite)} sequences")
    print(f"  State coverage: {stats['state_coverage']:.2%}")
    print(f"  Transition coverage: {stats['transition_coverage']:.2%}")

    if use_closed_loop:
        print("\n  Closed-Loop Adaptation...")
        adapter = ClosedLoopAdapter(convergence_threshold=0.1)
        for i, tc in enumerate(suite[:20]):
            sample = TelemetrySample(
                path=tc.path,
                duration=float(len(tc.path)),
                outcome="pass" if len(tc.path) < 100 else "fail",
            )
            adapter.ingest_telemetry(sample)
        delta = adapter.detect_divergence(mc)
        if delta:
            mc = adapter.apply_delta(mc, delta)
            print(f"  Applied adaptation: {len(delta.probability_adjustments)} adjustments")

    result = {
        "name": scenario["name"],
        "num_states": mc.num_states,
        "num_transitions": mc.num_transitions,
        "coverage": stats,
        "generation_time_seconds": 0,
    }
    return result


def run_ecommerce_demo() -> Dict:
    results = {}
    user_scenario = build_ecommerce_user_model()
    admin_scenario = build_ecommerce_admin_model()
    results["user"] = build_and_evaluate_model(user_scenario)
    results["admin"] = build_and_evaluate_model(admin_scenario)
    return results


if __name__ == "__main__":
    run_ecommerce_demo()
