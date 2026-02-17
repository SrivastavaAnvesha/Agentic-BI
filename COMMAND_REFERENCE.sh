#!/bin/bash
# QUICK COMMAND REFERENCE - Agentic BI 60-70%
# ============================================

# === SETUP & INSTALLATION ===

# 1. Install all required packages
pip install streamlit pandas plotly sqlalchemy psycopg2-binary python-dotenv google-genai

# 2. Upgrade packages (if needed)
pip install --upgrade streamlit plotly pandas

# === DATABASE COMMANDS ===

# 3. Verify PostgreSQL is running
psql -U postgres -d agentic_bi -c "SELECT COUNT(*) FROM raw_sales_data;"

# 4. Check database size
psql -U postgres -d agentic_bi -c "SELECT COUNT(*) as total_records, SUM(sales_amount) as total_sales FROM raw_sales_data;"

# 5. List all tables
psql -U postgres -d agentic_bi -c "\dt"

# === TESTING COMMANDS ===

# 6. Test Gemini API connection
python -c "from google import genai; print('✅ Gemini works')"

# 7. Test brain.py module
python brain.py

# 8. Verify list_models.py fix
python list_models.py

# === RUN DASHBOARD ===

# 9. Start dashboard (main command)
streamlit run app.py

# 10. Start dashboard with custom port
streamlit run app.py --server.port 8502

# 11. Start dashboard with debug logging
streamlit run app.py --logger.level=debug

# 12. Run dashboard and open browser automatically
streamlit run app.py --client.showErrorDetails=true

# === DEVELOPMENT COMMANDS ===

# 13. Check Python syntax
python -m py_compile app.py

# 14. Format code with Black
pip install black
black app.py

# 15. Run linter for errors
pip install pylint
pylint app.py

# === FILE MANAGEMENT ===

# 16. List all project files
ls -la

# 17. View app.py
cat app.py

# 18. View brain.py
cat brain.py

# 19. Count lines in files
wc -l app.py brain.py list_models.py

# 20. Check file size
du -h app.py

# === TROUBLESHOOTING ===

# 21. Kill streamlit on port 8501 (if stuck)
lsof -i :8501
kill -9 <PID>

# 22. Kill PostgreSQL connection (if stuck)
psql -U postgres -d agentic_bi -c "SELECT pid FROM pg_stat_activity WHERE datname = 'agentic_bi';"

# 23. Check system Python version
python --version

# 24. Check pip packages
pip list | grep -E "streamlit|plotly|pandas|sqlalchemy"

# 25. Verify .env file
cat .env

# === ENVIRONMENT SETUP ===

# 26. Create virtual environment (optional)
python -m venv venv

# 27. Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# 28. Deactivate virtual environment
deactivate

# === GIT COMMANDS (if using version control) ===

# 29. Initialize git repo
git init

# 30. Add all files to git
git add .

# 31. Commit changes
git commit -m "60-70% Milestone: Add data visualizations"

# === MONITORING ===

# 32. Monitor Streamlit process
ps aux | grep streamlit

# 33. Check system resources
top -p $(pgrep -f streamlit)

# 34. View system memory usage
free -h

# 35. Check disk space
df -h

# === BACKUP ===

# 36. Backup entire project
cp -r . ../Agentic_BI_Project_backup

# 37. Backup PostgreSQL database
pg_dump -U postgres agentic_bi > agentic_bi_backup.sql

# === DOCUMENTATION ===

# 38. Generate code documentation
pydoc app.py > app_docs.txt

# 39. View markdown files
cat MILESTONE_60-70_COMPLETE.md

# 40. View quick start guide
cat QUICK_START_60-70.txt

# === ADVANCED ===

# 41. Run app with profiler (performance testing)
python -m cProfile app.py

# 42. Export requirements.txt for sharing
pip freeze > requirements.txt

# 43. Install from requirements
pip install -r requirements.txt

# 44. Check for unused imports
pip install autoflake
autoflake --remove-all-unused-imports --in-place app.py

# === SHORTCUTS ===

