import React, { useEffect, useState } from "react";

import getRadarData from "../helpers/radarData";
import {
  getPiePlatformDistributionData,
  getPieSentimentData,
} from "../helpers/pieData";
import { getTimelineData } from "../helpers/timelineData";
import Downloader from "../components/downloader";
import { AVAILABLE_KEYWORDS, AVAILABLE_PLATFORMS } from "../helpers/formatData";
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
      {["2023/2024", "2022/2023", "2021/2022"].map((season) => (
        <div style={{ width: "60%", marginBottom: "50px" }}>
          <h1>Season {season}</h1>
          <div style={{ display: "flex", justifyContent: "space-between" }}>
            <div>
              <h1>Distribution of sentiment over time</h1>
              <AreaChartComponent
                data={getTimelineData(
                  season,
                  AVAILABLE_PLATFORMS.map((p) => p.key),
                  AVAILABLE_KEYWORDS["VeroVolley"],
                  false,
                  true
                )}
                ylabel={"Comments %"}
                height={600}
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
