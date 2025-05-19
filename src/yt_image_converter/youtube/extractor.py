# extractor.py
from PIL import Image
from playwright.sync_api import sync_playwright
import time

def extract_clean_screenshot(video_id, executable_path, screenshot_path="base.png"):
    YT_BASE_URL = "https://www.youtube.com/watch?v="
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True, executable_path=executable_path)
            context = browser.new_context(
                viewport={'width': 375, 'height': 812},
                user_agent="Mozilla/5.0 (iPhone; CPU iPhone OS 13_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Mobile/15E148 Safari/604.1"
            )

            print("🌐 Navigating to YouTube video...")
            page = context.new_page()
            page.goto(YT_BASE_URL + video_id, timeout=15000)

            # Hide scrollbars & popups
            page.add_style_tag(content="""
                ::-webkit-scrollbar { display: none; }
                html, body { scrollbar-width: none; -ms-overflow-style: none; }
            """)

            print("⏳ Waiting for comments to load...")
            page.wait_for_selector("div.related-items-container", timeout=10000)

            # Find bounding box for where suggestions begin
            suggestion_element = page.query_selector("div.related-items-container")
            box = suggestion_element.bounding_box()

            if box is None:
                raise RuntimeError("❌ Could not get bounding box of related-items-container.")

            print(f"✂️ Screenshot will end at height: {int(box['y'])} px")

            # Remove overlays like unmute, enforcement messages, tooltips
            page.evaluate("""
                () => {
                    const selectors = [
                        '[aria-label="Tap to unmute"]',
                        'ytd-enforcement-message-view-model',
                        'tp-yt-paper-toast',
                        '.ytp-unmute-text',
                        '#movie_player .ytp-pause-overlay',
                        '#movie_player .ytp-popup',
                        '.ytp-tooltip'
                    ];
                    for (const selector of selectors) {
                        document.querySelectorAll(selector).forEach(el => el.remove());
                    }

                    const overlayParent = document.querySelector('#movie_player .ytp-unmute-button')?.parentElement;
                    if (overlayParent) overlayParent.remove();
                }
            """)

            time.sleep(1)

            video_box = page.query_selector("#player-container-id").bounding_box()

            # Take screenshot
            page.screenshot(path=screenshot_path, full_page=False)

            # Take screenshot up to before suggestions
            page.screenshot(
                path=screenshot_path,
                full_page=False,
                clip={"x": 0, "y": 50, "width": 375, "height": int(box["y"]) - 50}
            )

            print(f"✅ Screenshot saved: {screenshot_path}")

            browser.close()

            return video_box  # contains x, y, width, height

    except TimeoutError as te:
        print(f"❌ Timeout while waiting for elements: {te}")
        return None

    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return None

