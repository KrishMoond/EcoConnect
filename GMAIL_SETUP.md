# Gmail SMTP Setup for OTP Login

## Steps to Enable Gmail for Sending OTP Emails:

### 1. Enable 2-Step Verification
1. Go to your Google Account: https://myaccount.google.com/
2. Click on "Security" in the left sidebar
3. Under "Signing in to Google", click on "2-Step Verification"
4. Follow the steps to enable 2-Step Verification

### 2. Generate App Password
1. After enabling 2-Step Verification, go back to Security settings
2. Under "Signing in to Google", click on "App passwords"
3. Select "Mail" as the app and "Other" as the device
4. Enter "Django EcoConnect" as the device name
5. Click "Generate"
6. Copy the 16-character password (remove spaces)

### 3. Update Django Settings
Open `sustainabilityhub/settings.py` and update:

```python
EMAIL_HOST_USER = 'your-email@gmail.com'  # Your Gmail address
EMAIL_HOST_PASSWORD = 'your-app-password'  # The 16-character app password
```

### 4. Alternative: Use Environment Variables (Recommended)
Create a `.env` file in the project root:

```
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

Then the settings will automatically load from environment variables.

### 5. Test the Setup
1. Restart the Django server
2. Go to OTP Login page
3. Enter a registered email address
4. Check your Gmail inbox for the OTP code

## Troubleshooting:

### "Username and Password not accepted"
- Make sure you're using an App Password, not your regular Gmail password
- Verify 2-Step Verification is enabled
- Check that EMAIL_HOST_USER matches the Gmail account that generated the App Password

### "SMTPAuthenticationError"
- Double-check the App Password (no spaces)
- Ensure the Gmail account is active and not suspended

### Email not received
- Check spam/junk folder
- Verify the recipient email is correct
- Check Gmail's "Sent" folder to confirm email was sent

## Security Notes:
- Never commit EMAIL_HOST_PASSWORD to Git
- Use environment variables for production
- App Passwords are safer than using your main Gmail password
- You can revoke App Passwords anytime from Google Account settings
