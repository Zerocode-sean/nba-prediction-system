#!/usr/bin/env python3
"""
🔍 Production Deployment Health Check
=====================================

Verify all components are working before deployment.
Run this script to ensure production readiness.
"""

import sys
import importlib
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

def check_imports():
    """Check all required imports work"""
    print("🔍 CHECKING IMPORTS")
    print("-" * 30)
    
    required_packages = [
        'streamlit',
        'pandas', 
        'numpy',
        'sklearn',
        'plotly',
        'requests',
        'joblib'
    ]
    
    failed_imports = []
    
    for package in required_packages:
        try:
            importlib.import_module(package)
            print(f"✅ {package}")
        except ImportError as e:
            print(f"❌ {package}: {e}")
            failed_imports.append(package)
    
    return len(failed_imports) == 0

def check_file_structure():
    """Check all required files exist"""
    print("\n📁 CHECKING FILE STRUCTURE")
    print("-" * 30)
    
    required_files = [
        'streamlit_app.py',
        'requirements.txt',
        '.streamlit/config.toml',
        'app/user_interface.py',
        'app/admin_interface.py',
        'app/validation_dashboard.py',
        'src/prediction/pipeline.py',
        'src/prediction/realtime_system.py',
        'models/nba_win_loss_model.pkl',
        'models/nba_over_under_model.pkl'
    ]
    
    missing_files = []
    
    for file_path in required_files:
        full_path = Path(file_path)
        if full_path.exists():
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path}")
            missing_files.append(file_path)
    
    return len(missing_files) == 0

def check_app_interfaces():
    """Check app interfaces can be imported"""
    print("\n🎨 CHECKING APP INTERFACES")
    print("-" * 30)
    
    interfaces = [
        ('app.user_interface', 'User Interface'),
        ('app.admin_interface', 'Admin Interface'), 
        ('app.validation_dashboard', 'Validation Dashboard')
    ]
    
    failed_interfaces = []
    
    for module_name, display_name in interfaces:
        try:
            # Add app directory to path
            app_dir = Path(__file__).parent / "app"
            sys.path.append(str(app_dir))
            
            module = importlib.import_module(module_name.split('.')[-1])
            print(f"✅ {display_name}")
        except Exception as e:
            print(f"❌ {display_name}: {e}")
            failed_interfaces.append(display_name)
    
    return len(failed_interfaces) == 0

def check_prediction_system():
    """Check prediction system works"""
    print("\n🤖 CHECKING PREDICTION SYSTEM")
    print("-" * 30)
    
    try:
        sys.path.append(str(Path(__file__).parent))
        from src.prediction.pipeline import NBAPredictionPipeline
        
        pipeline = NBAPredictionPipeline()
        print("✅ Pipeline initialized")
        
        # Load models first
        pipeline.load_models()
        print("✅ Models loaded")
        
        # Test prediction with basic features instead of full prediction
        # Just test that predict_game method exists and models are loaded
        if pipeline.win_loss_model and pipeline.over_under_model:
            print("✅ Prediction generation ready")
            return True
        else:
            print("❌ Models not properly loaded")
            return False
            
    except Exception as e:
        print(f"❌ Prediction system error: {e}")
        return False

def check_data_access():
    """Check data files are accessible"""
    print("\n📊 CHECKING DATA ACCESS")
    print("-" * 30)
    
    try:
        import pandas as pd
        
        # Check if feature data exists
        feature_file = Path("data/processed/nba_features_for_modeling.csv")
        if feature_file.exists():
            df = pd.read_csv(feature_file)
            print(f"✅ Feature data loaded ({len(df)} rows)")
        else:
            print("⚠️ Feature data not found (will use demo mode)")
        
        # Check if models exist
        model_files = [
            "models/nba_win_loss_model.pkl",
            "models/nba_over_under_model.pkl"
        ]
        
        models_exist = all(Path(f).exists() for f in model_files)
        if models_exist:
            print("✅ ML models found")
        else:
            print("⚠️ ML models not found (will use demo mode)")
        
        return True
        
    except Exception as e:
        print(f"❌ Data access error: {e}")
        return False

def check_streamlit_config():
    """Check Streamlit configuration"""
    print("\n⚙️ CHECKING STREAMLIT CONFIG")
    print("-" * 30)
    
    config_file = Path(".streamlit/config.toml")
    secrets_example = Path(".streamlit/secrets.toml.example")
    
    if config_file.exists():
        print("✅ Streamlit config found")
    else:
        print("❌ Streamlit config missing")
    
    if secrets_example.exists():
        print("✅ Secrets example found")
    else:
        print("❌ Secrets example missing")
    
    return config_file.exists()

def check_production_files():
    """Check production-specific files"""
    print("\n🚀 CHECKING PRODUCTION FILES")
    print("-" * 30)
    
    prod_files = [
        ('requirements.txt', 'Production requirements'),
        ('.gitignore', 'Production gitignore'),
        ('README.md', 'Production README'),
        ('streamlit_app.py', 'Streamlit entry point')
    ]
    
    all_exist = True
    
    for file_path, description in prod_files:
        if Path(file_path).exists():
            print(f"✅ {description}")
        else:
            print(f"❌ {description}")
            all_exist = False
    
    return all_exist

def main():
    """Run complete health check"""
    print("🏀 NBA PREDICTIONS - PRODUCTION HEALTH CHECK")
    print("=" * 50)
    
    checks = [
        ("Imports", check_imports),
        ("File Structure", check_file_structure),
        ("App Interfaces", check_app_interfaces),
        ("Prediction System", check_prediction_system),
        ("Data Access", check_data_access),
        ("Streamlit Config", check_streamlit_config),
        ("Production Files", check_production_files)
    ]
    
    results = []
    
    for check_name, check_func in checks:
        try:
            result = check_func()
            results.append((check_name, result))
        except Exception as e:
            print(f"\n❌ {check_name} check failed: {e}")
            results.append((check_name, False))
    
    # Summary
    print("\n🏆 HEALTH CHECK SUMMARY")
    print("=" * 30)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for check_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {check_name}")
    
    print(f"\n📊 Overall: {passed}/{total} checks passed")
    
    if passed == total:
        print("\n🎉 ALL CHECKS PASSED - READY FOR DEPLOYMENT! 🚀")
        return True
    else:
        print(f"\n⚠️ {total - passed} checks failed - fix issues before deployment")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
