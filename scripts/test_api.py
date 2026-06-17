#!/usr/bin/env python3
"""
StockPillar Skill API Smoke Test

Endpoints follow references/route-index.md. Reads STOCKPILLAR_API_KEY and
STOCKPILLAR_API_URL from the environment, with the production URL as fallback.
"""

import argparse
import json
import os
import sys
import time
from datetime import datetime, timedelta

import requests

try:
    from colorama import Fore, Style, init as _color_init
    _color_init(autoreset=True)
    _GREEN, _RED, _YELLOW, _CYAN, _RESET = Fore.GREEN, Fore.RED, Fore.YELLOW, Fore.CYAN, Style.RESET_ALL
except Exception:
    _GREEN = _RED = _YELLOW = _CYAN = _RESET = ""


DEFAULT_BASE_URL = "https://stockpillar.layercake18.com/api/skill/v1"


def _normalize_base_url(url: str) -> str:
    """Strip trailing slashes so endpoint joins do not produce //api/skill/v1/..."""
    return url.rstrip("/") if url else url


class StockPillarTester:
    def __init__(self, api_key: str = None, base_url: str = None, ts_code: str = "600519.SH"):
        self.api_key = api_key or os.environ.get("STOCKPILLAR_API_KEY")
        self.base_url = _normalize_base_url(
            base_url or os.environ.get("STOCKPILLAR_API_URL") or DEFAULT_BASE_URL
        )
        self.ts_code = ts_code
        self.headers = {"Content-Type": "application/json"}
        if self.api_key:
            self.headers["Authorization"] = f"Bearer {self.api_key}"
        self.results = []

    def _record(self, name: str, ok: bool, info: str = ""):
        flag = f"{_GREEN}PASS{_RESET}" if ok else f"{_RED}FAIL{_RESET}"
        print(f"[{flag}] {name}{(' - ' + info) if info else ''}")
        self.results.append({"test": name, "ok": ok, "info": info})

    def _get(self, name: str, path: str, params: dict = None, expect_data: bool = True):
        try:
            resp = requests.get(f"{self.base_url}{path}", headers=self.headers, params=params, timeout=15)
            if resp.status_code != 200:
                self._record(name, False, f"HTTP {resp.status_code}: {resp.text[:120]}")
                return None
            payload = resp.json()
            if expect_data and "code" in payload and payload.get("code") not in (0, 200):
                self._record(name, False, f"code={payload.get('code')} message={payload.get('message')}")
                return None
            preview = json.dumps(payload, ensure_ascii=False)[:160]
            self._record(name, True, preview)
            return payload
        except Exception as exc:
            self._record(name, False, repr(exc))
            return None

    def _post(self, name: str, path: str, body: dict):
        try:
            resp = requests.post(f"{self.base_url}{path}", headers=self.headers, json=body, timeout=20)
            if resp.status_code != 200:
                self._record(name, False, f"HTTP {resp.status_code}: {resp.text[:120]}")
                return None
            payload = resp.json()
            if "code" in payload and payload.get("code") not in (0, 200):
                self._record(name, False, f"code={payload.get('code')} message={payload.get('message')}")
                return None
            preview = json.dumps(payload, ensure_ascii=False)[:160]
            self._record(name, True, preview)
            return payload
        except Exception as exc:
            self._record(name, False, repr(exc))
            return None

    def health(self):
        return self._get("GET /health", "/health", expect_data=False)

    def stock_basic(self):
        return self._get(f"GET /stocks/{self.ts_code}", f"/stocks/{self.ts_code}")

    def stocks_batch(self):
        return self._get(
            "GET /stocks/batch",
            "/stocks/batch",
            params={"ts_codes": f"{self.ts_code},000001.SZ,000858.SZ"},
        )

    def realtime(self):
        return self._get(
            "GET /prices/realtime",
            "/prices/realtime",
            params={"ts_codes": self.ts_code},
        )

    def kline(self, days: int = 30):
        end_date = datetime.now().strftime("%Y%m%d")
        start_date = (datetime.now() - timedelta(days=days)).strftime("%Y%m%d")
        return self._get(
            f"GET /stocks/{self.ts_code}/prices/kline",
            f"/stocks/{self.ts_code}/prices/kline",
            params={"start_date": start_date, "end_date": end_date},
        )

    def minute(self):
        trade_date = datetime.now().strftime("%Y%m%d")
        return self._get(
            f"GET /stocks/{self.ts_code}/prices/minute",
            f"/stocks/{self.ts_code}/prices/minute",
            params={"trade_date": trade_date, "freq": "1m"},
        )

    def technical_indicators(self, days: int = 60):
        end_date = datetime.now().strftime("%Y%m%d")
        start_date = (datetime.now() - timedelta(days=days)).strftime("%Y%m%d")
        return self._get(
            f"GET /stocks/{self.ts_code}/technical/indicators",
            f"/stocks/{self.ts_code}/technical/indicators",
            params={
                "start_date": start_date,
                "end_date": end_date,
                "indicators": "MA,MACD,RSI,KDJ",
            },
        )

    def technical_alerts(self):
        return self._get(
            f"GET /stocks/{self.ts_code}/technical/alerts",
            f"/stocks/{self.ts_code}/technical/alerts",
        )

    def technical_radar(self):
        return self._get("GET /technical/radar", "/technical/radar")

    def stock_moneyflow(self, days: int = 10):
        end_date = datetime.now().strftime("%Y%m%d")
        start_date = (datetime.now() - timedelta(days=days)).strftime("%Y%m%d")
        return self._get(
            f"GET /stocks/{self.ts_code}/moneyflow",
            f"/stocks/{self.ts_code}/moneyflow",
            params={"start_date": start_date, "end_date": end_date},
        )

    def hsgt_overview(self):
        return self._get("GET /moneyflow/hsgt/overview", "/moneyflow/hsgt/overview")

    def financial(self):
        return self._get(
            f"GET /stocks/{self.ts_code}/financial",
            f"/stocks/{self.ts_code}/financial",
            params={"period": "latest"},
        )

    def toplist(self):
        return self._get("GET /toplist", "/toplist")

    def top20_daily(self):
        return self._get(
            "GET /top20/daily",
            "/top20/daily",
            params={"previous_trade_date": "true", "type": "score_top20"},
        )

    def macro(self, days: int = 30):
        end_date = datetime.now().strftime("%Y%m%d")
        start_date = (datetime.now() - timedelta(days=days)).strftime("%Y%m%d")
        return self._get(
            "GET /macro", "/macro", params={"start_date": start_date, "end_date": end_date}
        )

    def market_summary(self):
        return self._get("GET /market/summary", "/market/summary")

    def market_sentiment_pulse(self):
        return self._get("GET /market/sentiment_pulse", "/market/sentiment_pulse")

    def industries_status(self):
        return self._get("GET /industries/status", "/industries/status")

    def stock_screening(self):
        body = {
            "filters": {
                "pe": {"lt": 20},
                "roe": {"gt": 15},
            },
            "sort_by": "roe",
            "sort_order": "desc",
            "limit": 5,
        }
        return self._post("POST /screen/stocks", "/screen/stocks", body=body)

    def positions(self):
        return self._get("GET /positions", "/positions", params={"status": "holding"})

    def positions_summary(self):
        return self._get("GET /positions/summary", "/positions/summary")

    def run_all(self):
        suite = [
            self.stock_basic,
            self.stocks_batch,
            self.realtime,
            self.minute,
            self.kline,
            self.technical_indicators,
            self.technical_alerts,
            self.technical_radar,
            self.stock_moneyflow,
            self.hsgt_overview,
            self.financial,
            self.toplist,
            self.top20_daily,
            self.macro,
            self.market_summary,
            self.market_sentiment_pulse,
            self.industries_status,
            self.stock_screening,
            self.positions,
            self.positions_summary,
        ]
        for fn in suite:
            fn()
            time.sleep(0.3)

    def summary(self):
        total = len(self.results)
        passed = sum(1 for r in self.results if r["ok"])
        failed = total - passed
        print(f"\n{_CYAN}== Summary =={_RESET}")
        print(f"Total: {total}  Pass: {_GREEN}{passed}{_RESET}  Fail: {_RED}{failed}{_RESET}")
        if failed:
            print(f"\n{_YELLOW}Failed cases:{_RESET}")
            for r in self.results:
                if not r["ok"]:
                    print(f"  - {r['test']}: {r['info']}")
        return failed == 0


