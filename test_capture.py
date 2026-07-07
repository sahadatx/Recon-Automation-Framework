from modules.screenshot.exporter import (
    save_screenshot_results,
    export_screenshot_json,
    show_summary,
)

sample = {

    "google.com": {

        "url": "https://google.com",

        "screenshot": "output/screenshots/google.com.png",

        "captured": True,

        "timestamp": "2026-07-06T11:30:00Z",

        "width": 1440,

        "height": 900,

    },

    "github.com": {

        "url": "https://github.com",

        "screenshot": "output/screenshots/github.com.png",

        "captured": True,

        "timestamp": "2026-07-06T11:31:00Z",

        "width": 1440,

        "height": 900,

    },

}

save_screenshot_results(sample)

export_screenshot_json(sample)

show_summary(
    sample,
    [],
    1.25,
)
