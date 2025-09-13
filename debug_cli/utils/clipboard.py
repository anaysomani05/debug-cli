"""Clipboard management utilities."""

import platform
import subprocess  # nosec B404
from typing import Optional


class ClipboardManager:
    """Handles clipboard operations across different platforms."""

    def __init__(self) -> None:
        self.system = platform.system().lower()

    def copy_to_clipboard(self, text: str) -> bool:
        """
        Copy text to clipboard.

        Args:
            text: Text to copy to clipboard

        Returns:
            True if successful, False otherwise
        """
        try:
            if self.system == "darwin":  # macOS
                return self._copy_macos(text)
            elif self.system == "linux":
                return self._copy_linux(text)
            elif self.system == "windows":
                return self._copy_windows(text)
            else:
                return False
        except Exception:
            return False

    def _copy_macos(self, text: str) -> bool:
        """Copy text to clipboard on macOS."""
        try:
            process = subprocess.Popen(  # nosec B603, B607
                ["pbcopy"],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            process.communicate(input=text.encode("utf-8"))
            return process.returncode == 0
        except Exception:
            return False

    def _copy_linux(self, text: str) -> bool:
        """Copy text to clipboard on Linux."""
        # Try xclip first
        try:
            process = subprocess.Popen(  # nosec B603, B607
                ["xclip", "-selection", "clipboard"],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            process.communicate(input=text.encode("utf-8"))
            if process.returncode == 0:
                return True
        except Exception:  # nosec B110
            pass

        # Try xsel as fallback
        try:
            process = subprocess.Popen(  # nosec B603, B607
                ["xsel", "--clipboard", "--input"],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            process.communicate(input=text.encode("utf-8"))
            return process.returncode == 0
        except Exception:
            return False

    def _copy_windows(self, text: str) -> bool:
        """Copy text to clipboard on Windows."""
        try:
            import pyperclip

            pyperclip.copy(text)
            return True
        except ImportError:
            # Fallback to PowerShell
            try:
                process = subprocess.Popen(  # nosec B603, B607
                    ["powershell", "-command", f'Set-Clipboard -Value "{text}"'],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                )
                process.communicate()
                return process.returncode == 0
            except Exception:
                return False
        except Exception:
            return False

    def get_clipboard_content(self) -> Optional[str]:
        """
        Get content from clipboard.

        Returns:
            Clipboard content or None if failed
        """
        try:
            if self.system == "darwin":  # macOS
                return self._get_macos()
            elif self.system == "linux":
                return self._get_linux()
            elif self.system == "windows":
                return self._get_windows()
            else:
                return None
        except Exception:
            return None

    def _get_macos(self) -> Optional[str]:
        """Get clipboard content on macOS."""
        try:
            result = subprocess.run(  # nosec B603, B607
                ["pbpaste"], capture_output=True, text=True, timeout=5
            )
            return result.stdout if result.returncode == 0 else None
        except Exception:
            return None

    def _get_linux(self) -> Optional[str]:
        """Get clipboard content on Linux."""
        # Try xclip first
        try:
            result = subprocess.run(  # nosec B603, B607
                ["xclip", "-selection", "clipboard", "-o"],
                capture_output=True,
                text=True,
                timeout=5,
            )
            if result.returncode == 0:
                return result.stdout
        except Exception:  # nosec B110
            pass

        # Try xsel as fallback
        try:
            result = subprocess.run(  # nosec B603, B607
                ["xsel", "--clipboard", "--output"],
                capture_output=True,
                text=True,
                timeout=5,
            )
            return result.stdout if result.returncode == 0 else None
        except Exception:
            return None

    def _get_windows(self) -> Optional[str]:
        """Get clipboard content on Windows."""
        try:
            import pyperclip

            return str(pyperclip.paste())
        except ImportError:
            # Fallback to PowerShell
            try:
                result = subprocess.run(  # nosec B603, B607
                    ["powershell", "-command", "Get-Clipboard"],
                    capture_output=True,
                    text=True,
                    timeout=5,
                )
                return result.stdout if result.returncode == 0 else None
            except Exception:
                return None
        except Exception:
            return None

    def is_clipboard_available(self) -> bool:
        """
        Check if clipboard functionality is available.

        Returns:
            True if clipboard is available, False otherwise
        """
        try:
            if self.system == "darwin":
                # Check if pbcopy is available
                subprocess.run(
                    ["which", "pbcopy"], check=True, capture_output=True
                )  # nosec B603, B607
                return True
            elif self.system == "linux":
                # Check if xclip or xsel is available
                try:
                    subprocess.run(
                        ["which", "xclip"], check=True, capture_output=True
                    )  # nosec B603, B607
                    return True
                except subprocess.CalledProcessError:
                    try:
                        subprocess.run(  # nosec B603, B607
                            ["which", "xsel"], check=True, capture_output=True
                        )
                        return True
                    except subprocess.CalledProcessError:
                        return False
            elif self.system == "windows":
                # Check if pyperclip is available or PowerShell works
                try:
                    import pyperclip  # noqa: F401

                    return True
                except ImportError:
                    try:
                        subprocess.run(  # nosec B603, B607
                            ["powershell", "-command", "Get-Clipboard"],
                            check=True,
                            capture_output=True,
                            timeout=5,
                        )
                        return True
                    except Exception:
                        return False
            else:
                return False
        except Exception:
            return False
