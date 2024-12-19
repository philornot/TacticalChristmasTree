import requests
from logger import NiceLogger
from packaging import version

from settings import PROJECT_VERSION, GITHUB_REPO

# Initialize logger
logger = NiceLogger(__name__).get_logger()


def check_for_updates():
    """Check for new versions of the application on GitHub."""
    try:
        logger.info("Checking for updates...", extra={
            'metadata': {
                'current_version': PROJECT_VERSION,
                'repo': GITHUB_REPO
            }
        })

        # Extract owner and repo from GitHub URL
        _, _, _, owner, repo = GITHUB_REPO.rstrip('/').split('/')

        # GitHub API endpoint for releases
        api_url = f"https://api.github.com/repos/{owner}/{repo}/releases"

        # Get releases from GitHub
        logger.debug(f"Fetching releases from {api_url}")
        response = requests.get(api_url)
        response.raise_for_status()

        releases = response.json()
        stable_releases = [r for r in releases if not r['prerelease']]

        if not stable_releases:
            logger.warning("No stable releases found")
            return

        latest_release = stable_releases[0]
        latest_version = latest_release['tag_name'].lstrip('v')

        # Compare versions
        logger.debug(f"Comparing versions: current={PROJECT_VERSION}, latest={latest_version}")

        if version.parse(latest_version) > version.parse(PROJECT_VERSION):
            logger.info(
                f"New version {latest_version} is available!",
                extra={
                    'metadata': {
                        'current_version': PROJECT_VERSION,
                        'latest_version': latest_version,
                        'download_url': f"{GITHUB_REPO}/releases/latest"
                    }
                }
            )
            print(f"New version {latest_version} is available! (Current: {PROJECT_VERSION})")
            print(f"Download it from: {GITHUB_REPO}/releases/latest")
        else:
            logger.info("Using the latest version", extra={
                'metadata': {'version': PROJECT_VERSION}
            })
            print("You are using the latest version")

    except Exception as e:
        logger.error(
            "Failed to check for updates",
            extra={'metadata': {'error': str(e)}},
            exc_info=True
        )
        print(f"Failed to check for updates: {e}")


if __name__ == "__main__":
    check_for_updates()
