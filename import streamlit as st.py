import streamlit as st
import requests

# API Key สำหรับการแปลงสกุลเงิน
api_key = 'xxxxxxxxxx'

# รายการของ denominations ตามสกุลเงิน
denominations = {
    "EUR": {
        "500 euro": 500,
        "200 euro": 200,
        "100 euro": 100,
        "50 euro": 50,
        "20 euro": 20,
        "10 euro": 10,
        "5 euro": 5,
        "2 euro": 2,
        "1 euro": 1,
        "50 cent": 0.50,
        "20 cent": 0.20,
        "10 cent": 0.10,
        "5 cent": 0.05,
        "2 cent": 0.02,
        "1 cent": 0.01,
    }
}

# ฟังก์ชันคำนวณบิล
def calculate_bill(bill_amount, tax_rate, tip_percentage, num_people):
    tax = bill_amount * (tax_rate / 100)
    tip = bill_amount * (tip_percentage / 100)
    total_bill = bill_amount + tax + tip
    price_per_person = total_bill / num_people if num_people > 0 else 0
    return tax, tip, total_bill, price_per_person

# ฟังก์ชันแปลงสกุลเงิน
def convert_currency(api_key, from_currency, to_currency, amount):
    url = f"https://v6.exchangerate-api.com/v6/{api_key}/pair/{from_currency}/{to_currency}/{amount}"
    try:
        response = requests.get(url)
        data = response.json()
        if response.status_code == 200:
            return data['conversion_result']
        else:
            st.error(f"Error: {data['error-type']}")
            return None
    except Exception as e:
        st.error(f"Error occurred: {e}")
        return None

# ฟังก์ชันแสดงใบเสร็จ
def display_receipt(bill_amount, tax, tip, total_bill_converted, price_per_person_converted, paid_amount, change, currency):
    receipt = f"""
    <div style="border: 1px solid #ccc; border-radius: 10px; padding: 20px; width: 400px; margin: auto; font-family: Arial, sans-serif;">
        <h2 style="text-align: center; color: #007BFF;">Receipt</h2>
        <p><strong>Bill Amount:</strong> €{bill_amount:.2f}</p>
        <p><strong>Tax:</strong> €{tax:.2f}</p>
        <p><strong>Tip:</strong> €{tip:.2f}</p>
        <p><strong>Total Bill:</strong> {total_bill_converted:.2f} {currency}</p>
        <p><strong>Price per Person:</strong> {price_per_person_converted:.2f} {currency}</p>
        <p><strong>Paid Amount:</strong> {paid_amount:.2f} {currency}</p>
        <p><strong>Change:</strong> {change:.2f} {currency}</p>
        <p style="text-align: center; color: #28a745;">Thank you for your payment!</p>
    </div>
    """
    st.markdown(receipt, unsafe_allow_html=True)

# ส่วนอินเตอร์เฟสสำหรับการคำนวณบิล
st.title("Bill Calculator")
st.sidebar.header("Enter Bill Details")

# อินพุตข้อมูลบิล
bill_amount = st.sidebar.number_input("Bill Amount (EUR):", min_value=0.0, format="%.2f")
tax_rate = st.sidebar.number_input("Tax Rate (%):", min_value=0.0, format="%.2f")
tip_percentage = st.sidebar.number_input("Tip Percentage (%):", min_value=0.0, format="%.2f")
num_people = st.sidebar.number_input("Number of People:", min_value=1)

# ตัวเลือกสกุลเงินสำหรับการจ่าย
to_currency = st.sidebar.selectbox("Select currency for payment:", ["EUR"])

# คำนวณบิลและเก็บค่าใน session_state
if st.sidebar.button("Calculate"):
    tax, tip, total_bill, price_per_person = calculate_bill(bill_amount, tax_rate, tip_percentage, num_people)
    total_bill_converted = convert_currency(api_key, "EUR", to_currency, total_bill)
    price_per_person_converted = convert_currency(api_key, "EUR", to_currency, price_per_person)

    st.session_state.tax = tax
    st.session_state.tip = tip
    st.session_state.total_bill_converted = total_bill_converted
    st.session_state.price_per_person_converted = price_per_person_converted
    st.session_state.calculated = True

# ตรวจสอบว่าคำนวณเสร็จแล้วหรือไม่ก่อนแสดงผล
if st.session_state.get('calculated', False):
    st.subheader("Calculation Result")
    st.write(f"Tax: {st.session_state.tax:.2f} EUR")
    st.write(f"Tip: {st.session_state.tip:.2f} EUR")
    st.write(f"Total Bill: {st.session_state.total_bill_converted:.2f} {to_currency}")
    st.write(f"Price per Person: {st.session_state.price_per_person_converted:.2f} {to_currency}")

    # ส่วนสำหรับการชำระเงิน
    st.subheader("Payment")

    # ใช้ฟอร์มสำหรับการป้อนเงิน
    with st.form(key='payment_form'):
        paid_amount = 0
        selected_denominations = denominations[to_currency]

        for denomination, value in selected_denominations.items():
            count = st.number_input(f"{denomination}:", min_value=0, step=1, key=denomination)
            paid_amount += count * value

        submit_button = st.form_submit_button(label='Pay')

        if submit_button:
            if paid_amount >= st.session_state.total_bill_converted:
                change = paid_amount - st.session_state.total_bill_converted
                display_receipt(bill_amount, st.session_state.tax, st.session_state.tip, st.session_state.total_bill_converted, st.session_state.price_per_person_converted, paid_amount, change, to_currency)
            else:
                shortfall = st.session_state.total_bill_converted - paid_amount
                st.error(f"Not enough money provided. You need to add {shortfall:.2f} {to_currency}.")
