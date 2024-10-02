import streamlit as st

# ฟังก์ชันคำนวณขนาดไฟล์ภาพ
def calculate_image_file_size(width, height, bits_per_pixel):
    size_bytes = (width * height * bits_per_pixel) / 8
    size_mb = size_bytes / (1024 * 1024)
    return size_mb

# ฟังก์ชันคำนวณขนาดไฟล์วิดีโอ
def calculate_video_file_size(bitrate_mbps, duration_seconds):
    size_bytes = (bitrate_mbps * 1_000_000 * duration_seconds) / 8
    size_mb = size_bytes / (1024 * 1024)
    return size_mb

# ฟังก์ชันคำนวณขนาดไฟล์ฟิล์ม
def calculate_film_file_size(width, height, frames, bits_per_pixel):
    size_bytes = (width * height * frames * bits_per_pixel) / 8
    size_gb = size_bytes / (1024 * 1024 * 1024)
    return size_gb

# ฟังก์ชันคำนวณมวลกายที่ไม่มีไขมัน
def calculate_lean_body_mass(weight_kg, height_cm, gender):
    if gender == "Male":
        lbm = (0.407 * weight_kg) + (0.267 * height_cm) - 19.2
    else:
        lbm = (0.252 * weight_kg) + (0.473 * height_cm) - 48.3
    return lbm

# ฟังก์ชันคำนวณความต้องการแคลอรี
def calculate_calorie_needs(weight_kg, height_cm, age, gender, activity_level):
    if gender == "Male":
        bmr = 10 * weight_kg + 6.25 * height_cm - 5 * age + 5
    else:
        bmr = 10 * weight_kg + 6.25 * height_cm - 5 * age - 161

    activity_multipliers = {
        "Sedentary": 1.2,
        "Lightly Active": 1.375,
        "Moderately Active": 1.55,
        "Very Active": 1.725,
        "Super Active": 1.9
    }

    calorie_needs = bmr * activity_multipliers.get(activity_level, 1.2)
    return calorie_needs

# ฟังก์ชันหลักสำหรับ Streamlit app
def main():
    st.title("Health and File Size Calculator")

    # ส่วนคำนวณขนาดไฟล์
    st.header("File Size Calculator")
    option = st.selectbox("Select File Type:", ("Image", "Video", "Film"))

    if option == "Image":
        width = st.number_input("Width (pixels):", min_value=1)
        height = st.number_input("Height (pixels):", min_value=1)
        bits_per_pixel = st.number_input("Bits per pixel (e.g., 24 for RGB):", min_value=1)

        if st.button("Calculate Image Size"):
            size_mb = calculate_image_file_size(width, height, bits_per_pixel)
            st.success(f"Image file size: {size_mb:.2f} MB")

    elif option == "Video":
        bitrate_mbps = st.number_input("Bitrate (Mbps):", min_value=1.0)
        duration_seconds = st.number_input("Duration (seconds):", min_value=1)

        if st.button("Calculate Video Size"):
            size_mb = calculate_video_file_size(bitrate_mbps, duration_seconds)
            st.success(f"Video file size: {size_mb:.2f} MB")

    elif option == "Film":
        width = st.number_input("Width (pixels):", min_value=1)
        height = st.number_input("Height (pixels):", min_value=1)
        frames = st.number_input("Number of frames:", min_value=1)
        bits_per_pixel = st.number_input("Bits per pixel (e.g., 24 for RGB):", min_value=1)

        if st.button("Calculate Film Size"):
            size_gb = calculate_film_file_size(width, height, frames, bits_per_pixel)
            st.success(f"Film file size: {size_gb:.2f} GB")

    # ส่วนคำนวณมวลกายที่ไม่มีไขมัน
    st.header("Lean Body Mass and Calorie Needs Calculator")
    weight_kg = st.number_input("Weight (kg):", min_value=1.0)
    height_cm = st.number_input("Height (cm):", min_value=1.0)
    age = st.number_input("Age (years):", min_value=1)
    gender = st.selectbox("Gender:", ["Male", "Female"])
    activity_level = st.selectbox("Activity Level:", ["Sedentary", "Lightly Active", "Moderately Active", "Very Active", "Super Active"])

    if st.button("Calculate Lean Body Mass"):
        lbm = calculate_lean_body_mass(weight_kg, height_cm, gender)
        fat_mass = weight_kg - lbm
        fat_percentage = (fat_mass / weight_kg) * 100
        st.success(f"Lean Body Mass: {lbm:.2f} kg\nFat Mass: {fat_mass:.2f} kg\nBody Fat Percentage: {fat_percentage:.2f}%")

    if st.button("Calculate Calorie Needs"):
        daily_calories = calculate_calorie_needs(weight_kg, height_cm, age, gender, activity_level)
        st.success(f"Daily Calorie Needs: {daily_calories:.2f} kcal")

if __name__ == "__main__":
    main()
