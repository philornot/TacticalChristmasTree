import subprocess
import tempfile

import requests
from packaging import version

from logger import NiceLogger
from settings import PROJECT_VERSION, GITHUB_REPO

# Initialize logger
logger = NiceLogger(__name__).get_logger()


def download_update(download_url):
    """Download update installer from GitHub."""
    try:
        logger.info("Downloading update", extra={'metadata': {'url': download_url}})
        response = requests.get(download_url, stream=True)
        response.raise_for_status()

        # Create temp directory for the download
        with tempfile.NamedTemporaryFile(suffix='.exe', delete=False) as temp_file:
            logger.debug(f"Saving installer to: {temp_file.name}")
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    temp_file.write(chunk)
            return temp_file.name
    except Exception as e:
        logger.error(
            "Failed to download update",
            extra={'metadata': {'error': str(e)}},
            exc_info=True
        )
        return None


def install_update(installer_path):
    """Install the update silently."""
    try:
        logger.info("Installing update", extra={'metadata': {'installer': installer_path}})

        # Create startupinfo to hide console window
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        startupinfo.wShowWindow = subprocess.SW_HIDE

        # Start the installer directly without batch file
        subprocess.Popen(
            [installer_path, '/VERYSILENT', '/SUPPRESSMSGBOXES', '/NORESTART'],
            creationflags=subprocess.CREATE_NO_WINDOW | subprocess.DETACHED_PROCESS,
            close_fds=True,
            startupinfo=startupinfo
        )
        return True
    except Exception as e:
        logger.error(
            "Failed to install update",
            extra={'metadata': {'error': str(e)}},
            exc_info=True
        )
        return False


def check_for_updates():
    """Check for new versions and prepare silent update if available."""
    try:
        logger.info("Checking for updates...", extra={
            'metadata': {
                'current_version': PROJECT_VERSION,
                'repo': GITHUB_REPO
            }
        })

        # Extract owner and repo from GitHub URL
        _, _, _, owner, repo = GITHUB_REPO.rstrip('/').split('/')
        api_url = f"https://api.github.com/repos/{owner}/{repo}/releases"

        # Get releases from GitHub
        logger.debug(f"Fetching releases from {api_url}")
        response = requests.get(api_url)
        response.raise_for_status()

        releases = response.json()
        logger.debug(f'Found {len(releases)} releases')
        stable_releases = [r for r in releases if not r['prerelease']]

        if not stable_releases:
            logger.warning("No stable releases found")
            return None

        latest_release = stable_releases[0]
        latest_version = latest_release['tag_name'].lstrip('v')

        # Compare versions
        logger.debug(f"Comparing versions: current={PROJECT_VERSION}, latest={latest_version}")

        if version.parse(latest_version) > version.parse(PROJECT_VERSION):
            logger.info(f"New version {latest_version} available!")

            # Find the installer asset
            installer_asset = next(
                (asset for asset in latest_release['assets']
                 if asset['name'].endswith('_Setup.exe')),
                None
            )

            if installer_asset:
                # Download the installer
                installer_path = download_update(installer_asset['browser_download_url'])
                if installer_path:
                    logger.info("Update downloaded successfully")
                    return {
                        'installer_path': installer_path,
                        'version': latest_version,
                        'release_url': latest_release['html_url']
                    }
            else:
                logger.warning("No installer found in release assets")
        else:
            logger.info("Using the latest version", extra={
                'metadata': {'version': PROJECT_VERSION}
            })

        return None

    except Exception as e:
        logger.error(
            "Failed to check for updates",
            extra={'metadata': {'error': str(e)}},
            exc_info=True
        )
        return None
