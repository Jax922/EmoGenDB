"use client"; 

import React, { useState } from "react";
import { Button, Checkbox, Form, Typography, Row, Col, Card, Image, Radio, Space } from "antd";
import { UserOutlined } from '@ant-design/icons';

const { Title, Text } = Typography;

const App = () => {
  const [selectedEmotions, setSelectedEmotions] = useState([]);
  const [vadValues, setVadValues] = useState({ valence: 0, arousal: 0, dominance: 0 });
  const [currentImage, setCurrentImage] = useState("https://via.placeholder.com/512"); // Placeholder image

  const emotions = ["Amusement", "Anger", "Awe", "Contentment", "Disgust", "Excitement", "Fear", "Sad"];

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
      valence: { left: "Unhappy", right: "Happy" },
      arousal: { left: "Calm", right: "Active" },
      dominance: { left: "Uncontrollable", right: "In control" },
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
    console.log("Previous Image");
    alert("Previous Image");
  };

  const handleNext = () => {
    console.log("Next Image");
    alert("Next Image");
  };

  const handleSave = () => {
    console.log("Save Current Annotations:", {
      image: currentImage,
      emotions: selectedEmotions,
      vad: vadValues,
    });
    alert("Annotations Saved!");
  };

  return (
    <Row gutter={16} style={{ padding: 20 }}>
      {/* Image Section */}
      <Col span={8} style={{ textAlign: "center" }}>
        <Card bordered={false} style={{ display: "inline-block", width: "512px", height: "512px" }}>
          <Image src={currentImage} alt="Current" style={{ maxWidth: "100%", height: "auto" }} />
        </Card>
      </Col>

      {/* Annotation Section */}
      <Col span={16}>
        <Card title="Emotion Annotation" bordered={false}>
          <Form layout="vertical">
            {/* Emotion Selection */}
            <Form.Item label="Select Emotions" name="emotions">
              <Checkbox.Group
                options={emotions.map((emotion) => ({ label: emotion, value: emotion }))}
                value={selectedEmotions}
                onChange={handleEmotionChange}
              />
            </Form.Item>

            {/* VAD Annotation */}
            <Title level={5} style={{ marginBottom: 10 }}>VAD Annotation</Title>
            {Object.keys(vadValues).map((dimension) => (
              <Form.Item label={dimension.charAt(0).toUpperCase() + dimension.slice(1)} key={dimension}>
                {vadOptions(dimension)}
              </Form.Item>
            ))}
            <Space style={{ marginTop: 20, display: 'flex', justifyContent: 'center' }}>
              <Button onClick={handlePrevious}>Previous</Button>
              <Button onClick={handleSave} type="primary">Save</Button>
              <Button onClick={handleNext}>Next</Button>
            </Space>
          </Form>
        </Card>
      </Col>
    </Row>
  );
};

export default App;




