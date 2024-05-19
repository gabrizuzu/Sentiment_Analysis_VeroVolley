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
import Downloader from "./components/downloader";

const BarChartComponent = ({
  ylabel,
  data,
  graphRef,
  height = 400,
  width = "100%",
}) => {
  return (
    <div style={{ border: "1px solid black", width, height }}>
      <ResponsiveContainer width="100%" height="100%">
        <BarChart
          ref={graphRef}
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
              <stop offset="100%" stopColor="#20519F" stopOpacity={0.8} />
            </linearGradient>
            <linearGradient id="colorPv" x1="0" y1="0" x2="0" y2="1">
              <stop offset="0%" stopColor="#C58FA2" stopOpacity={1} />
              <stop offset="10%" stopColor="#A8D9FD" stopOpacity={1} />
              <stop offset="50%" stopColor="#A8D9FD" stopOpacity={0.7} />
              <stop offset="90%" stopColor="#A8D9FD" stopOpacity={1} />
              <stop offset="100%" stopColor="#6495CE" stopOpacity={1} />
            </linearGradient>
            <linearGradient id="colorAmt" x1="0" y1="0" x2="0" y2="1">
              <stop offset="0%" stopColor="#e14547" stopOpacity={0.8} />
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
          <CartesianGrid vertical={false} strokeDasharray="3 3" />
          <XAxis dataKey="month" />
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
    </div>
  );
};

const AreaChartComponent = ({
  ylabel,
  data,
  graphRef,
  height = 400,
  width = "100%",
}) => {
  return (
    <div style={{ border: "1px solid black", width, height }}>
      <ResponsiveContainer width="100%" height="100%">
        <AreaChart
          ref={graphRef}
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
          <XAxis dataKey="month" />
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
    </div>
  );
};

const RadarChartComponent = ({
  data,
  graphRef,
  height = 400,
  width = "100%",
}) => {
  return (
    <div style={{ border: "1px solid black", width, height }}>
      <ResponsiveContainer width="100%" height="100%">
        <RadarChart
          ref={graphRef}
          cx="50%"
          cy="50%"
          outerRadius="80%"
          data={data}
        >
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
    </div>
  );
};

const athletes_colors = {
  sylla: "#8884d8",
  orro: "#82ca9d",
  egonu: "#ffc658",
  danesi: "#ff7300",
  larson: "#ff0000",
};

const SingleRadarChartComponent = ({
  data,
  graphRef,
  height = 400,
  width = "100%",
}) => {
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
    <>
      <div style={{ display: "flex", width: "100%", justifyContent: "center" }}>
        <div style={{ border: "1px solid black", width, height }}>
          <ResponsiveContainer width="100%" height="100%">
            <RadarChart
              cx="50%"
              cy="50%"
              outerRadius="80%"
              data={invertedData}
              ref={graphRef}
            >
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
      </div>
      <select
        value={names}
        onChange={(e) =>
          setNames(
            Array.from(e.target.selectedOptions, (option) => option.value)
          )
        }
        style={{
          width: "600px",
          height: "50px",
          fontSize: 26,
        }}
        multiple={true}
        size={1}
      >
        {data.map((item) => (
          <option
            key={item.subject}
            value={item.subject}
            style={{
              color: athletes_colors[item.subject],
              display: "inline-block",
              width: 100,
              textAlign: "center",
            }}
          >
            {item.subject}
          </option>
        ))}
      </select>
    </>
  );
};

const App = () => {
  const availablePlatforms = [
    { name: "Facebook", key: "FB" },
    { name: "Instagram", key: "IG" },
    { name: "Blogs", key: "Web" },
  ];
  const availableSeasons = ["2023/2024", "2022/2023", "2021/2022", "2020/2021"];

  const [season, setSeasons] = useState(availableSeasons[0]);
  const [platforms, setPlatforms] = useState(
    Object.values(availablePlatforms).map((p) => p.key)
  );
  const [usePostsTimeline, setUsePostsTimeline] = useState(true);
  const [usePostsRadar, setUsePostsRadar] = useState(true);

  const timelineDataPosts = getTimelineData(season, platforms);
  const timelineDataComments = getTimelineData(season, platforms, true);
  const radarData = getRadarData(usePostsRadar);

  return (
    <div>
      <div style={{ display: "flex", gap: 20 }}>
        <h1>{usePostsTimeline ? "Posts" : "Comments"} Sentiment Timelines</h1>
        <div
          style={{
            display: "flex",
            alignItems: "center",
          }}
        >
          <button onClick={() => setUsePostsTimeline(!usePostsTimeline)}>
            {usePostsTimeline ? "Change To Comments" : "Change To Posts"}
          </button>
        </div>
      </div>
      <div style={{ display: "flex", width: "50%", margin: "auto", gap: 50 }}>
        <select
          value={season}
          onChange={(e) => setSeasons(e.target.value)}
          style={{ width: "100%", fontSize: 26, textAlign: "center" }}
        >
          {availableSeasons.map((s) => (
            <option key={s} value={s}>
              {s}
            </option>
          ))}
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
      <Downloader
        data={usePostsTimeline ? timelineDataPosts : timelineDataComments}
        ChartComponent={BarChartComponent}
        props={{
          ylabel: "Comments",
        }}
      />
      <Downloader
        data={usePostsTimeline ? timelineDataPosts : timelineDataComments}
        ChartComponent={AreaChartComponent}
        props={{
          ylabel: "Comments",
        }}
      />

      <div style={{ display: "flex", gap: 20 }}>
        <h1>
          Athletes Percentage of Sentiment by{" "}
          {usePostsTimeline ? "Posts" : "Comments"}
        </h1>
        <div
          style={{
            display: "flex",
            alignItems: "center",
          }}
        >
          <button onClick={() => setUsePostsRadar(!usePostsRadar)}>
            {usePostsTimeline ? "Change To Comments" : "Change To Posts"}
          </button>
        </div>
      </div>
      <Downloader data={radarData} ChartComponent={RadarChartComponent} />
      <Downloader data={radarData} ChartComponent={SingleRadarChartComponent} />
    </div>
  );
};

export default App;