def main():
    parser = argparse.ArgumentParser(description="StockPillar Skill API smoke test")
    parser.add_argument("--key", help="API key (or set STOCKPILLAR_API_KEY env)")
    parser.add_argument("--url", help="API base URL (or set STOCKPILLAR_API_URL env)")
    parser.add_argument("--ts-code", default="600519.SH", help="Stock code used in single-stock tests")
    parser.add_argument(
        "--only",
        help="Run a single endpoint family. Choices: health, basic, batch, realtime, kline, "
             "minute, indicators, alerts, radar, moneyflow, hsgt, financial, toplist, top20, macro, "
             "market_summary, market_pulse, industries, screen, positions",
    )
    args = parser.parse_args()

    tester = StockPillarTester(api_key=args.key, base_url=args.url, ts_code=args.ts_code)

    print(f"{_CYAN}StockPillar Skill API smoke test{_RESET}")
    print(f"Base URL: {tester.base_url}")
    if not tester.api_key:
        print(f"{_YELLOW}WARNING: STOCKPILLAR_API_KEY missing. Auth-protected endpoints will fail.{_RESET}")

    if not tester.health():
        print(f"{_RED}Health check failed; aborting.{_RESET}")
        sys.exit(1)

    if args.only:
        dispatch = {
            "health": tester.health,
            "basic": tester.stock_basic,
            "batch": tester.stocks_batch,
            "realtime": tester.realtime,
            "minute": tester.minute,
            "kline": tester.kline,
            "indicators": tester.technical_indicators,
            "alerts": tester.technical_alerts,
            "radar": tester.technical_radar,
            "moneyflow": tester.stock_moneyflow,
            "hsgt": tester.hsgt_overview,
            "financial": tester.financial,
            "toplist": tester.toplist,
            "top20": tester.top20_daily,
            "macro": tester.macro,
            "market_summary": tester.market_summary,
            "market_pulse": tester.market_sentiment_pulse,
            "industries": tester.industries_status,
            "screen": tester.stock_screening,
            "positions": tester.positions,
        }
        fn = dispatch.get(args.only)
        if not fn:
            print(f"{_RED}Unknown --only value: {args.only}{_RESET}")
            sys.exit(2)
        fn()
    else:
        tester.run_all()

    ok = tester.summary()
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
