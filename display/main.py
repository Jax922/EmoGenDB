import streamlit as st
import pandas as pd

# 加载数据并缓存
@st.cache_data
def load_data(csv_path):
    df = pd.read_csv(csv_path)
    # 替换 image_path 开头路径
    # df["image_path"] = df["image_path"].str.replace(
    #     "/home/pci/dong",
    #     "/home/pci/dong/emodb/dong",
    #     regex=False
    # )
    return df

csv_path = "/home/pci/dong/emodb/dong/AIGC-image/MJ/all_cleaned_vicuna7b_balanced25.csv"
df = load_data(csv_path)

# 添加标题
st.title("AIGC Image Viewer")

# 搜索功能
keyword = st.text_input("Search by Caption or ANP", "")
if keyword:
    filtered_df = df[
        df["Caption"].str.contains(keyword, na=False, case=False) |
        df["ANP"].str.contains(keyword, na=False, case=False) |
        df["image_path"].str.contains(keyword, na=False, case=False)
    ]
else:
    filtered_df = df

# 分类选项
emotions = ["All"] + list(df["Emotion_Categorical"].unique())
selected_emotion = st.selectbox("Select Emotion Category", options=emotions)
if selected_emotion != "All":
    filtered_df = filtered_df[filtered_df["Emotion_Categorical"] == selected_emotion]

# 滚动加载状态
if "loaded_rows" not in st.session_state:
    st.session_state.loaded_rows = 20  # 初始加载 20 张图片

# 当前加载的图片
current_df = filtered_df.iloc[:st.session_state.loaded_rows]

# 使用 `st.columns` 实现图片平铺布局和 `st.image`
cols_per_row = 4  # 每行列数
rows = [current_df.iloc[i:i + cols_per_row] for i in range(0, len(current_df), cols_per_row)]  # 切分行

for row in rows:
    cols = st.columns(cols_per_row)
    for idx, (_, data) in enumerate(row.iterrows()):
        with cols[idx]:
            with st.container():
                # 使用 st.image 展示图片
                st.image(data["image_path"], caption=data["Caption"], use_container_width=True)
                st.markdown(f"""
                    **Emotion**: {data['Emotion_Categorical']}  
                    **ANP**: {data['ANP']}  
                    **Reason**: {data['Reason_for_Emotion']}
                """)

# 加载更多按钮
if st.session_state.loaded_rows < len(filtered_df):
    if st.button("Load More"):
        st.session_state.loaded_rows += 20  # 每次加载更多 20 张图片
else:
    st.write("No more images to load.")