"""Unit tests for Ryde Council API parsing helpers."""
from __future__ import annotations

from datetime import date
import json
from pathlib import Path

from ryde_waste_collection.api import (
    API_HEADERS,
    calculate_days_until,
    extract_date,
    parse_address_matches,
    parse_collection_date,
    parse_waste_schedule,
)
from ryde_waste_collection.const import (
    WASTE_TYPE_GARDEN,
    WASTE_TYPE_GENERAL,
    WASTE_TYPE_RECYCLING,
)

FIXTURES = Path(__file__).parent / "fixtures"


def test_api_headers_override_home_assistant_user_agent() -> None:
    """Council WAF blocks Home Assistant and generic browser user agents."""
    user_agent = API_HEADERS["User-Agent"]
    assert "Home Assistant" not in user_agent
    assert "HomeAssistant" not in user_agent
    assert "Mozilla" not in user_agent
    assert API_HEADERS["Accept"] == "application/json"


def test_extract_dates_from_council_html() -> None:
    html = (FIXTURES / "waste_response.html").read_text()
    assert extract_date(html, WASTE_TYPE_GENERAL) == "Tue 25/8/2026"
    assert extract_date(html, WASTE_TYPE_GARDEN) == "Tue 25/8/2026"
    assert extract_date(html, WASTE_TYPE_RECYCLING) == "Tue 1/9/2026"


def test_extract_date_missing_type() -> None:
    assert extract_date("<h3>General Waste</h3>", WASTE_TYPE_RECYCLING) is None


def test_parse_collection_date_variants() -> None:
    assert parse_collection_date("Tue 25/8/2026") == date(2026, 8, 25)
    assert parse_collection_date("Tue 01/09/2026") == date(2026, 9, 1)
    assert parse_collection_date("not a date") is None
    assert parse_collection_date("") is None


def test_calculate_days_until_is_explicit() -> None:
    today = date(2026, 8, 24)
    assert calculate_days_until(date(2026, 8, 24), today) == 0
    assert calculate_days_until(date(2026, 8, 25), today) == 1
    assert calculate_days_until(date(2026, 9, 1), today) == 8


def test_parse_waste_schedule_does_not_treat_parse_failure_as_today() -> None:
    html = '<h3>General Waste</h3><div class="next-service">soon</div>'
    schedule = parse_waste_schedule(html, date(2026, 8, 24))
    general = schedule[WASTE_TYPE_GENERAL]
    assert general.date_text == "soon"
    assert general.collection_date is None
    assert general.days_until is None
    assert schedule[WASTE_TYPE_RECYCLING].date_text is None


def test_parse_waste_schedule_fixture() -> None:
    html = (FIXTURES / "waste_response.html").read_text()
    schedule = parse_waste_schedule(html, date(2026, 8, 24))
    assert schedule[WASTE_TYPE_GENERAL].days_until == 1
    assert schedule[WASTE_TYPE_GARDEN].collection_date == date(2026, 8, 25)
    assert schedule[WASTE_TYPE_RECYCLING].days_until == 8


def test_parse_single_address_match() -> None:
    payload = json.loads((FIXTURES / "search_single.json").read_text())
    matches = parse_address_matches(payload)
    assert len(matches) == 1
    assert matches[0].address == "1028/109-129 Blaxland Road, Ryde 2112"
    assert matches[0].geolocation_id == "b148f7d7-e435-4b28-8970-b89af8be2ba0"


def test_parse_multiple_address_matches_preserves_all() -> None:
    payload = json.loads((FIXTURES / "search_multiple.json").read_text())
    matches = parse_address_matches(payload)
    assert [match.address for match in matches] == [
        "286 Blaxland Road, Ryde 2112",
        "128 Blaxland Road, Ryde 2112",
        "150 Blaxland Road, Ryde 2112",
    ]


def test_parse_address_matches_skips_incomplete_items() -> None:
    matches = parse_address_matches({"Items": [{"Id": "only-id"}, {"AddressSingleLine": "no-id"}]})
    assert matches == []
