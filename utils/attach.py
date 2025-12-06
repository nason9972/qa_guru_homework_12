import allure
from allure_commons.types import AttachmentType


def add_screenshot(driver):
    png = driver.get_screenshot_as_png()
    allure.attach(
        png,
        name="screenshot",
        attachment_type=AttachmentType.PNG,
        extension=".png"
    )


def add_logs(driver):
    try:
        logs = driver.get_log('browser')
        text = "\n".join([f"{l['level']}: {l['message']}" for l in logs])
        allure.attach(text, "browser_logs", AttachmentType.TEXT, ".log")
    except Exception:
        pass


def add_html(driver):
    html = driver.page_source
    allure.attach(html, "page_source", AttachmentType.HTML, ".html")


def add_video(driver):
    video_url = f"https://selenoid.autotests.cloud/video/{driver.session_id}.mp4"

    html = (
        "<html><body><video width='100%' height='100%' controls autoplay>"
        f"<source src='{video_url}' type='video/mp4'></video></body></html>"
    )

    allure.attach(html, f"video_{driver.session_id}", AttachmentType.HTML, ".html")