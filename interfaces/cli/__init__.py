"""
CLI (Command Line Interface) module for terminal-based interaction.

This module provides terminal input/output interfaces that implement
the base InputInterface and OutputInterface classes.
"""

from .terminal import TerminalInput, TerminalOutput, TerminalInterface

__all__ = [
    'TerminalInput',
    'TerminalOutput', 
    'TerminalInterface'
]
