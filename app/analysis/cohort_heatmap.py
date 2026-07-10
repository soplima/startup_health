from collections import defaultdict

from app import models


def build_heatmap(db, company_id):
    customers = (
        db.query(models.Customer).filter(models.Customer.company_id == company_id).all()
    )

    cohorts = defaultdict(list)

    for customer in customers:
        cohorts[customer.signup_month].append(customer)

    result = []

    for signup_month, customers in sorted(cohorts.items()):
        cohort_size = len(customers)

        months = defaultdict(int)

        max_offset = 0

        for customer in customers:
            for snapshot in sorted(customer.snapshots, key=lambda x: x.month):
                offset = (
                    (snapshot.month.year - signup_month.year) * 12
                    + snapshot.month.month
                    - signup_month.month
                )

                if offset < 0:
                    continue

                max_offset = max(max_offset, offset)

                if snapshot.active:
                    months[offset] += 1

        cells = []

        for offset in range(max_offset + 1):
            active = months[offset]

            retention = active / cohort_size * 100 if cohort_size else 0

            cells.append(
                {
                    "month_offset": offset,
                    "retention": round(retention, 1),
                }
            )

        result.append(
            {
                "cohort_month": signup_month,
                "cohort_size": cohort_size,
                "cells": cells,
            }
        )

    return result