# Quick test suite:
echo "🧪 Running tests..."
python -m py_compile app.py && echo "✅ Syntax OK" || echo "❌ Syntax Error"
python -c "from google import genai; print('✅ Gemini OK')" || echo "❌ Gemini Error"
psql -U postgres -d agentic_bi -c "SELECT 1;" 2>/dev/null && echo "✅ DB OK" || echo "❌ DB Error"

# Quick start:
echo "🚀 Starting dashboard..."
streamlit run app.py

# === WINDOWS POWERSHELL EQUIVALENTS ===

# For Windows users, replace Unix commands:

# List files:
# ls -la  →  Get-ChildItem -Force
# cat file  →  Get-Content file
# wc -l  →  (Get-Content file | Measure-Object -Line).Lines
# du -h  →  (Get-Item file).Length
# lsof -i :port  →  netstat -ano | findstr :port
# kill -9 PID  →  Stop-Process -Id PID -Force
# top  →  Get-Process | Sort-Object CPU -Descending
# free -h  →  Get-WmiObject Win32_OperatingSystem | Select-Object TotalVisibleMemorySize, FreePhysicalMemory
# df -h  →  Get-Volume
# grep  →  Select-String

# === USEFUL ONE-LINERS ===

# Run app and show real-time logs
streamlit run app.py 2>&1 | tee streamlit.log

# Reload app on file changes (dev mode)
streamlit run app.py --logger.level=debug --client.showErrorDetails=true

# Check if port is in use
netstat -ano | findstr :8501

# Test all connections at once
echo "Testing connections..." && python brain.py && streamlit run app.py &

# === MONITORING DASHBOARD ===

# Run Streamlit with profiling
streamlit run app.py --logger.level=debug --client.showErrorDetails=true --logLevel=debug

# === CLEANUP ===

# Remove cache files
rm -rf .streamlit __pycache__ *.pyc .pytest_cache

# Clean everything for fresh start
rm -rf .streamlit __pycache__ *.pyc .pytest_cache .egg-info dist build

# === DEPLOYMENT PREP ===

# Create production requirements
pip freeze > requirements_prod.txt

# Generate project documentation
pydoc3 -w app brain list_models

# === FINAL CHECKLIST ===

# Before demo/presentation:
✅ streamlit run app.py          # Works without errors
✅ python brain.py               # AI is responsive
✅ psql -U postgres ...          # Database has data
✅ Quick query buttons work      # All 4 buttons functional
✅ Charts display correctly      # Plotly renders fine
✅ Sidebar stats load            # DB connection alive
✅ Dark theme displays correctly # CSS loaded
✅ No console errors             # Clean logs
✅ Response time < 10s           # Acceptable performance
✅ All buttons responsive        # UI is interactive

# === CONTACT & HELP ===

# View documentation:
cat README_SOLUTION.md
cat TROUBLESHOOTING.md
cat ARCHITECTURE.txt
cat DASHBOARD_UPDATE.md
cat MILESTONE_60-70_COMPLETE.md
cat BEFORE_AND_AFTER.md
cat QUICK_START_60-70.txt

# === TIME ESTIMATES ===

# Setup:                      5-10 minutes
# First run:                  2-3 minutes
# Testing all features:       10-15 minutes
# Full setup + test:          20-30 minutes
# Dashboard customization:    15-30 minutes

# === SUCCESS CRITERIA ===

# Your setup is ready when:
✓ Dashboard loads in 1-2 seconds
✓ Quick queries return in 3-5 seconds
✓ Charts render without errors
✓ Sidebar stats show correct numbers
✓ Dark theme displays properly
✓ No console errors or warnings
✓ All 4 quick buttons work
✓ Custom queries work smoothly

# === NEXT STEPS ===

# 1. Run: streamlit run app.py
# 2. Test: Click all quick query buttons
# 3. Try: Ask a custom question
# 4. Check: Verify all metrics and charts
# 5. Optimize: Add more features for 80%

# === REMEMBER ===

# Current Status: 60-70% Complete ✅
# Target: 100% Production Ready
# Next: 80% with advanced analytics
# Goal: Professional BI platform

# Good luck! 🚀
