import React, { useState } from "react";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  AreaChart,
  Radar,
  PolarRadiusAxis,
  PolarAngleAxis,
  PolarGrid,
  RadarChart,
  Area,
} from "recharts";

import getRadarData from "./helpers/radarData";
import { getTimelineData } from "./helpers/timelineData";

const BarChartComponent = ({ xlabel, ylabel, title, data }) => {
  return (
    <ResponsiveContainer width="100%" height={400}>
      <BarChart
        data={data}
        margin={{
          top: 20,
          right: 30,
          left: 20,
          bottom: 5,
        }}
      >
        <defs>
          <linearGradient id="colorUv" x1="0" y1="0" x2="0" y2="1">
            <stop offset="0%" stopColor="#6495CE" stopOpacity={1} />
            <stop offset="10%" stopColor="#20519F" stopOpacity={1} />
            <stop offset="100%" stopColor="#20519F" stopOpacity={1} />
          </linearGradient>
          <linearGradient id="colorPv" x1="0" y1="0" x2="0" y2="1">
            <stop offset="0%" stopColor="#C58FA2" stopOpacity={1} />
            <stop offset="10%" stopColor="#A8D9FD" stopOpacity={1} />
            <stop offset="90%" stopColor="#A8D9FD" stopOpacity={1} />
            <stop offset="100%" stopColor="#6495CE" stopOpacity={1} />
          </linearGradient>
          <linearGradient id="colorAmt" x1="0" y1="0" x2="0" y2="1">
            <stop offset="90%" stopColor="#e14547" stopOpacity={1} />
            <stop offset="100%" stopColor="#C58FA2" stopOpacity={1} />
          </linearGradient>
          {/* <linearGradient id="colorUv" x1="0" y1="0" x2="0" y2="1">
            <stop offset="50%" stopColor="#20519F" stopOpacity={1} />
            <stop offset="100%" stopColor="#20519F" stopOpacity={0.2} />
          </linearGradient>
          <linearGradient id="colorPv" x1="0" y1="0" x2="0" y2="1">
            <stop offset="50%" stopColor="#A8D9FD" stopOpacity={1} />
            <stop offset="100%" stopColor="#A8D9FD" stopOpacity={0.2} />
          </linearGradient>
          <linearGradient id="colorAmt" x1="0" y1="0" x2="0" y2="1">
            <stop offset="50%" stopColor="#e14547" stopOpacity={1} />
            <stop offset="100%" stopColor="#e14547" stopOpacity={0.2} />
          </linearGradient> */}
        </defs>
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis
          dataKey="name"
          label={{ value: xlabel, position: "insideBottomRight", offset: 0 }}
        />
        <YAxis
          // scale="log"
          // domain={["auto", "auto"]}
          label={{ value: ylabel, angle: -90, position: "insideLeft" }}
        />
        <Tooltip />
        <Legend />
        <Bar dataKey="positive" fill="url(#colorUv)" stackId="a" />
        <Bar dataKey="neutral" fill="url(#colorPv)" stackId="a" />
        <Bar dataKey="negative" fill="url(#colorAmt)" stackId="a" />
      </BarChart>
    </ResponsiveContainer>
  );
};

const AreaChartComponent = ({ xlabel, ylabel, title, data }) => {
  return (
    <ResponsiveContainer width="100%" height={400}>
      <AreaChart
        data={data}
        margin={{
          top: 20,
          right: 30,
          left: 20,
          bottom: 5,
        }}
      >
        <defs>
          <linearGradient id="color1" x1="0" y1="0" x2="0" y2="1">
            <stop offset="5%" stopColor="#20519F" stopOpacity={0.8} />
            <stop offset="95%" stopColor="#20519F" stopOpacity={0} />
          </linearGradient>
          <linearGradient id="color2" x1="0" y1="0" x2="0" y2="1">
            <stop offset="5%" stopColor="#e14547" stopOpacity={0.8} />
            <stop offset="95%" stopColor="#e14547" stopOpacity={0} />
          </linearGradient>
          <linearGradient id="color3" x1="0" y1="0" x2="0" y2="1">
            <stop offset="5%" stopColor="#A8D9FD" stopOpacity={0.8} />
            <stop offset="95%" stopColor="#A8D9FD" stopOpacity={0} />
          </linearGradient>
        </defs>
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis
          dataKey="name"
          label={{ value: xlabel, position: "insideBottomRight", offset: 0 }}
        />
        <YAxis
          // scale="log"
          // domain={["auto", "auto"]}
          label={{ value: ylabel, angle: -90, position: "insideLeft" }}
        />
        <Tooltip />
        <Legend />
        <Area
          type="monotone"
          dataKey="positive"
          stroke="#20519F"
          fill="url(#color1)"
        />
        <Area
          type="monotone"
          dataKey="negative"
          stroke="#e14547"
          fill="url(#color2)"
        />
        <Area
          type="monotone"
          dataKey="neutral"
          stroke="#A8D9FD"
          fill="url(#color3)"
        />
      </AreaChart>
    </ResponsiveContainer>
  );
};

