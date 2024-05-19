import React, { useEffect, useState } from "react";
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
import { AVAILABLE_KEYWORDS } from "./helpers/formatData";

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
  Sylla: "#8884d8",
  Orro: "#82ca9d",
  Egonu: "#ffc658",
  Danesi: "#ff7300",
  Larson: "#ff0000",
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

  const [seasonTimeline, setSeasonTimeline] = useState(availableSeasons[0]);
  const [platformsTimeline, setPlatformsTimeline] = useState(
    Object.values(availablePlatforms).map((p) => p.key)
  );
  const [usePostsTimeline, setUsePostsTimeline] = useState(true);
  const [usePercentageTimeline, setUsePercentageTimeline] = useState(false);
  const [keywords, setKeywords] = useState(AVAILABLE_KEYWORDS[0]);

  const [seasonsRadar, setSeasonsRadar] = useState(availableSeasons);
  const [platformsRadar, setPlatformsRadar] = useState(
    Object.values(availablePlatforms).map((p) => p.key)
  );
  const [usePostsRadar, setUsePostsRadar] = useState(true);

  const timelineData = getTimelineData(
    seasonTimeline,
    platformsTimeline,
    keywords,
    usePostsTimeline,
    usePercentageTimeline
  );
  const radarData = getRadarData(seasonsRadar, platformsRadar, usePostsRadar);

  const [timelineAttrsName, setTimelineAttrsName] = useState("");
  useEffect(() => {
    const usePost = usePostsTimeline ? "Posts" : "Comments";
    const platforms = "[" + platformsTimeline.join(",") + "]";
    const season = seasonTimeline.replace("/", "-");
    setTimelineAttrsName(
      `${usePost}_${season}_${platforms}` +
        (usePercentageTimeline ? "_Percentual" : "")
    );
  }, [
    usePostsTimeline,
    seasonTimeline,
    platformsTimeline,
    usePercentageTimeline,
  ]);

  const [radarAttrsName, setRadarAttrsName] = useState("");
  useEffect(() => {
    const usePost = usePostsRadar ? "Posts" : "Comments";
    const platforms = "[" + platformsRadar.join(",") + "]";
    const seasons =
      "[" +
      seasonsRadar.map((value) => value.replace("/", "-")).join(",") +
      "]";
    setRadarAttrsName(`${usePost}_${seasons}_${platforms}`);
  }, [usePostsRadar, seasonsRadar, platformsRadar]);

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
          value={seasonTimeline}
          onChange={(e) => setSeasonTimeline(e.target.value)}
          style={{ width: "100%", fontSize: 26, textAlign: "center" }}
        >
          {availableSeasons.map((s) => (
            <option key={s} value={s}>
              {s}
            </option>
          ))}
        </select>
        <select
          value={platformsTimeline}
          onChange={(e) =>
            setPlatformsTimeline(
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
        <select
          value={keywords}
          onChange={(e) => {
            const selectedKeywords = Array.from(
              e.target.selectedOptions,
              (option) => option.value
            );
            const newKeywords = [];
            for (const keyword of selectedKeywords) {
              if (AVAILABLE_KEYWORDS[keyword]) {
                newKeywords.push(...AVAILABLE_KEYWORDS[keyword]);
              }
              newKeywords.push(keyword);
            }
            setKeywords(newKeywords);
          }}
          style={{ width: "100%", fontSize: 26 }}
          multiple={true}
        >
          {Object.keys(AVAILABLE_KEYWORDS).map((p) => (
            <option key={p} value={p}>
              {p}
            </option>
          ))}
        </select>
        <div
          style={{
            display: "flex",
            justifyContent: "center",
            alignItems: "center",
          }}
        >
          <label htmlFor="usePercentage">Percentual</label>
          <input
            id="usePercentage"
            type="checkbox"
            onChange={(e) => setUsePercentageTimeline(e.target.checked)}
            checked={usePercentageTimeline}
          ></input>
        </div>
      </div>

      <Downloader
        data={timelineData}
        name={`Bar_${timelineAttrsName}`}
        xAxisLabel="month"
        ChartComponent={BarChartComponent}
        props={{
          ylabel:
            (usePostsTimeline ? "Posts" : "Comments") +
            (usePercentageTimeline ? " %" : ""),
        }}
      />
      <Downloader
        data={timelineData}
        name={`Area_${timelineAttrsName}`}
        xAxisLabel="month"
        ChartComponent={AreaChartComponent}
        props={{
          ylabel:
            (usePostsTimeline ? "Posts" : "Comments") +
            (usePercentageTimeline ? " %" : ""),
        }}
      />

      <div style={{ display: "flex", gap: 20 }}>
        <h1>
          Athletes Percentage of Sentiment by{" "}
          {usePostsRadar ? "Posts" : "Comments"}
        </h1>
        <div
          style={{
            display: "flex",
            alignItems: "center",
          }}
        >
          <button onClick={() => setUsePostsRadar(!usePostsRadar)}>
            {usePostsRadar ? "Change To Comments" : "Change To Posts"}
          </button>
        </div>
      </div>
      <div style={{ display: "flex", width: "50%", margin: "auto", gap: 50 }}>
        <select
          value={seasonsRadar}
          onChange={(e) =>
            setSeasonsRadar(
              Array.from(e.target.selectedOptions, (option) => option.value)
            )
          }
          style={{ width: "100%", fontSize: 26, textAlign: "center" }}
          multiple={true}
        >
          {availableSeasons.map((s) => (
            <option key={s} value={s}>
              {s}
            </option>
          ))}
        </select>
        <select
          value={platformsRadar}
          onChange={(e) =>
            setPlatformsRadar(
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
        data={radarData}
        name={`Radar_${radarAttrsName}`}
        xAxisLabel="subject"
        ChartComponent={RadarChartComponent}
      />
      <Downloader
        data={radarData}
        name={`SingleRadar_${radarAttrsName}`}
        xAxisLabel="subject"
        ChartComponent={SingleRadarChartComponent}
      />
    </div>
  );
};

export default App;
