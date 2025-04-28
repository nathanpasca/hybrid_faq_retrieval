import pandas as pd

# Define FAQ data as a list of dictionaries
faq_data = [
    # Shipping (15 questions)
    {"question": "How do I track my order?", "answer": "Log in to your account, go to 'Order History,' and click your order number for a tracking link. If it’s not active, your order is still processing. Contact support@shop.com for help."},
    {"question": "Where’s my package?", "answer": "Check your package’s status in 'Order History' under your account. Click the order number for tracking details. If not shipped, it’s likely processing. Email support@shop.com for delays."},
    {"question": "How can I find my shipment status?", "answer": "Visit 'Order History' in your account and select your order to view tracking information. If no tracking is available, it’s still being prepared. Reach out to support@shop.com if needed."},
    {"question": "When will my order arrive?", "answer": "Delivery times depend on your shipping method and location. Check 'Order History' for estimated delivery dates. Standard shipping takes 5–7 business days. Email support@shop.com for specific inquiries."},
    {"question": "How long does shipping take?", "answer": "Standard shipping takes 5–7 business days, while express shipping takes 2–3 days. View your order’s estimated delivery in 'Order History.' Contact support@shop.com for delays."},
    {"question": "What’s the delivery time for my purchase?", "answer": "Check 'Order History' for your order’s estimated delivery date. Standard shipping is 5–7 days; express is 2–3 days. For issues, email support@shop.com."},
    {"question": "Can I change my shipping address?", "answer": "If your order hasn’t shipped, update your address in 'Order Details.' Once shipped, changes aren’t possible. Contact support@shop.com immediately to confirm options."},
    {"question": "How do I update my delivery address?", "answer": "Go to 'Order Details' to modify your address before shipping. Post-shipment changes aren’t allowed. Email support@shop.com for assistance."},
    {"question": "Is express shipping available?", "answer": "Yes, select express shipping at checkout for 2–3 day delivery. Costs vary by location. Check 'Order History' for tracking. Email support@shop.com for details."},
    {"question": "Do you offer fast delivery?", "answer": "Express shipping (2–3 days) is available at checkout. Fees depend on your location. Track your order in 'Order History.' Contact support@shop.com for help."},
    {"question": "Why is my order delayed?", "answer": "Delays may occur due to high demand, weather, or carrier issues. Check 'Order History' for updates. Email support@shop.com, and we’ll investigate."},
    {"question": "What’s causing my package delay?", "answer": "High demand, weather, or carrier issues may cause delays. View updates in 'Order History.' Contact support@shop.com for a detailed status."},
    {"question": "Do you ship internationally?", "answer": "Yes, we ship to select countries. Check available destinations at checkout. International delivery takes 7–14 days. Email support@shop.com for specifics."},
    {"question": "Can I get my order shipped abroad?", "answer": "International shipping is available to certain countries, listed at checkout. Delivery takes 7–14 days. Contact support@shop.com for details."},
    {"question": "How much is shipping?", "answer": "Shipping costs vary by location and method. View fees at checkout. Standard shipping is free for orders over $50. Email support@shop.com for clarity."},
    
    # Returns (10 questions)
    {"question": "How do I return an item?", "answer": "Initiate a return in 'Order History' within 30 days. Print the return label, pack the item, and ship it back. Refunds are processed within 7 days of receipt. Email support@shop.com for help."},
    {"question": "What’s the process for sending something back?", "answer": "Within 30 days, go to 'Order History,' select 'Return,' and follow the steps to get a return label. Ship the item back; refunds take 7 days. Contact support@shop.com."},
    {"question": "Can I return my purchase?", "answer": "Yes, returns are accepted within 30 days. Start the process in 'Order History' to get a return label. Refunds are issued within 7 days. Email support@shop.com."},
    {"question": "What is your return policy?", "answer": "Items can be returned within 30 days in original condition. Use 'Order History' to start a return and get a label. Refunds take 7 days. Contact support@shop.com."},
    {"question": "How long do I have to return something?", "answer": "You have 30 days from delivery to return items in original condition. Go to 'Order History' for a return label. Refunds are processed in 7 days. Email support@shop.com."},
    {"question": "Can I exchange an item?", "answer": "Exchanges aren’t directly offered. Return the item via 'Order History' and place a new order. Refunds take 7 days. Contact support@shop.com for assistance."},
    {"question": "How do I swap a product?", "answer": "Return the original item through 'Order History' within 30 days, then order the desired item. Refunds are processed in 7 days. Email support@shop.com."},
    {"question": "Who pays for return shipping?", "answer": "Return shipping is free for defective items. For other returns, you cover the cost unless specified. Check 'Order History' for details. Email support@shop.com."},
    {"question": "Is return shipping free?", "answer": "Free return shipping applies to faulty items. Otherwise, you pay the shipping cost. View return instructions in 'Order History.' Contact support@shop.com."},
    {"question": "How long does a refund take?", "answer": "Refunds are processed within 7 days after we receive your return. Funds return to your original payment method. Email support@shop.com for status."},
    
    # Account Management (15 questions)
    {"question": "How do I reset my password?", "answer": "Click 'Forgot Password' on the login page, enter your email, and follow the link sent to reset your password. Check spam if the email doesn’t arrive. Contact support@shop.com."},
    {"question": "What do I do if I forgot my password?", "answer": "Go to the login page, select 'Forgot Password,' and enter your email. Use the reset link sent to your inbox. Email support@shop.com if you don’t receive it."},
    {"question": "How can I recover my account?", "answer": "Use 'Forgot Password' on the login page. Enter your email to receive a reset link. If it’s missing, check spam or contact support@shop.com for help."},
    {"question": "How do I create an account?", "answer": "Click 'Sign Up' on our homepage, enter your email, name, and password, then verify your email. You’re ready to shop! Email support@shop.com for issues."},
    {"question": "How can I sign up?", "answer": "Select 'Sign Up' on the website, provide your email, name, and password, and confirm your email via the link sent. Contact support@shop.com for help."},
    {"question": "How do I update my account details?", "answer": "Log in, go to 'Account Settings,' and edit your name, email, or address. Save changes to update. Email support@shop.com for technical issues."},
    {"question": "Can I change my email address?", "answer": "In 'Account Settings,' update your email and verify the new address via the confirmation link sent. Contact support@shop.com if you encounter problems."},
    {"question": "How do I delete my account?", "answer": "Contact support@shop.com to request account deletion. We’ll process it within 48 hours after verifying your identity. Include your registered email in the request."},
    {"question": "Can I close my account?", "answer": "Email support@shop.com with your registered email to delete your account. Deletion takes 48 hours after verification. Reach out for assistance."},
    {"question": "Why can’t I log in?", "answer": "Check your email and password. Use 'Forgot Password' if needed. Ensure your account is verified. Email support@shop.com if issues persist."},
    {"question": "What if I’m unable to sign in?", "answer": "Verify your email and password. Try resetting via 'Forgot Password.' Confirm your account is active. Contact support@shop.com for further help."},
    {"question": "How do I add a shipping address?", "answer": "In 'Account Settings,' go to 'Addresses,' click 'Add New,' and enter your details. Save to update. Email support@shop.com for issues."},
    {"question": "Can I save a new delivery address?", "answer": "Go to 'Account Settings,' select 'Addresses,' and add a new address. Save it for future orders. Contact support@shop.com if you need help."},
    {"question": "How do I verify my account?", "answer": "Check your email for a verification link after signing up. Click it to activate. If missing, check spam or email support@shop.com for a resend."},
    {"question": "Why isn’t my account verified?", "answer": "Look for the verification email sent during signup. Click the link to activate. If not found, check spam or contact support@shop.com."},
    
    # Payments (10 questions)
    {"question": "What payment methods do you accept?", "answer": "We accept credit/debit cards (Visa, MasterCard, Amex), PayPal, and Apple Pay. Select your method at checkout. Email support@shop.com for issues."},
    {"question": "How can I pay for my order?", "answer": "Use Visa, MasterCard, Amex, PayPal, or Apple Pay at checkout. Choose your preferred method. Contact support@shop.com for payment problems."},
    {"question": "Why was my payment declined?", "answer": "Declines may occur due to insufficient funds, incorrect details, or bank restrictions. Verify your info and try again. Email support@shop.com for help."},
    {"question": "What if my card was rejected?", "answer": "Check your card details, balance, or bank restrictions. Re-enter info or use another method. Contact support@shop.com for assistance."},
    {"question": "Can I use a gift card?", "answer": "Yes, enter your gift card code at checkout to apply the balance. If it doesn’t work, email support@shop.com with the code."},
    {"question": "How do I apply a gift card?", "answer": "At checkout, input your gift card code in the designated field. The balance will apply. Contact support@shop.com if it fails."},
    {"question": "Is my payment secure?", "answer": "All payments are encrypted with SSL technology for security. We don’t store card details. Email support@shop.com with concerns."},
    {"question": "Are transactions safe on your site?", "answer": "We use SSL encryption to protect all transactions. Your payment info is secure. Contact support@shop.com for security questions."},
    {"question": "Can I pay in installments?", "answer": "Installment plans are available via PayPal Credit for eligible orders. Select it at checkout. Email support@shop.com for details."},
    {"question": "Do you offer payment plans?", "answer": "PayPal Credit offers installment payments for qualifying orders. Choose it at checkout. Contact support@shop.com for more info."},
]

# Create DataFrame
df = pd.DataFrame(faq_data)

# Save to CSV
df.to_csv('faq_dataset.csv', index=False)
print("FAQ dataset saved to 'faq_dataset.csv' with 50 entries.")