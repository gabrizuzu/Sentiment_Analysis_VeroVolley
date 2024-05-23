import React, { useEffect, useState } from "react";

import {
  getPiePlatformDistributionData,
  getPieSentimentData,
  getPieSentimentDataByPlatforms,
} from "../helpers/pieData";
import { getTimelineData } from "../helpers/timelineData";
import {
  AVAILABLE_KEYWORDS,
  AVAILABLE_PLATFORMS,
  AVAILABLE_SOURCES,
  countComments,
  countPosts,
} from "../helpers/formatData";
import {
  AreaChartComponent,
  PieChartComponent,
  RadarChartComponent,
} from "../components/graphs";
import Downloader from "../components/downloader";
import { getRadarData } from "../helpers/radarData";

const Athletes = () => {
  // all but VeroVolley
  const keywords = Object.keys(AVAILABLE_KEYWORDS).filter(
    (k) => k !== "VeroVolley"
  );

  return (
    <div
      style={{ display: "flex", flexDirection: "column", alignItems: "center" }}
    >
      <div style={{ width: "60%", marginBottom: "50px" }}>
        <p style={{ textAlign: "justify", fontSize: "1.5em" }}>
          This section shows the distribution of the sentiment on comments
          directed to the athletes. This means that the comments directed to the
          club are not included in this analysis, and only the ones which talks
          directly about the players are included.
        </p>
        <p style={{ textAlign: "justify", fontSize: "1.5em" }}>
          The area chart shows the distribution of the sentiment over time, both
          in percentage and in number of comments.
        </p>
        <p style={{ textAlign: "justify", fontSize: "1.5em" }}>
          The pie charts shows the distribution of the comments over the
          platforms, and the sentiment distribution over each platform.
        </p>
      </div>
      {["2023/2024", "2022/2023", "2021/2022"].map((season) => (
        <div key={season} style={{ width: "60%", marginBottom: "50px" }}>
          <h1>Season {season}</h1>

          <div style={{ display: "flex", justifyContent: "space-between" }}>
            <h2>Number of Posts: {countPosts(season, keywords)}</h2>
            <h2>Number of Comments: {countComments(season, keywords)}</h2>
          </div>
          <div
            style={{
              display: "flex",
              flexDirection: "column",
              justifyContent: "space-between",
            }}
          >
            <div>
              <h1>Distribution of sentiment over time</h1>
              <Downloader
                data={getTimelineData(
                  season,
                  AVAILABLE_PLATFORMS.map((p) => p.key),
                  AVAILABLE_SOURCES,
                  keywords,
                  false,
                  true
                )}
                name={`Athletes_AreaChart_Percentual_${season}`}
                xAxisLabel={"month"}
                ChartComponent={AreaChartComponent}
                props={{
                  ylabel: "Comments %",
                }}
                defaultHeight={300}
                defaultWidth={1000}
                justCsvDownload={true}
              />
              <Downloader
                data={getTimelineData(
                  season,
                  AVAILABLE_PLATFORMS.map((p) => p.key),
                  AVAILABLE_SOURCES,
                  keywords,
                  false,
                  false
                )}
                name={`Athletes_AreaChart_Quantity_${season}`}
                xAxisLabel={"month"}
                ChartComponent={AreaChartComponent}
                props={{
                  ylabel: "Comments",
                }}
                defaultHeight={300}
                defaultWidth={1000}
                justCsvDownload={true}
              />
            </div>
            <div style={{ display: "flex", justifyContent: "space-around" }}>
              <Downloader
                data={getPiePlatformDistributionData(
                  season,
                  AVAILABLE_SOURCES,
                  keywords,
                  false
                )}
                name={`Athletes_PieChart_Platforms_${season}`}
                xAxisLabel={"subject"}
                ChartComponent={PieChartComponent}
                props={{
                  title: "Platforms Comments Distribution",
                }}
                defaultWidth={400}
                defaultHeight={272}
                justCsvDownload={true}
              />
              <Downloader
                data={getPieSentimentDataByPlatforms(season, keywords)}
                name={`Athletes_PieChart_Sentiment_${season}`}
                xAxisLabel={"subject"}
                ChartComponent={PieChartComponent}
                props={{
                  title: "Sentiment Per Platform: [ONE PER PLATFORM]",
                }}
                defaultWidth={400}
                defaultHeight={272}
                justCsvDownload={true}
              />
              <div>
                <h2>Sentiment Distribution Per Athlete</h2>
                <Downloader
                  data={getRadarData(
                    [season],
                    AVAILABLE_PLATFORMS.map((p) => p.key),
                    false
                  )}
                  name={`Athletes_Radar_${season}`}
                  xAxisLabel="subject"
                  ChartComponent={RadarChartComponent}
                  defaultWidth={400}
                  defaultHeight={272}
                  justCsvDownload={true}
                />
              </div>
            </div>
          </div>
        </div>
      ))}
    </div>
  );
};

export default Athletes;
