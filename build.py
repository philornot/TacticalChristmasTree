import os
import shutil
import subprocess
from pathlib import Path

from logger import NiceLogger
from settings import (
    PROJECT_NAME, PROJECT_VERSION, AUTHOR, DIST_DIR, TEMP_DIR, BUILD_DIR, MAIN_SCRIPT, ICON_PATH, ROOT_DIR, GITHUB_REPO,
    ICON_PNG_PATH
)

# Initialize logger
logger = NiceLogger(__name__).get_logger()


def get_versioned_name(with_setup=False):
    """Generate versioned filename."""
    base_name = f"{PROJECT_NAME}-v{PROJECT_VERSION}"
    return f"{base_name}_Setup.exe" if with_setup else f"{base_name}.exe"


def check_icons():
    """Check if icon files exist and log their status."""
    icons_status = {
        'ico': ICON_PATH.exists(),
        'png': ICON_PNG_PATH.exists()
    }

    if all(icons_status.values()):
        logger.info("All icon files found", extra={
            'metadata': {
                'ico_path': str(ICON_PATH),
                'ico_size': ICON_PATH.stat().st_size,
                'png_path': str(ICON_PNG_PATH),
                'png_size': ICON_PNG_PATH.stat().st_size
            }
        })
        return True
    else:
        logger.warning("Some icon files missing", extra={
            'metadata': {
                'status': icons_status,
                'ico_path': str(ICON_PATH),
                'png_path': str(ICON_PNG_PATH)
            }
        })
        return False


def create_spec_file():
    """Create PyInstaller spec file."""
    logger.debug("Creating spec file")

    # Check icons status
    icons_exist = check_icons()
    if icons_exist:
        logger.debug("Icons will be included in the build")
    else:
        logger.warning("Icons will not be included in the build")

    spec_content = f'''# -*- mode: python ; coding: utf-8 -*-
import os
import sv_ttk

block_cipher = None

# Get sv_ttk package location
sv_ttk_path = os.path.dirname(sv_ttk.__file__)

a = Analysis(
    [r'{MAIN_SCRIPT}'],
    pathex=[],
    binaries=[],
    datas=[
        # Include sv_ttk theme files
        (sv_ttk_path, 'sv_ttk'),
        # Include icon files
        (r'{ICON_PATH}', '.'),
        (r'{ICON_PNG_PATH}', '.'),
    ] if os.path.exists(r'{ICON_PATH}') and os.path.exists(r'{ICON_PNG_PATH}') else [(sv_ttk_path, 'sv_ttk')],
    hiddenimports=['sv_ttk'],
    hookspath=[],
    hooksconfig={{}},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='{PROJECT_NAME}',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=r'{ICON_PATH}' if os.path.exists(r'{ICON_PATH}') else None,
)
'''
    return spec_content


def create_inno_setup_script():
    """Create Inno Setup script."""
    logger.debug("Creating Inno Setup script")
    iss_content = f'''#define MyAppName "{PROJECT_NAME}"
#define MyAppVersion "{PROJECT_VERSION}"
#define MyAppPublisher "{AUTHOR}"
#define MyAppURL "{GITHUB_REPO}"
#define MyAppExeName "{get_versioned_name()}"

[Setup]
AppId={{{{{PROJECT_NAME}}}}}
AppName={{#MyAppName}}
AppVersion={{#MyAppVersion}}
AppPublisher={{#MyAppPublisher}}
AppPublisherURL={{#MyAppURL}}
AppSupportURL={{#MyAppURL}}
AppUpdatesURL={{#MyAppURL}}
DefaultDirName={{userappdata}}\\{{#MyAppName}}
DisableProgramGroupPage=yes
LicenseFile=LICENSE
OutputDir={DIST_DIR}
OutputBaseFilename={PROJECT_NAME}-v{PROJECT_VERSION}_Setup
Compression=lzma
SolidCompression=yes
WizardStyle=modern
PrivilegesRequired=lowest

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"
Name: "polish"; MessagesFile: "compiler:Languages\\Polish.isl"

[Tasks]
Name: "desktopicon"; Description: "{{cm:CreateDesktopIcon}}"; GroupDescription: "{{cm:AdditionalIcons}}"

[Files]
Source: "{os.path.join(DIST_DIR, get_versioned_name())}"; DestDir: "{{app}}"; DestName: "{{#MyAppExeName}}"; Flags: ignoreversion

[Icons]
Name: "{{autoprograms}}\\{{#MyAppName}}"; Filename: "{{app}}\\{{#MyAppExeName}}"
Name: "{{autodesktop}}\\{{#MyAppName}}"; Filename: "{{app}}\\{{#MyAppExeName}}"; Tasks: desktopicon

[Run]
Filename: "{{app}}\\{{#MyAppExeName}}"; Description: "{{cm:LaunchProgram,{{#StringChange(MyAppName, '&', '&&')}}}}"; Flags: nowait postinstall skipifsilent shellexec
'''
    return iss_content


def ensure_directories():
    """Create necessary directories if they don't exist."""
    logger.debug("Ensuring directories exist")
    for directory in [DIST_DIR, TEMP_DIR, BUILD_DIR]:
        Path(directory).mkdir(parents=True, exist_ok=True)


