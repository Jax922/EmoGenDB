"use client"; 

import React, { useState } from "react";
import { Button, Checkbox, Form, Typography, Row, Col, Card, Image, Radio, Space} from "antd";
import { UserOutlined } from '@ant-design/icons';

const { Title, Text } = Typography;

const App = () => {
  const [selectedEmotions, setSelectedEmotions] = useState([]);
  const [vadValues, setVadValues] = useState({ valence: 0, arousal: 0, dominance: 0 });
  // const [currentImage, setCurrentImage] = useState("https://via.placeholder.com/512"); // Placeholder image
  const [currentImage, setCurrentImage] = useState("./demo.jpg"); // Placeholder image

  const text_vad = {
    valence: "情感倾向",
    arousal: "情感激活",
    dominance: "情感控制"
  }


  const emotions = ["欢乐", "愤怒", "敬畏", "满足", "厌恶", "兴奋", "恐惧", "悲伤"];

  const handleEmotionChange = (checkedValues) => {
    setSelectedEmotions(checkedValues);
  };

  const handleVadChange = (name, value) => {
    setVadValues({ ...vadValues, [name]: value });
  };

  const vadOptions = (dimension) => {
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
      arousal: Object.keys(iconColors).reduce((acc, key) => {
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

    return (
      <div>
        <Space style={{ display: "flex", alignItems: "center", marginBottom: 10 }}>
          <Text strong style={{ flex: "0 0 auto", textAlign: "left", marginRight: 5 }}>{explanations[dimension].left}</Text>
          <Radio.Group
            options={Array.from({ length: 9 }, (_, i) => i - 4).map((value) => ({
              label: (
                <div style={{ textAlign: "center" }}>
                  <span style={{ display: "block", fontSize: "2rem", lineHeight: "2rem" }}>
                    {emojiMap[dimension][value] || <UserOutlined style={{ color: iconColors[value], fontSize: "2rem" }} />}
                  </span>
                  <Text style={{ display: "block", fontWeight: "bold" }}>{value}</Text>
                </div>
              ),
              value,
            }))}
            value={vadValues[dimension]}
            onChange={(e) => handleVadChange(dimension, e.target.value)}
            optionType="button"
            buttonStyle="solid"
          />
          <Text strong style={{ flex: "0 0 auto", textAlign: "right", marginLeft: 5 }}>{explanations[dimension].right}</Text>
        </Space>
      </div>
    );
  };

  const handlePrevious = () => {
    console.log("上一张图片");
    alert("上一张图片");
  };

  const handleNext = () => {
    console.log("下一张图片");
    alert("下一张图片");
  };

  const handleSave = () => {
    console.log("保存标注:", {
      image: currentImage,
      emotions: selectedEmotions,
      vad: vadValues,
    });
    alert("标注已保存！");
  };

  return (
    <Row gutter={16} style={{ padding: 20 }}>
      {/* 图片部分 */}
      <Col span={8} style={{ textAlign: "center" }}>
        <Card bordered={false} style={{ display: "inline-block", width: "512px", height: "512px" }}>
          <Image src={currentImage} alt="当前图片" style={{ maxWidth: "100%", height: "auto" }} />
          <Text style={{textAlign:"left", display: "block", marginTop: "25px", fontSize: "16px" }}>
            超级马里奥悠闲地坐在一张复古设计的椅子上，在昏暗的环境中散发着愉快的气息。
          </Text>
        </Card>
      </Col>

      {/* 标注部分 */}
      <Col span={16}>
        <Card title="情绪标注" bordered={false}>
          <Form layout="vertical">
            {/* 情绪选择 */}
            <Form.Item label="选择情绪" name="emotions">
              <Checkbox.Group
                options={emotions.map((emotion) => ({ label: emotion, value: emotion }))}
                value={selectedEmotions}
                onChange={handleEmotionChange}
              />
            </Form.Item>

            {/* VAD 标注 */}
            <Title level={5} style={{ marginBottom: 10 }}>VAD 标注</Title>
            {Object.keys(text_vad).map((dimension) => (
              <Form.Item label={text_vad[dimension]} key={dimension}>
                {vadOptions(dimension)}
              </Form.Item>
            ))}
            <Space style={{ marginTop: 20, display: 'flex', justifyContent: 'center' }}>
              <Button onClick={handlePrevious}>上一张</Button>
              <Button onClick={handleSave} type="primary">保存</Button>
              <Button onClick={handleNext}>下一张</Button>
            </Space>
          </Form>
        </Card>
      </Col>
    </Row>
  );
};

export default App;
