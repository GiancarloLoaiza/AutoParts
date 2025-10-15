#!/usr/bin/env python3
import argparse, sys, subprocess, os, shutil

def main():
    parser = argparse.ArgumentParser(description="Run pytest with coverage and show failing tests.")
    parser.add_argument("--cov-target", default=".", help="Path/package to measure coverage against (default: current dir).")
    parser.add_argument("--junitxml", default="test-results.xml", help="JUnit XML output file name.")
    parser.add_argument("--cov-xml", default="coverage.xml", help="Coverage XML output file name.")
    args = parser.parse_args()

    # Ensure pytest is installed
    try:
        import pytest  # noqa
    except ImportError:
        print("Installing test dependencies...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])

    # Build pytest command
    cmd = [
        sys.executable, "-m", "pytest",
        "--maxfail=0", "-q",
        f"--junitxml={args.junitxml}",
        f"--cov={args.cov-target if False else args.cov_target}",
        f"--cov-report=term-missing",
        f"--cov-report=xml:{args.cov_xml}"
    ]
    print(">> Running:", " ".join(cmd))
    code = subprocess.call(cmd)
    print("\n=== Summary ===")
    if code == 0:
        print("All tests passed ✅")
    else:
        print("Some tests failed ❌ (see output above and junit xml).")
    print(f"Coverage XML: {args.cov_xml}")
    print(f"JUnit XML: {args.junitxml}")
    sys.exit(code)

if __name__ == "__main__":
    main()
