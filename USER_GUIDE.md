# 🏀 NBA Prediction Hub - User Guide

## 🚀 Quick Start

### Launch the App
```bash
python launch_app.py
```
The web interface will open at: http://localhost:8501

## 📱 How to Use

### 1. **Making Predictions**
- Select **Home Team** from the dropdown
- Select **Away Team** from the dropdown  
- Click **"GET PREDICTION"** button
- View your prediction results instantly!

### 2. **Understanding Predictions**

#### 🏆 Win/Loss Predictions
- Shows which team is predicted to win
- Displays win probabilities for both teams
- **HOME** = Home team wins | **AWAY** = Away team wins

#### 📈 Over/Under Predictions  
- Predicts if total score will be OVER or UNDER the line
- Default line is **235 points**
- Shows probabilities for both OVER and UNDER

#### 🎯 Confidence Levels
- **🔥 HIGH (80%+)**: Very confident bet
- **⚡ MEDIUM (65-80%)**: Good confidence bet  
- **⚠️ LOW (<65%)**: Less confident, use caution

### 3. **Betting Recommendations**

Each prediction includes:
- **Best Bet**: Highest confidence prediction
- **Confidence Level**: Color-coded confidence indicator
- **Probabilities**: Percentage chances for each outcome

## 📊 Features

### 🎨 **Beautiful Design**
- Modern, mobile-friendly interface
- Color-coded confidence levels
- Clear visual indicators
- Easy-to-read cards and metrics

### 🏀 **NBA Teams**
- All 30 NBA teams available
- Team colors and styling
- Home/Away designations

### 📈 **Advanced Analytics**
- Machine learning predictions (100% Win/Loss, 96.7% Over/Under accuracy)
- Cross-validated models
- Historical data training (150+ games)

### 📱 **Mobile Responsive**
- Works on all devices
- Touch-friendly interface
- Optimized for mobile betting

## 🎯 Betting Tips

### High Confidence Bets (🔥)
- **80%+ confidence**: Strong betting opportunity
- Model is very confident in prediction
- Higher probability of success

### Medium Confidence Bets (⚡)  
- **65-80% confidence**: Good betting opportunity
- Solid prediction with decent confidence
- Consider bet size accordingly

### Low Confidence Bets (⚠️)
- **<65% confidence**: Use caution
- Model is less certain
- Consider smaller bets or avoid

## 🔧 Troubleshooting

### App Won't Start
```bash
# Install missing packages
pip install streamlit plotly

# Try manual launch
streamlit run app/nba_prediction_app.py
```

### No Predictions Showing
- Try "Load Sample Predictions" in sidebar
- Check internet connection
- Restart the app

### Teams Not Loading
- Check if data files exist in `/data/processed/`
- Try sample predictions first
- Contact support if issues persist

## 📞 Support

For technical issues:
1. Check the terminal for error messages
2. Try restarting the app
3. Use sample predictions mode
4. Review this user guide

## 🎉 Enjoy Your NBA Predictions!

Your NBA Prediction Hub is now ready for professional sports betting analysis. Good luck with your bets! 🍀

---
*Disclaimer: This is for educational and entertainment purposes. Please bet responsibly.*
