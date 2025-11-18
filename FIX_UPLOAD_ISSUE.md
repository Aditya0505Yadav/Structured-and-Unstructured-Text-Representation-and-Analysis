# 🚨 SOLUTION: Pass Token Directly in Command

## The Problem
Windows terminal sometimes blocks interactive input for Twine.

## ✅ SOLUTION: Pass credentials directly

Replace `YOUR_TOKEN_HERE` with your actual PyPI token, then run:

```powershell
python -m twine upload dist/* -u __token__ -p YOUR_TOKEN_HERE
```

## 📝 Step-by-Step:

### 1. Get Your PyPI API Token

1. Go to: https://pypi.org/manage/account/token/
2. Click "**Add API token**"
3. Token name: `SUTRA`
4. Scope: Select "**Entire account**"
5. Click "**Add token**"
6. **COPY THE TOKEN** (it starts with `pypi-...`)
   ⚠️ You can only see it once!

### 2. Upload Using Token

```powershell
python -m twine upload dist/* -u __token__ -p pypi-YOUR-ACTUAL-TOKEN-HERE
```

**Example:**
```powershell
python -m twine upload dist/* -u __token__ -p pypi-AgEIcHlwaS5vcmcCJGFiY2RlZi0xMjM0LTU2NzgtOTBhYi1jZGVmMDEyMzQ1Njc
```

---

## 🧪 Test on Test PyPI First (Recommended)

### 1. Get Test PyPI Token
- Go to: https://test.pypi.org/manage/account/token/
- Create token same way

### 2. Upload to Test PyPI
```powershell
python -m twine upload --repository testpypi dist/* -u __token__ -p YOUR_TEST_TOKEN
```

### 3. Test Install
```powershell
pip install --index-url https://test.pypi.org/simple/ sutra
```

### 4. If successful, upload to real PyPI
```powershell
python -m twine upload dist/* -u __token__ -p YOUR_REAL_TOKEN
```

---

## 🎯 Alternative: Use Environment Variables

**PowerShell:**
```powershell
$env:TWINE_USERNAME = "__token__"
$env:TWINE_PASSWORD = "pypi-YOUR-TOKEN-HERE"
python -m twine upload dist/*
```

**CMD:**
```cmd
set TWINE_USERNAME=__token__
set TWINE_PASSWORD=pypi-YOUR-TOKEN-HERE
python -m twine upload dist/*
```

---

## 🔐 Alternative: Save in .pypirc (Most Secure)

1. Create file: `C:\Users\ADITYA BATTA\.pypirc`

2. Add this content:
```ini
[pypi]
username = __token__
password = pypi-YOUR-TOKEN-HERE
```

3. Then just run:
```powershell
python -m twine upload dist/*
```

---

## ✅ Success Looks Like:

```
Uploading distributions to https://upload.pypi.org/legacy/
Uploading sutra-0.1.0-py3-none-any.whl
100% ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 42.2/42.2 kB • 00:00 • ?
Uploading sutra-0.1.0.tar.gz
100% ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 42.7/42.7 kB • 00:00 • ?

View at:
https://pypi.org/project/sutra/0.1.0/
```

---

## 🎉 After Success

Your package is live! Anyone can now:

```bash
pip install sutra
```

Test it yourself:
```bash
pip install sutra
python -c "from sutra import SUTRA; print('Success!')"
```

---

## 🆘 Still Having Issues?

Try this in Python directly:

```python
import subprocess
import getpass

token = getpass.getpass("Paste your PyPI token: ")
cmd = f'python -m twine upload dist/* -u __token__ -p {token}'
subprocess.run(cmd, shell=True)
```

Or just use this command format:
```powershell
# On one line, replace YOUR_TOKEN:
python -m twine upload dist/* -u __token__ -p YOUR_TOKEN
```
