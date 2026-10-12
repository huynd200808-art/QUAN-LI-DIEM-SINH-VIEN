import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st

# Cấu hình trang
st.set_page_config(
    page_title="Quản Lý Điểm Sinh Viên", page_icon="🎓", layout="wide"
)

# 1. Hiển thị tiêu đề
st.title("QUẢN LÝ ĐIỂM SINH VIÊN-")
st.markdown("---")

# Dữ liệu 10 sinh viên
data = {
    "Họ tên": [
        " Nguyen Van A",
        " Nguyen Van b",
        " Nguyen Van c",
        " Nguyen Van d",
        " Nguyen Van e",
        " Nguyen Van h",
        " Nguyen Van f",
        " Nguyen Van g",
        " Nguyen Van s",
        " Nguyen Van y",
    ],
    "Chuyên cần": [8.0, 7.0, 6.0, 9.0, 9.0, 7.0, 5.0, 8.0, 6.0, 10.0],
    "Giữa kỳ": [7.0, 8.0, 8.0, 7.0, 9.0, 8.0, 6.0, 6.0, 7.0, 8.0],
    "Cuối kỳ": [8.0, 7.0, 7.0, 8.0, 8.0, 6.0, 6.0, 7.0, 7.0, 9.0],
}

df = pd.DataFrame(data)

# Tính điểm tổng kết: 20% Chuyên cần + 30% Giữa kỳ + 50% Cuối kỳ
df["Tổng kết"] = (
    0.2 * df["Chuyên cần"] + 0.3 * df["Giữa kỳ"] + 0.5 * df["Cuối kỳ"]
)

# Xếp loại sinh viên
conditions = [
    (df["Tổng kết"] >= 8.5),
    (df["Tổng kết"] >= 7.0) & (df["Tổng kết"] < 8.5),
    (df["Tổng kết"] >= 5.0) & (df["Tổng kết"] < 7.0),
    (df["Tổng kết"] < 5.0),
]
choices = ["Giỏi", "Khá", "Trung bình", "Yếu"]
df["Xếp loại"] = np.select(conditions, choices, default="Yếu")

# Làm tròn điểm
df[["Chuyên cần", "Giữa kỳ", "Cuối kỳ", "Tổng kết"]] = df[
    ["Chuyên cần", "Giữa kỳ", "Cuối kỳ", "Tổng kết"]
].round(2)

# 2. Hiển thị bảng điểm 10 sinh viên
st.subheader("📋 Bảng điểm danh sách sinh viên")
st.dataframe(df, use_container_width=True)

st.markdown("---")

# 3, 4, 5. Thống kê
st.subheader("📊 Thống kê tổng quan")

avg_score = df["Tổng kết"].mean()
max_student = df.loc[df["Tổng kết"].idxmax()]
min_student = df.loc[df["Tổng kết"].idxmin()]
passed_count = (df["Tổng kết"] >= 5.0).sum()

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric(label="Điểm trung bình lớp", value=f"{avg_score:.2f}")
with col2:
    st.metric(
        label="Điểm cao nhất",
        value=f"{max_student['Tổng kết']}",
        delta=max_student["Họ tên"],
    )
with col3:
    st.metric(
        label="Điểm thấp nhất",
        value=f"{min_student['Tổng kết']}",
        delta=min_student["Họ tên"],
        delta_color="inverse",
    )
with col4:
    st.metric(label="Số sinh viên đạt (>=5.0)", value=f"{passed_count}/10")

st.markdown("---")

# 6, 7. Selectbox chọn sinh viên và hiển thị chi tiết
st.subheader("🔍 Tra cứu sinh viên")
selected_student = st.selectbox(
    "Chọn sinh viên cần xem:", df["Họ tên"].tolist()
)

if selected_student:
    info = df[df["Họ tên"] == selected_student].iloc[0]
    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Chuyên cần", info["Chuyên cần"])
    c2.metric("Giữa kỳ", info["Giữa kỳ"])
    c3.metric("Cuối kỳ", info["Cuối kỳ"])
    c4.metric("Tổng kết", info["Tổng kết"])
    c5.metric("Xếp loại", info["Xếp loại"])

st.markdown("---")

# 8. Hiển thị biểu đồ cột điểm tổng kết
st.subheader("📈 Biểu đồ điểm tổng kết của 10 sinh viên")

fig, ax = plt.subplots(figsize=(10, 5))
bars = ax.barh(df["Họ tên"], df["Tổng kết"], color="#4C72B0")
ax.set_xlabel("Điểm tổng kết", fontsize=12)
ax.set_ylabel("Họ tên sinh viên", fontsize=12)
ax.set_title(
    "Biểu đồ điểm tổng kết của 10 sinh viên", fontsize=14, fontweight="bold"
)
ax.set_xlim(0, 10)
ax.grid(axis="x", linestyle="--", alpha=0.5)
ax.invert_yaxis()

for bar in bars:
    width = bar.get_width()
    ax.text(
        width + 0.1,
        bar.get_y() + bar.get_height() / 2,
        f"{width:.2f}",
        va="center",
        ha="left",
    )

st.pyplot(fig)

st.markdown("---")

# 9. Họ tên và MSSV ở cuối trang với chữ nhỏ
st.markdown(
    "<div style='text-align: center; color: gray; font-size: 13px;'>"
    "Người thực hiện: Nguyễn Đức Huy — MSSV: [051208002157]"
    "</div>",
    unsafe_allow_html=True,
)
