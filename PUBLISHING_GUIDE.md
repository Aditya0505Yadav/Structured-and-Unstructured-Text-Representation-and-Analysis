# SUTRA - Publishing Guide to PyPI

This guide will help you publish SUTRA to PyPI so anyone can install it with `pip install sutra`.

## 📋 Pre-requisites

1. **PyPI Account**: Create account at https://pypi.org/account/register/
2. **Test PyPI Account** (recommended): https://test.pypi.org/account/register/
3. **Python 3.8+** installed
4. **Project ready** with all files

## 🔧 Step 1: Install Required Tools

```bash
pip install build twine
```

## 📦 Step 2: Project Structure

Make sure your project looks like this:

```
SUTRA/
├── sutra/
│   ├── __init__.py          ✅ (contains: from .sutra_simple import SUTRA)
│   └── sutra_simple.py      ✅ (main code - single file with everything)
├── setup.py                  ✅
├── pyproject.toml           ✅
├── README.md                ✅
├── LICENSE                  ⚠️  (need to create)
├── requirements.txt         ✅
└── .gitignore              ✅
```

## 📝 Step 3: Create LICENSE File

```bash
# Create MIT License
cat > LICENSE << 'EOF'
MIT License

Copyright (c) 2024 Your Name

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
EOF
```

## ⚙️ Step 4: Update setup.py

Open `setup.py` and update these fields:

```python
setup(
    name="sutra",  # ⚠️ This name must be unique on PyPI
    version="0.1.0",
    author="Your Name",  # ⚠️ UPDATE THIS
    author_email="your.email@example.com",  # ⚠️ UPDATE THIS
    description="Natural Language to SQL Query System with Visualization",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/sutra",  # ⚠️ UPDATE THIS
    # ... rest stays the same
)
```

## 🔨 Step 5: Build the Package

```bash
# Clean previous builds
rm -rf build/ dist/ *.egg-info

# Build the package
python -m build
```

This creates:
- `dist/sutra-0.1.0.tar.gz` (source distribution)
- `dist/sutra-0.1.0-py3-none-any.whl` (wheel distribution)

## 🧪 Step 6: Test on Test PyPI (Recommended)

```bash
# Upload to Test PyPI
python -m twine upload --repository testpypi dist/*

# You'll be prompted for:
# Username: your_testpypi_username
# Password: your_testpypi_password
```

Test installation:

```bash
# Install from Test PyPI
pip install --index-url https://test.pypi.org/simple/ sutra

# Test it
python -c "from sutra import SUTRA; print('Success!')"
```

## 🚀 Step 7: Publish to Real PyPI

Once testing is successful:

```bash
# Upload to real PyPI
python -m twine upload dist/*

# You'll be prompted for:
# Username: your_pypi_username
# Password: your_pypi_password (or API token)
```

## 🎉 Step 8: Verify Publication

1. Visit https://pypi.org/project/sutra/
2. Install from PyPI:

```bash
pip install sutra
```

3. Test:

```python
from sutra import SUTRA

sutra = SUTRA(api_key="test")
print("SUTRA installed successfully!")
```

## 🔐 Using API Tokens (Recommended)

Instead of username/password, use API tokens:

1. Go to https://pypi.org/manage/account/token/
2. Create a new API token
3. Use it instead of password:

```bash
# Create .pypirc file
cat > ~/.pypirc << 'EOF'
[pypi]
username = __token__
password = pypi-YourActualTokenHere

[testpypi]
username = __token__
password = pypi-YourTestTokenHere
EOF

# Set permissions
chmod 600 ~/.pypirc
```

Now you can upload without entering credentials:

```bash
python -m twine upload dist/*
```

## 🔄 Updating the Package

When you make changes:

1. **Update version** in `setup.py` and `pyproject.toml`:
   ```python
   version="0.1.1",  # Increment version
   ```

2. **Update version** in `sutra_simple.py`:
   ```python
   __version__ = "0.1.1"
   ```

3. **Clean and rebuild**:
   ```bash
   rm -rf build/ dist/ *.egg-info
   python -m build
   ```

4. **Upload**:
   ```bash
   python -m twine upload dist/*
   ```

## ✅ Checklist Before Publishing

- [ ] Updated `author` and `author_email` in setup.py
- [ ] Updated GitHub URL in setup.py
- [ ] Created LICENSE file
- [ ] README.md is complete and formatted
- [ ] Version number is set correctly
- [ ] Tested locally: `pip install -e .`
- [ ] Tested on Test PyPI
- [ ] All dependencies listed in requirements.txt
- [ ] .gitignore excludes build files

## 📝 Common Issues

### Issue: Package name already exists

**Solution**: Choose a different name in `setup.py`:
```python
name="sutra-nlp",  # or sutra-query, my-sutra, etc.
```

### Issue: Upload fails with 403 error

**Solution**: Check credentials or use API token

### Issue: Module not found after installation

**Solution**: Check `__init__.py` has correct imports:
```python
from .sutra_simple import SUTRA
```

### Issue: Dependencies not installing

**Solution**: Ensure `install_requires` in setup.py matches requirements.txt

## 🎯 Quick Reference Commands

```bash
# Build
python -m build

# Test PyPI upload
python -m twine upload --repository testpypi dist/*

# Real PyPI upload
python -m twine upload dist/*

# Install locally for testing
pip install -e .

# Uninstall
pip uninstall sutra -y

# Check package
twine check dist/*
```

## 🌟 After Publishing

1. **Tag the release on GitHub**:
   ```bash
   git tag -a v0.1.0 -m "Release version 0.1.0"
   git push origin v0.1.0
   ```

2. **Announce** on social media, Reddit, forums

3. **Create documentation** site (optional)

4. **Monitor** PyPI downloads: https://pypistats.org/packages/sutra

## 🆘 Need Help?

- PyPI Help: https://pypi.org/help/
- Packaging Guide: https://packaging.python.org/
- Twine Docs: https://twine.readthedocs.io/

---

**Congratulations! Your package is now live on PyPI! 🎉**

Anyone can now install it with:
```bash
pip install sutra
```
