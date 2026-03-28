from __future__ import annotations

import json
import sys
from dataclasses import dataclass

from playwright.sync_api import sync_playwright


THEME_URL = "http://127.0.0.1:9292/"


@dataclass
class CheckFailure:
    viewport: int
    message: str


def collect_footer_metrics(page) -> dict:
    return page.evaluate(
        r"""() => {
          const q = (selector) => document.querySelector(selector);
          const rect = (el) => {
            if (!el) return { width: 0, height: 0, x: 0, y: 0 };
            const r = el.getBoundingClientRect();
            return { width: r.width, height: r.height, x: r.x, y: r.y };
          };
          const style = (el, prop) => el ? getComputedStyle(el).getPropertyValue(prop) : '';

          const footer = q('.footer-section');
          const heading = q('.footer-section__heading') || q('.footer-section__eyebrow');
          const button = q('.footer-section__button');
          const socials = [...document.querySelectorAll('.footer-section__social')];
          const desktopLogo = q('.footer-section__brand-logo--desktop');
          const mobileLogo = q('.footer-section__brand-logo--mobile');

          return {
            footer: rect(footer),
            heading: {
              rect: rect(heading),
              fontSize: style(heading, 'font-size'),
              fontFamily: style(heading, 'font-family'),
              letterSpacing: style(heading, 'letter-spacing'),
              textTransform: style(heading, 'text-transform'),
            },
            button: rect(button),
            socials: {
              count: socials.length,
              rect: rect(q('.footer-section__socials')),
              tags: socials.map((el) => el.firstElementChild ? el.firstElementChild.tagName.toLowerCase() : null),
              imageSrcs: socials.map((el) => el.querySelector('img')?.getAttribute('src') || ''),
            },
            desktopLogo: {
              rect: rect(desktopLogo),
              naturalWidth: desktopLogo?.naturalWidth || 0,
              naturalHeight: desktopLogo?.naturalHeight || 0,
            },
            mobileLogo: {
              rect: rect(mobileLogo),
              naturalWidth: mobileLogo?.naturalWidth || 0,
              naturalHeight: mobileLogo?.naturalHeight || 0,
            },
          };
        }"""
    )


def check_viewport(viewport: int, metrics: dict) -> list[CheckFailure]:
    failures: list[CheckFailure] = []

    if viewport >= 1024:
      if metrics["socials"]["count"] < 4:
          failures.append(CheckFailure(viewport, f"expected 4 social icons, found {metrics['socials']['count']}"))
      if any(tag != "img" for tag in metrics["socials"]["tags"]):
          failures.append(CheckFailure(viewport, f"expected footer social icons to use image assets, got tags {metrics['socials']['tags']}"))
      if metrics["desktopLogo"]["rect"]["width"] < 250:
          failures.append(CheckFailure(viewport, f"expected visible desktop logo width >= 250px, got {metrics['desktopLogo']['rect']['width']:.1f}px"))
      if "rl-limo" not in metrics["heading"]["fontFamily"].lower() and not metrics["heading"]["fontFamily"].lower().endswith("serif"):
          failures.append(CheckFailure(viewport, f"expected serif newsletter heading, got {metrics['heading']['fontFamily']}"))
      if metrics["button"]["width"] > 180:
          failures.append(CheckFailure(viewport, f"expected desktop subscribe button width <= 180px, got {metrics['button']['width']:.1f}px"))

    if viewport == 768:
      if metrics["socials"]["count"] < 4:
          failures.append(CheckFailure(viewport, f"expected tablet footer social row, found {metrics['socials']['count']} icons"))
      if metrics["desktopLogo"]["rect"]["width"] < 250:
          failures.append(CheckFailure(viewport, f"expected tablet desktop wordmark to render, got {metrics['desktopLogo']['rect']['width']:.1f}px"))

    if viewport <= 390:
      if metrics["socials"]["count"] < 4:
          failures.append(CheckFailure(viewport, f"expected 4 mobile social icons, found {metrics['socials']['count']}"))
      if any(tag != "img" for tag in metrics["socials"]["tags"]):
          failures.append(CheckFailure(viewport, f"expected mobile social icons to use image assets, got tags {metrics['socials']['tags']}"))
      if not (56 <= metrics["mobileLogo"]["rect"]["width"] <= 66):
          failures.append(CheckFailure(viewport, f"expected mobile logo width between 56px and 66px, got {metrics['mobileLogo']['rect']['width']:.1f}px"))
      if metrics["button"]["width"] > 140:
          failures.append(CheckFailure(viewport, f"expected mobile subscribe button width <= 140px, got {metrics['button']['width']:.1f}px"))
      if "rl-limo" not in metrics["heading"]["fontFamily"].lower() and not metrics["heading"]["fontFamily"].lower().endswith("serif"):
          failures.append(CheckFailure(viewport, f"expected serif mobile newsletter heading, got {metrics['heading']['fontFamily']}"))

    return failures


def main() -> int:
    all_failures: list[CheckFailure] = []
    captured: dict[int, dict] = {}

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        for viewport in (1440, 768, 390):
            page = browser.new_page(viewport={"width": viewport, "height": 900 if viewport >= 768 else 844})
            page.goto(THEME_URL, wait_until="domcontentloaded", timeout=60000)
            page.wait_for_timeout(2500)
            page.locator(".footer-section").scroll_into_view_if_needed()
            page.wait_for_timeout(300)
            metrics = collect_footer_metrics(page)
            captured[viewport] = metrics
            all_failures.extend(check_viewport(viewport, metrics))
            page.close()
        browser.close()

    print(json.dumps(captured, indent=2))

    if all_failures:
        print("\nFooter checks failed:", file=sys.stderr)
        for failure in all_failures:
            print(f"- [{failure.viewport}px] {failure.message}", file=sys.stderr)
        return 1

    print("\nFooter checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
