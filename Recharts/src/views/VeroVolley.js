import React, { useEffect, useState } from "react";

import {
  getPiePlatformDistributionData,
  getPieSentimentDataByPlatforms,
} from "../helpers/pieData";
import { getTimelineData } from "../helpers/timelineData";
import Downloader from "../components/downloader";
import {
  AVAILABLE_KEYWORDS,
  AVAILABLE_PLATFORMS,
  AVAILABLE_SOURCES,
  countComments,
  countPosts,
} from "../helpers/formatData";
import {
  AreaChartComponent,
  BarChartComponent,
  PieChartComponent,
  RadarChartComponent,
} from "../components/graphs";

const VeroVolley = () => {
  return (
    <div
      style={{ display: "flex", flexDirection: "column", alignItems: "center" }}
    >
      <div style={{ width: "60%", marginBottom: "50px" }}>
        <p style={{ textAlign: "justify", fontSize: "1.5em" }}>
          This section shows the distribution of the sentiment on comments
          directed to Vero Volley. This means that the comments directed to the
          players or the team are not included in this analysis, and only the
          ones which talks directly about the club itself are included.
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
        <div style={{ width: "60%", marginBottom: "50px" }}>
          <h1>Season {season}</h1>
          <div style={{ display: "flex", justifyContent: "space-between" }}>
            <h2>
              Number of Posts:{" "}
              {countPosts(season, AVAILABLE_KEYWORDS["VeroVolley"])}
            </h2>
            <h2>
              Number of Comments:{" "}
              {countComments(season, AVAILABLE_KEYWORDS["VeroVolley"])}
            </h2>
          </div>
          <div style={{ display: "flex", justifyContent: "space-between" }}>
            <div>
              <h1>Distribution of sentiment over time</h1>
              <Downloader
                data={getTimelineData(
                  season,
                  AVAILABLE_PLATFORMS.map((p) => p.key),
                  AVAILABLE_SOURCES,
                  AVAILABLE_KEYWORDS["VeroVolley"],
                  false,
                  true
                )}
                name={`VeroVolley_AreaChart_Percentual_${season}`}
                xAxisLabel={"month"}
                ChartComponent={AreaChartComponent}
                props={{
                  ylabel: "Comments %",
                }}
                defaultWidth={1000}
                defaultHeight={300}
                justCsvDownload={true}
              />
              <Downloader
                data={getTimelineData(
                  season,
                  AVAILABLE_PLATFORMS.map((p) => p.key),
                  AVAILABLE_SOURCES,
                  AVAILABLE_KEYWORDS["VeroVolley"],
                  false,
                  false
                )}
                name={`VeroVolley_AreaChart_Quantity_${season}`}
                xAxisLabel={"month"}
                ChartComponent={AreaChartComponent}
                props={{
                  ylabel: "Comments",
                }}
                defaultWidth={1000}
                defaultHeight={300}
                justCsvDownload={true}
              />
            </div>
            <div style={{ display: "flex", flexDirection: "column" }}>
              <Downloader
                data={getPiePlatformDistributionData(
                  season,
                  AVAILABLE_SOURCES,
                  AVAILABLE_KEYWORDS["VeroVolley"],
                  false
                )}
                name={`VeroVolley_PieChart_Platforms_${season}`}
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
                data={getPieSentimentDataByPlatforms(
                  season,
                  AVAILABLE_KEYWORDS["VeroVolley"]
                )}
                name={`VeroVolley_PieChart_Sentiment_${season}`}
                xAxisLabel={"subject"}
                ChartComponent={PieChartComponent}
                props={{
                  title: "Sentiment Per Platform: [ONE PER PLATFORM]",
                }}
                defaultWidth={400}
                defaultHeight={272}
                justCsvDownload={true}
              />
            </div>
          </div>
        </div>
      ))}
    </div>
  );
};

export default VeroVolley;
