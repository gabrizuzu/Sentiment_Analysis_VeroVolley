import React, { useEffect, useState } from "react";

import getRadarData from "./helpers/radarData";
import {
  getPiePlatformDistributionData,
  getPieSentimentData,
} from "./helpers/pieData";
import { getTimelineData } from "./helpers/timelineData";
import Downloader from "./components/downloader";
import {
  AVAILABLE_KEYWORDS,
  AVAILABLE_PLATFORMS,
  AVAILABLE_SOURCES,
  dataToCSV,
} from "./helpers/formatData";
import {
  AreaChartComponent,
  BarChartComponent,
  PieChartComponent,
  RadarChartComponent,
  SingleRadarChartComponent,
} from "./components/graphs";
import { getOffensiveData } from "./helpers/offensiveData";

const App = () => {
  const availableSeasons = ["2023/2024", "2022/2023", "2021/2022", "2020/2021"];

  const [seasonTimeline, setSeasonTimeline] = useState(availableSeasons[0]);
  const [platformsTimeline, setPlatformsTimeline] = useState(
    Object.values(AVAILABLE_PLATFORMS).map((p) => p.key)
  );
  const [sourcesTimeline, setSourcesTimeline] = useState(AVAILABLE_SOURCES);
  const [usePostsTimeline, setUsePostsTimeline] = useState(true);
  const [usePercentageTimeline, setUsePercentageTimeline] = useState(false);
  const [keywordsTimeline, setKeywordsTimeline] = useState([
    ...AVAILABLE_KEYWORDS["VeroVolley"],
    "VeroVolley",
  ]);

  const [seasonsRadar, setSeasonsRadar] = useState(availableSeasons);
  const [platformsRadar, setPlatformsRadar] = useState(
    Object.values(AVAILABLE_PLATFORMS).map((p) => p.key)
  );
  const [usePostsRadar, setUsePostsRadar] = useState(true);

  console.log(getOffensiveData("2023/2024"));

  const timelineData = getTimelineData(
    seasonTimeline,
    platformsTimeline,
    sourcesTimeline,
    keywordsTimeline,
    usePostsTimeline,
    usePercentageTimeline
  );
  const piePlatformDistributionData = getPiePlatformDistributionData(
    seasonTimeline,
    sourcesTimeline,
    keywordsTimeline,
    usePostsTimeline
  );
  const radarData = getRadarData(seasonsRadar, platformsRadar, usePostsRadar);

  const [timelineAttrsName, setTimelineAttrsName] = useState("");
  useEffect(() => {
    const usePost = usePostsTimeline ? "Posts" : "Comments";
    const platforms = "[" + platformsTimeline.join(",") + "]";
    const season = seasonTimeline.replace("/", "-");
    setTimelineAttrsName(
      `${usePost}_${season}_${platforms}` +
        (usePercentageTimeline ? "_Percentual" : "") +
        (keywordsTimeline.includes("verovolley") ? "_WithVeroVolley" : "")
    );
  }, [
    usePostsTimeline,
    seasonTimeline,
    platformsTimeline,
    usePercentageTimeline,
    keywordsTimeline,
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
      <div style={{ display: "flex", width: "80%", margin: "auto", gap: 50 }}>
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
          {AVAILABLE_PLATFORMS.map((p) => (
            <option key={p.key} value={p.key}>
              {p.name}
            </option>
          ))}
        </select>
        <select
          value={sourcesTimeline}
          onChange={(e) =>
            setSourcesTimeline(
              Array.from(e.target.selectedOptions, (option) => option.value)
            )
          }
          style={{ width: "100%", fontSize: 26 }}
          multiple={true}
        >
          {AVAILABLE_SOURCES.map((s) => (
            <option key={s} value={s}>
              {s}
            </option>
          ))}
        </select>
        <select
          value={keywordsTimeline}
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
            setKeywordsTimeline(newKeywords);
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
        name={`Area_${timelineAttrsName}`}
        xAxisLabel="month"
        ChartComponent={AreaChartComponent}
        props={{
          ylabel:
            (usePostsTimeline ? "Posts" : "Comments") +
            (usePercentageTimeline ? " %" : ""),
        }}
      />
      <Downloader
        data={getOffensiveData(seasonTimeline)}
        name={`Offensive_Bar_${timelineAttrsName}`}
        xAxisLabel="subject"
        ChartComponent={BarChartComponent}
        props={{
          ylabel:
            (usePostsTimeline ? "Posts" : "Comments") +
            (usePercentageTimeline ? " %" : ""),
        }}
      />
      <Downloader
        data={piePlatformDistributionData}
        name={`Pie_Platforms_${timelineAttrsName}`}
        xAxisLabel="name"
        props={{ title: `Platforms Distribution` }}
        ChartComponent={PieChartComponent}
        getCustomCSVData={() => {
          const new_data = { id: 1 };
          // Data is in the format [{name: "Instagram", value: 10}, ...]
          // We want to convert it to [{Instagram: 10, ...}]
          for (const d of piePlatformDistributionData) {
            new_data[d.name] = d.value;
          }
          return dataToCSV([new_data], "id");
        }}
      />
      <Downloader
        data={getPieSentimentData(
          seasonTimeline,
          AVAILABLE_PLATFORMS.map((p) => p.key),
          sourcesTimeline,
          keywordsTimeline,
          usePostsTimeline
        )}
        name={`Pie_Total_${timelineAttrsName}`}
        xAxisLabel="name"
        props={{ title: `Total Sentiment Distribution` }}
        ChartComponent={PieChartComponent}
        getCustomCSVData={() => {
          const new_data = [{ Platform: "All" }];

          // Add the total sentiment distribution
          const temp_data = getPieSentimentData(
            seasonTimeline,
            AVAILABLE_PLATFORMS.map((p) => p.key),
            sourcesTimeline,
            keywordsTimeline,
            usePostsTimeline
          );
          for (const d of temp_data) {
            new_data[0][d.name] = d.value;
          }

          // Add the sentiment distribution for each platform
          for (const p of AVAILABLE_PLATFORMS) {
            new_data.push({ Platform: p.name });
            const temp_data = getPieSentimentData(
              seasonTimeline,
              [p.key],
              sourcesTimeline,
              keywordsTimeline,
              usePostsTimeline
            );
            for (const d of temp_data) {
              new_data[new_data.length - 1][d.name] = d.value;
            }
          }
          return dataToCSV(new_data, "Platform");
        }}
      />
      {AVAILABLE_PLATFORMS.map((platform) => (
        <Downloader
          key={platform.key}
          data={getPieSentimentData(
            seasonTimeline,
            [platform.key],
            sourcesTimeline,
            keywordsTimeline,
            usePostsTimeline
          )}
          name={`Pie_${platform.key}_${timelineAttrsName}`}
          xAxisLabel="name"
          props={{ title: `${platform.name} Sentiment Distribution` }}
          ChartComponent={PieChartComponent}
          getCustomCSVData={() => {
            const new_data = [{ Platform: "All" }];

            // Add the total sentiment distribution
            const temp_data = getPieSentimentData(
              seasonTimeline,
              AVAILABLE_PLATFORMS.map((p) => p.key),
              sourcesTimeline,
              keywordsTimeline,
              usePostsTimeline
            );
            for (const d of temp_data) {
              new_data[0][d.name] = d.value;
            }

            // Add the sentiment distribution for each platform
            for (const p of AVAILABLE_PLATFORMS) {
              new_data.push({ Platform: p.name });
              const temp_data = getPieSentimentData(
                seasonTimeline,
                [p.key],
                sourcesTimeline,
                keywordsTimeline,
                usePostsTimeline
              );
              for (const d of temp_data) {
                new_data[new_data.length - 1][d.name] = d.value;
              }
            }
            return dataToCSV(new_data, "Platform");
          }}
        />
      ))}

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
          {AVAILABLE_PLATFORMS.map((p) => (
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
