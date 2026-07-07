from app.benchmarks import get_benchmarks


def status(
    value: float,
    good_threshold: float,
    ok_threshold: float,
    higher_is_better: bool,
) -> str:
    if higher_is_better:
        if value >= good_threshold:
            return "good"
        if value >= ok_threshold:
            return "warn"
        return "bad"

    if value <= good_threshold:
        return "good"
    if value <= ok_threshold:
        return "warn"
    return "bad"
