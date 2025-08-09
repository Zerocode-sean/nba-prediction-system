# 📝 Git Remote Setup Commands

## After creating your remote repository, run these commands:

# 1. Add your remote repository (replace YOUR_USERNAME)
git remote add origin https://github.com/YOUR_USERNAME/nba-prediction-system.git

# 2. Rename branch to main (if needed)
git branch -M main

# 3. Push to remote repository
git push -u origin main

# 4. Verify the push worked
git remote -v

## Alternative: If using GitLab
git remote add origin https://gitlab.com/YOUR_USERNAME/nba-prediction-system.git
git branch -M main
git push -u origin main

## Troubleshooting:
# If you get authentication errors:
# - Use personal access token instead of password
# - Or set up SSH keys

## After successful push:
# Your repository will be available at:
# https://github.com/YOUR_USERNAME/nba-prediction-system
# 
# Ready for Streamlit Cloud deployment! 🚀
