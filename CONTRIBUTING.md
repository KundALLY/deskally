# Contributing

[English](CONTRIBUTING.md) · [Türkçe](CONTRIBUTING.tr.md)

When reporting a bug, include your distribution, desktop environment, X11 or Wayland session, reproduction steps, and relevant lines from `deskally logs`. Remove personal information such as public IP addresses before posting.

For code contributions:

1. Fork the repository and create a focused branch.
2. Keep the change small and limited to one purpose.
3. Add all new user-facing text in both Turkish and English in `deskally/i18n.py`.
4. Run `python3 -m unittest discover -s tests -v`.
5. Open a pull request explaining the purpose and validation steps.
