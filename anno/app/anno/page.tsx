"use client"; 
import "@/app/globals.css";
import React, { useState, useEffect, AnyActionArg, use} from "react";
import { Button, Checkbox, Form, Typography, Row, Col, Card, Image, Radio, Space, message, Alert } from "antd";
import { UserOutlined } from '@ant-design/icons';
import appConfig from "@/appConfig";
import { useParams } from "react-router-dom";


const { Title, Text } = Typography;

const App = () => {
  const [selectedEmotions, setSelectedEmotions] = useState<string | null>(null);
  const [valence, setValence] = useState<number | null>(null);
  const [arousal, setArousal] = useState<number | null>(null);
  const [dominance, setDominance] = useState<number | null>(null);
  // const [currentImage, setCurrentImage] = useState("https://via.placeholder.com/512"); // Placeholder image
  const [currentImage, setCurrentImage] = useState("./demo.jpg"); // Placeholder image
  const [haveDoneNum, setHaveDoneNum] = useState(0);
  const [messageApi, contextHolder] = message.useMessage();
  const [showSuccess, setShowSuccess] = useState(false);


  const text_vad = {
    valence: "情感倾向",
    arousal: "情感激活",
    dominance: "情感控制"
  }

  const [userid, setUserid] = useState<string | null>(null);

  // const emotions = ["欢乐", "愤怒", "敬畏", "满足", "厌恶", "兴奋", "恐惧", "悲伤"];
  const emotions = ["厌恶或恶心", "恐惧或害怕", "愤怒或不满", "悲伤、难过、失落", "中性偏正向", "满足/惬意/舒适", "愉悦/开心", "激动/兴奋"];
  const emotions_cat = ["Disgust", "Fear", "Anger","Sad", "Awe",  "Contentment", "Amusement", "Excitement" ]
  const emotions_map_list = [
    {label: "厌恶或恶心", value: "Disgust"},
    {label: "恐惧或害怕", value: "Fear"},
    {label: "愤怒或不满", value: "Anger"},
    {label: "悲伤、难过、失落", value: "Sad"},
    {label: "中性偏正向", value: "Awe"},
    {label: "满足/惬意/舒适", value: "Contentment"},
    {label: "愉悦/开心", value: "Amusement"},
    {label: "激动/兴奋", value: "Excitement"}

    
  ]

  const iconColors = {
    "-4": "#0000CD",
    "-3": "#4169E1",
    "-2": "#4682B4",
    "-1": "#87CEFA",
    "0": "#D3D3D3",
    "1": "#FFB6C1",
    "2": "#FF69B4",
    "3": "#FF1493",
    "4": "#DB7093",
  };

  const emojiMap = {
    valence: {
      "-4": "😡",
      "-3": "😠",
      "-2": "😟",
      "-1": "😕",
      "0": "😐",
      "1": "🙂",
      "2": "😊",
      "3": "😀",
      "4": "😁",
    },
    arousal: Object.keys(iconColors).reduce((acc, key: any) => {
      acc[key] = <UserOutlined style={{ fontSize: "2rem", color: iconColors[key] }} />;
      return acc;
    }, {}),
    dominance: {
      "-4": "🙇",
      "-3": "🙇‍♂️",
      "-2": "🧍",
      "-1": "🧍‍♂️",
      "0": "🧍‍♀️",
      "1": "💪",
      "2": "🕴️",
      "3": "🕺",
      "4": "👑",
    },
  };

  const explanations = {
    valence: { left: "不开心", right: "开心" },
    arousal: { left: "平静", right: "活跃" },
    dominance: { left: "无法掌控", right: "掌控中" },
  };

  const handleEmotionChange = (checkedValues: any) => {
    setSelectedEmotions(checkedValues);
  };

  const handleVadChange = (name: any, value: any) => {
    console.log(name, value);
    switch (name) {
      case "valence":
        setValence(value);
        break;
      case "arousal":
        setArousal(value);
        break;
      case "dominance":
        setDominance(value);
        break;
    }
  }

  const [image, setImage] = useState<any | null>(null); // 当前图片数据
  const [loading, setLoading] = useState<boolean>(true); // 加载状态
  const [error, setError] = useState<string | null>(null); // 错误信息

  const handlePrevious = () => {
    console.log("上一张图片");
    alert("上一张图片");
  };

  const handleNext = () => {
    console.log("下一张图片");
    alert("下一张图片");
  };
  const handleAnnotate = async () => {
    const queryParams = new URLSearchParams(window.location.search);
    const id = queryParams.get("userid");
    console.log(JSON.stringify({
      user_id: id,
      img_name: image.image_path,
      emotion_categorical: selectedEmotions,
      valence: valence,
      arousal: arousal,
      dominance: dominance,
    }),)
    try {
      const response = await fetch(`${appConfig.baseURL}/annotate`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          user_id: id,
          img_name: image.image_path,
          emotion_categorical: selectedEmotions,
          valence: valence,
          arousal: arousal,
          dominance: dominance,
        }),
      });

      if (!response.ok) {
        throw new Error(`Error: ${response.status}`);
      }

      const data = await response.json();
      console.log("Annotation saved:", data);

      setShowSuccess(true);
      setTimeout(() => {
        setShowSuccess(false);
      }, 2000);
      fetchImage();
      fetchHaveDoneNum();

    } catch (err: any) {
      console.error("Failed to save annotation:", err);
      alert("保存标注失败！");
    }
  };

  const handleSave = () => {
    console.log("保存标注:", {
      image: currentImage,
      emotions: selectedEmotions,
      valence: valence,
      arousal: arousal,
      dominance: dominance,
    });
    handleAnnotate();
  };
  const fetchImage = async () => {
    try {
      setLoading(true); // 开始加载
      const queryParams = new URLSearchParams(window.location.search);
      const id = queryParams.get("userid");
      setUserid(id);
      const response = await fetch(`${appConfig.baseURL}/fetch_image/${id}`);

      if (!response.ok) {
        throw new Error(`Error: ${response.status}`);
      }

      const data = await response.json();
      console.log(data);

      if (data.message) {
        setImage(null); // 所有图片已标注完成
        setError(data.message);
      } else {
        setImage(data.image); // 设置当前图片
        setSelectedEmotions(data.image.emotion_categorical); // 设置当前图片的情绪标注
        
        setValence(data.image.valence); // 设置当前图片的情绪标注
        setArousal(data.image.arousal); // 设置当前图片的情绪标注
        setDominance(data.image.dominance); // 设置当前图片的情绪标注



        setError(null); // 清空错误信息
      }
    } catch (err: any) {
      setError(err.message || "Failed to fetch image");
    } finally {
      setLoading(false); // 加载结束
    }
  };

  const fetchHaveDoneNum = async () => {
    try {
      const queryParams = new URLSearchParams(window.location.search);
      const id = queryParams.get("userid");
      const response = await fetch(`${appConfig.baseURL}/remaining_images/${id}`);

      if (!response.ok) {
        throw new Error(`Error: ${response.status}`);
      }

      const data = await response.json();
      console.log(data);
      setHaveDoneNum(data.remaining_images);
    } catch (err: any) {
      console.error("Failed to fetch have done num:", err);
    }
  }

  // 在组件加载时调用 fetchImage
  useEffect(() => {
    fetchImage();
    fetchHaveDoneNum();
  }, []);

  function get_image_path(img_path: any) {
    const img_id = img_path.split("/").pop()
    // http://localhost:8000/image/1.jpg
    return `${appConfig.baseURL}/images/${img_id}`
  }

  function getDValue(dimension: any) {
    switch (dimension) {
      case "valence":
        return valence;
      case "arousal":
        return arousal;
      case "dominance":
        return dominance;
  }}
  

  return (
    <>
    <header
      style={{
        textAlign: "center",
        padding: "1rem",
        backgroundColor: "#f8f8f8",
        borderBottom: "1px solid #ddd",
      }}
    >
      <h1
        style={{
          margin: 0,
          fontSize: "2rem",
          color: "#333",
          fontFamily: "sans-serif",
        }}
      >
        EmoGenDB 图片标注
      </h1>
      <h2
        style={{
          margin: "0.5rem 0",
          fontSize: "1.2rem",
          color: "#555",
          fontWeight: 400,
        }}
      >
        用户：{userid}
      </h2>
      <h2
        style={{
          margin: 0,
          fontSize: "1.2rem",
          color: "#555",
          fontWeight: 400,
        }}
      >
        剩余{haveDoneNum}张图片
      </h2>
    </header>
    
    <Row
      gutter={[16, 16]}
      className="p-5 justify-center" // Tailwind: padding = 1.25rem, 水平居中
    >
      {/* 图片部分 */}
      <Col
        xs={24}
        sm={24}
        md={8}
        className="flex justify-center" // 在小屏时占满，md 及以上宽度时为 8 栅格; 图片部分水平居中
      >
        <Card
          bordered={false}
          className="inline-block w-[512px] h-[512px]" // 这里示例强制大小，你也可改为更灵活的 Tailwind 样式
        >
          <Image
            src={image && get_image_path(image.image_path)}
            alt="当前图片"
            className="max-w-full h-auto"
          />
          <Text
            className="text-left block mt-6 text-base" // Tailwind: text-left, block, margin-top=1.5rem, 字号base=16px
          >
            {image && image.caption}
          </Text>
        </Card>
      </Col>

      {/* 标注部分 */}
      <Col xs={24} sm={24} md={16}>
        <Card title="情绪标注" bordered={false}>
          {showSuccess && (
            <Alert
              className="mt-4"
              message="标注成功"
              type="success"
              showIcon
            />
          )}

          <Form layout="vertical">
            {/* 情绪选择 */}
            <Form.Item label="选择情绪" name="emotions">
              {selectedEmotions && (
                <Text className="hidden font-bold">
                  已选择：{selectedEmotions}
                </Text>
              )}
              <Radio.Group
                value={selectedEmotions}
                onChange={(e) => setSelectedEmotions(e.target.value)}
                buttonStyle="solid"
              >
                {emotions_map_list.map((emotion) => (
                  <Radio.Button value={emotion.value} key={emotion.value}>
                    {emotion.label}
                  </Radio.Button>
                ))}
              </Radio.Group>
            </Form.Item>

            {/* VAD 标注 */}
            <Title level={5} className="mb-2">
              VAD 标注
            </Title>

            {/* Valence */}
            <Space className="flex items-center mb-4">
              <Text strong className="mr-2">
                {explanations["valence"].left}
              </Text>
              <Radio.Group
                options={Array.from({ length: 9 }, (_, i) => i - 4).map(
                  (value) => ({
                    label: (
                      <div className="text-center">
                        <span className="block text-2xl leading-8">
                          {emojiMap["valence"][value] || (
                            <UserOutlined
                              style={{ color: iconColors[value], fontSize: "2rem" }}
                            />
                          )}
                        </span>
                        <Text className="block font-bold">{value}</Text>
                      </div>
                    ),
                    value,
                  })
                )}
                value={valence}
                onChange={(e) => handleVadChange("valence", e.target.value)}
                optionType="button"
                buttonStyle="solid"
              />
              <Text strong className="ml-2">
                {explanations["valence"].right}
              </Text>
            </Space>

            {/* Arousal */}
            <Space className="flex items-center mb-4">
              <Text strong className="mr-2">
                {explanations["arousal"].left}
              </Text>
              <Radio.Group
                options={Array.from({ length: 9 }, (_, i) => i - 4).map(
                  (value) => ({
                    label: (
                      <div className="text-center">
                        <span className="block text-2xl leading-8">
                          {emojiMap["arousal"][value] || (
                            <UserOutlined
                              style={{ color: iconColors[value], fontSize: "2rem" }}
                            />
                          )}
                        </span>
                        <Text className="block font-bold">{value}</Text>
                      </div>
                    ),
                    value,
                  })
                )}
                value={arousal}
                onChange={(e) => handleVadChange("arousal", e.target.value)}
                optionType="button"
                buttonStyle="solid"
              />
              <Text strong className="ml-2">
                {explanations["arousal"].right}
              </Text>
            </Space>

            {/* Dominance */}
            <Space className="flex items-center mb-4">
              <Text strong className="mr-2">
                {explanations["dominance"].left}
              </Text>
              <Radio.Group
                options={Array.from({ length: 9 }, (_, i) => i - 4).map(
                  (value) => ({
                    label: (
                      <div className="text-center">
                        <span className="block text-2xl leading-8">
                          {emojiMap["dominance"][value] || (
                            <UserOutlined
                              style={{ color: iconColors[value], fontSize: "2rem" }}
                            />
                          )}
                        </span>
                        <Text className="block font-bold">{value}</Text>
                      </div>
                    ),
                    value,
                  })
                )}
                value={dominance}
                onChange={(e) => handleVadChange("dominance", e.target.value)}
                optionType="button"
                buttonStyle="solid"
              />
              <Text strong className="ml-2">
                {explanations["dominance"].right}
              </Text>
            </Space>
          </Form>
        </Card>

        {/* 操作按钮 */}
        <div className="mt-5">
          {/* <Button onClick={handlePrevious} size="large">上一张</Button> */}
          <button onClick={handleSave} style={{
                padding: "16px 50px", // 增大按钮的内边距
                fontSize: "18px", // 增大字体大小
                backgroundColor:  "#28a745", // 悬停时变为绿色，否则为蓝色
                color: "white", // 字体颜色为白色
                border: "none", // 无边框
                borderRadius: "8px", // 圆角
                cursor: "pointer", // 鼠标指针为手型
                transition: "background-color 0.3s ease", // 平滑过渡效果
              }} className="mybtn">
            保存
          </button>
          {/* <Button onClick={handleNext} size="large">下一张</Button> */}
        </div>
      </Col>
    </Row>
    </>
  );
};

export default App;
