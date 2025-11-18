"""
SUTRA Pre-Publishing Checker
This script checks if everything is ready for publishing
"""

import os
import sys
from pathlib import Path

def check_file(filepath, description):
    """Check if a file exists"""
    if os.path.exists(filepath):
        print(f"✓ {description}: {filepath}")
        return True
    else:
        print(f"✗ MISSING: {description}: {filepath}")
        return False

def check_content(filepath, search_text, description):
    """Check if file contains specific text"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            if search_text in content:
                print(f"✓ {description}")
                return True
            else:
                print(f"⚠ WARNING: {description} - Needs update!")
                return False
    except Exception as e:
        print(f"✗ ERROR checking {filepath}: {e}")
        return False

def main():
    print("=" * 60)
    print("SUTRA PRE-PUBLISHING CHECKER")
    print("=" * 60)
    print()
    
    all_good = True
    
    # Check essential files
    print("📁 CHECKING ESSENTIAL FILES...")
    print("-" * 60)
    all_good &= check_file("setup.py", "Setup file")
    all_good &= check_file("pyproject.toml", "Project config")
    all_good &= check_file("README.md", "README")
    all_good &= check_file("LICENSE", "License")
    all_good &= check_file("requirements.txt", "Requirements")
    all_good &= check_file("MANIFEST.in", "Manifest")
    print()
    
    # Check package structure
    print("📦 CHECKING PACKAGE STRUCTURE...")
    print("-" * 60)
    all_good &= check_file("sutra/__init__.py", "Package init")
    all_good &= check_file("sutra/sutra_client.py", "Main client")
    print()
    
    # Check examples
    print("📚 CHECKING EXAMPLES...")
    print("-" * 60)
    check_file("examples/sutra_usage_guide.ipynb", "Jupyter tutorial")
    check_file("examples/quickstart.py", "Quick start script")
    print()
    
    # Check if author info is updated
    print("👤 CHECKING AUTHOR INFORMATION...")
    print("-" * 60)
    needs_update = False
    
    if check_content("setup.py", "Your Name", "Author name in setup.py"):
        print("⚠ Please update 'Your Name' in setup.py")
        needs_update = True
    
    if check_content("setup.py", "your.email@example.com", "Email in setup.py"):
        print("⚠ Please update email in setup.py")
        needs_update = True
    
    if check_content("setup.py", "yourusername", "GitHub URL in setup.py"):
        print("⚠ Please update GitHub URL in setup.py")
        needs_update = True
    
    if not needs_update:
        print("✓ Author information looks updated!")
    
    print()
    
    # Check dependencies
    print("📦 CHECKING DEPENDENCIES...")
    print("-" * 60)
    try:
        import build
        print("✓ 'build' package installed")
    except ImportError:
        print("✗ 'build' not installed. Run: pip install build")
        all_good = False
    
    try:
        import twine
        print("✓ 'twine' package installed")
    except ImportError:
        print("✗ 'twine' not installed. Run: pip install twine")
        all_good = False
    
    print()
    
    # Final summary
    print("=" * 60)
    print("SUMMARY")
    print("=" * 60)
    
    if all_good and not needs_update:
        print("✅ Everything looks good! Ready to publish!")
        print()
        print("Next steps:")
        print("1. Test locally: pip install -e .")
        print("2. Run: python examples/quickstart.py")
        print("3. Build: python -m build")
        print("4. Upload to TestPyPI: python -m twine upload --repository testpypi dist/*")
        print("5. Upload to PyPI: python -m twine upload dist/*")
        print()
        print("Or use the automated script:")
        print("  Windows: publish.bat")
        print("  Linux/Mac: ./publish.sh")
    else:
        print("⚠ Some items need attention!")
        print()
        if needs_update:
            print("TODO:")
            print("1. Update author information in setup.py and pyproject.toml")
            print("2. Update GitHub URLs")
            print("3. Update contact email in README.md")
        if not all_good:
            print("4. Install missing dependencies")
        print()
        print("Then run this checker again: python check_ready.py")
    
    print()
    print("For detailed instructions, see: PUBLISHING_GUIDE.md")
    print()

if __name__ == "__main__":
    main()
