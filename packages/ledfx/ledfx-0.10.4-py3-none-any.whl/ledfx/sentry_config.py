import sentry_sdk
from sentry_sdk.integrations.aiohttp import AioHttpIntegration

from ledfx.consts import PROJECT_VERSION

# Place your key between the quotes if you have a sentry.io account and wish to use it.
# Otherwise the LedFx sentry key is inserted here during deployment.


sentry_dsn = "https://691086dc41fa4218860be6ed4c888145@o482797.ingest.sentry.io/5533553"
if (
    sentry_dsn
    == "https://691086dc41fa4218860be6ed4c888145@o482797.ingest.sentry.io/5533553"
):
    sentry_sdk.init(
        sentry_dsn,
        traces_sample_rate=1,
        integrations=[AioHttpIntegration()],
        release=f"ledfx@{PROJECT_VERSION}",
    )
