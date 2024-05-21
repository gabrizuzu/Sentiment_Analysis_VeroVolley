import React, { useEffect, useState } from "react";

import getRadarData from "../helpers/radarData";
import {
  getPiePlatformDistributionData,
  getPieSentimentData,
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
  SingleRadarChartComponent,
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
              <AreaChartComponent
                data={getTimelineData(
                  season,
                  AVAILABLE_PLATFORMS.map((p) => p.key),
                  AVAILABLE_SOURCES,
                  AVAILABLE_KEYWORDS["VeroVolley"],
                  false,
                  true
                )}
                ylabel={"Comments %"}
                height={300}
                width={1000}
              />
              <AreaChartComponent
                data={getTimelineData(
                  season,
                  AVAILABLE_PLATFORMS.map((p) => p.key),
                  AVAILABLE_SOURCES,
                  AVAILABLE_KEYWORDS["VeroVolley"],
                  false,
                  false
                )}
                ylabel={"Comments"}
                height={300}
                width={1000}
              />
            </div>
            <div style={{ display: "flex", flexDirection: "column" }}>
              <PieChartComponent
                data={getPiePlatformDistributionData(
                  season,
                  AVAILABLE_KEYWORDS["VeroVolley"],
                  false
                )}
                title={"Platforms Distribution"}
                width={400}
                height={272}
              />
              <PieChartComponent
                data={getPieSentimentData(
                  [season],
                  AVAILABLE_PLATFORMS[0].key,
                  AVAILABLE_SOURCES,
                  AVAILABLE_KEYWORDS["VeroVolley"],
                  false
                )}
                title={"Sentiment Per Platform: " + AVAILABLE_PLATFORMS[0].name}
                width={400}
                height={272}
              />
            </div>
          </div>
        </div>
      ))}
    </div>
  );
};

export default VeroVolley;