const RadarChartComponent = ({ data }) => {
  return (
    <ResponsiveContainer width="100%" height={400}>
      <RadarChart cx="50%" cy="50%" outerRadius="80%" data={data}>
        <PolarGrid />
        <PolarAngleAxis dataKey="subject" fontSize={26} />
        <PolarRadiusAxis />
        {/* <Radar
          name="Neutrality"
          dataKey="neutral"
          stroke="#A8D9FD"
          fill="#A8D9FD"
          fillOpacity={0.6}
        /> */}
        <Radar
          name="Positivity"
          dataKey="positive"
          stroke="#20519F"
          fill="#20519F"
          fillOpacity={0.6}
        />
        <Radar
          name="Negativity"
          dataKey="negative"
          stroke="#e14547"
          fill="#e14547"
          fillOpacity={0.6}
        />
        <Tooltip />
        <Legend iconSize={15} />
      </RadarChart>
    </ResponsiveContainer>
  );
};

const athletes_colors = {
  sylla: "#8884d8",
  orro: "#82ca9d",
  egonu: "#ffc658",
  danesi: "#ff7300",
  larson: "#ff0000",
};

const SingleRadarChartComponent = ({ data }) => {
  const invertedData = ["positive", "negative", "neutral"].map((key) => {
    const item = {
      subject: key,
    };
    for (const value of data) {
      item[value.subject] = value[key];
    }
    return item;
  });

  const [names, setNames] = React.useState([data[0].subject]);

  return (
    <div style={{ width: "100%" }}>
      <select
        value={names}
        onChange={(e) =>
          setNames(
            Array.from(e.target.selectedOptions, (option) => option.value)
          )
        }
        style={{ width: "100%", fontSize: 26 }}
        multiple={true}
      >
        {data.map((item) => (
          <option key={item.subject} value={item.subject}>
            {item.subject}
          </option>
        ))}
      </select>
      <ResponsiveContainer width="100%" height={400}>
        <RadarChart cx="50%" cy="50%" outerRadius="80%" data={invertedData}>
          <PolarGrid />
          <PolarAngleAxis dataKey="subject" fontSize={26} />
          <PolarRadiusAxis />

          {names.map((name) => (
            <Radar
              key={name}
              name={name}
              dataKey={name}
              stroke={athletes_colors[name]}
              fill={athletes_colors[name]}
              fillOpacity={0.6}
            />
          ))}

          <Tooltip />
          <Legend iconSize={15} />
        </RadarChart>
      </ResponsiveContainer>
    </div>
  );
};

const App = () => {
  const [year, setYear] = useState(2024);

  const availablePlatforms = [
    { name: "Facebook", key: "FB" },
    { name: "Instagram", key: "IG" },
    { name: "Blogs", key: "Web" },
  ];

  const [platforms, setPlatforms] = useState(
    Object.values(availablePlatforms).map((p) => p.key)
  );

  const timelineDataPosts = getTimelineData(year, platforms);
  const timelineDataComments = getTimelineData(year, platforms, true);
  const radarData = getRadarData();

  return (
    <div>
      <div style={{ display: "flex", width: "100%", margin: "auto" }}>
        <select
          value={year}
          onChange={(e) => setYear(e.target.value)}
          style={{ width: "100%", fontSize: 26 }}
        >
          <option value={2024}>2024</option>
          <option value={2023}>2023</option>
          <option value={2022}>2022</option>
          <option value={2021}>2021</option>
        </select>
        <select
          value={platforms}
          onChange={(e) =>
            setPlatforms(
              Array.from(e.target.selectedOptions, (option) => option.value)
            )
          }
          style={{ width: "100%", fontSize: 26 }}
          multiple={true}
        >
          {availablePlatforms.map((p) => (
            <option key={p.key} value={p.key}>
              {p.name}
            </option>
          ))}
        </select>
      </div>
      <h1>Sentiment Comments Graph</h1>
      <div style={{ display: "flex", width: "100%" }}>
        <div style={{ width: "50%" }}>
          <BarChartComponent
            xlabel="Month"
            ylabel="Comments"
            title="Sample Bar Chart"
            data={timelineDataComments}
          />
        </div>
        <div style={{ width: "50%" }}>
          <AreaChartComponent
            xlabel="Months"
            ylabel="Comments"
            title="Sample Bar Chart"
            data={timelineDataComments}
          />
        </div>
      </div>
      <h1>Posts Comments Graph</h1>
      <div style={{ display: "flex", width: "100%" }}>
        <div style={{ width: "50%" }}>
          <BarChartComponent
            xlabel="Month"
            ylabel="Posts"
            title="Sample Bar Chart"
            data={timelineDataPosts}
          />
        </div>
        <div style={{ width: "50%" }}>
          <AreaChartComponent
            xlabel="Months"
            ylabel="Posts"
            title="Sample Bar Chart"
            data={timelineDataPosts}
          />
        </div>
      </div>

      <div style={{ display: "flex", width: "60%", margin: "auto" }}>
        <RadarChartComponent data={radarData} />
        <SingleRadarChartComponent
          data={radarData}
          name={radarData[0].subject}
        />
      </div>
    </div>
  );
};

export default App;