def build_executable():
    """Build the executable using PyInstaller."""
    try:
        logger.info("Building executable", extra={
            'metadata': {
                'version': PROJECT_VERSION,
                'main_script': str(MAIN_SCRIPT)
            }
        })

        # Create spec file
        spec_path = os.path.join(TEMP_DIR, f"{PROJECT_NAME}.spec")
        with open(spec_path, 'w', encoding='utf-8') as f:
            f.write(create_spec_file())

        logger.debug(f"Using spec file: {spec_path}")

        # Run PyInstaller
        result = subprocess.run(
            ['pyinstaller', spec_path, '--distpath', str(DIST_DIR), '--workpath', str(BUILD_DIR)],
            check=True,
            capture_output=True,
            text=True
        )

        logger.debug("PyInstaller output: " + result.stdout)
        if result.stderr:
            logger.warning("PyInstaller warnings/errors: " + result.stderr)

        # Rename exe file
        exe_file = DIST_DIR / get_versioned_name()
        logger.debug(f"Renaming executable to: {exe_file}")

        # Move the file with proper error handling
        original_exe = os.path.join(DIST_DIR, f"{PROJECT_NAME}.exe")
        if os.path.exists(original_exe):
            logger.debug(f"Moving {original_exe} to {exe_file}")
            os.replace(original_exe, exe_file)
        else:
            logger.error(f"Original exe not found: {original_exe}")
            return False

        return True
    except subprocess.CalledProcessError as e:
        logger.error(
            "Failed to build executable",
            extra={'metadata': {
                'error': str(e),
                'stdout': e.stdout,
                'stderr': e.stderr
            }},
            exc_info=True
        )
        return False
    except Exception as e:
        logger.error(
            "Unexpected error during build",
            extra={'metadata': {'error': str(e)}},
            exc_info=True
        )
        return False


def create_installer():
    """Create the installer using Inno Setup."""
    try:
        logger.info("Creating installer")

        # Copy LICENSE file to temp directory
        license_path = ROOT_DIR / "LICENSE"
        temp_license_path = TEMP_DIR / "LICENSE"
        logger.debug(f"Copying LICENSE to {temp_license_path}")
        shutil.copy2(license_path, temp_license_path)

        # Create Inno Setup script
        iss_path = TEMP_DIR / f"{PROJECT_NAME}.iss"
        with open(iss_path, 'w', encoding='utf-8') as f:
            f.write(create_inno_setup_script())

        # Run Inno Setup Compiler
        iscc_path = Path(r"C:\Program Files (x86)\Inno Setup 6\ISCC.exe")
        if iscc_path.exists():
            logger.debug(f"Running Inno Setup: {iscc_path}")
            result = subprocess.run(
                [str(iscc_path), str(iss_path)],
                check=True,
                capture_output=True,
                text=True
            )

            logger.debug("Inno Setup output: " + result.stdout)
            if result.stderr:
                logger.warning("Inno Setup warnings/errors: " + result.stderr)

            return True
        else:
            logger.error("Inno Setup not found", extra={
                'metadata': {'path': str(iscc_path)}
            })
            print("Inno Setup not found. Please install it first.")
            return False
    except subprocess.CalledProcessError as e:
        logger.error(
            "Failed to create installer",
            extra={'metadata': {
                'error': str(e),
                'stdout': e.stdout,
                'stderr': e.stderr
            }},
            exc_info=True
        )
        return False
    except Exception as e:
        logger.error(
            "Unexpected error during installer creation",
            extra={'metadata': {'error': str(e)}},
            exc_info=True
        )
        return False


def cleanup_dist():
    """Clean up the dist directory, keeping only the final exe files."""
    try:
        logger.info("Cleaning up dist directory")
        exe_name = get_versioned_name()
        setup_name = get_versioned_name(with_setup=True)
        keep_files = {exe_name, setup_name}

        for item in os.listdir(DIST_DIR):
            item_path = os.path.join(DIST_DIR, item)
            if item not in keep_files:
                logger.debug(f"Removing: {item_path}")
                if os.path.isfile(item_path):
                    os.remove(item_path)
                elif os.path.isdir(item_path):
                    shutil.rmtree(item_path)

        logger.debug(f"Kept files: {', '.join(keep_files)}")
    except Exception as e:
        logger.error(
            "Error during dist cleanup",
            extra={'metadata': {'error': str(e)}},
            exc_info=True
        )


def cleanup():
    """Clean up temporary files and directories."""
    try:
        logger.info("Cleaning up temporary files")
        shutil.rmtree(TEMP_DIR)
        shutil.rmtree(BUILD_DIR)
    except Exception as e:
        logger.error(
            "Failed to cleanup temporary files",
            extra={'metadata': {'error': str(e)}},
            exc_info=True
        )


def main():
    """Main build process."""
    logger.info(f"Starting build process for {PROJECT_NAME} v{PROJECT_VERSION}")

    ensure_directories()

    if build_executable():
        logger.info("Successfully built executable")
        if create_installer():
            logger.info("Successfully created installer")
        else:
            logger.error("Failed to create installer")
    else:
        logger.error("Failed to build executable")

    # Clean up dist directory before cleaning temp files
    cleanup_dist()
    cleanup()
    logger.info("Build process completed")


if __name__ == "__main__":
    main()
