import React, { useEffect, useState } from "react";

import { AVAILABLE_KEYWORDS, AVAILABLE_PLATFORMS } from "../helpers/formatData";
import {
  InvertedBarChartComponent,
  PieChartComponent,
  RadarChartComponent,
} from "../components/graphs";
import {
  getOffensiveData,
  getOffensiveDistributionData,
} from "../helpers/offensiveData";
import Downloader from "../components/downloader";
import { getRadarDataSentimentAsCorners } from "../helpers/radarData";

const Offensive = () => {
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
          This section shows the information about the offensive comments found
          accross the data. The comments are marked as offensive with four
          classifications:
        </p>
        <ul>
          <li>
            Toxicity: Comments that are offensive, disrespectful, or otherwise
            likely to make people leave a discussion.
          </li>
          <li>
            Severe toxicity: Comments that are very toxic or extremely
            offensive.
          </li>
          <li>
            Identity attack: Comments that are directly attacking the identity
            of a person or group.
          </li>
          <li>Insult: Comments that contain an insult.</li>
        </ul>
        <p style={{ textAlign: "justify", fontSize: "1.5em" }}>
          The bar charts shows the distribution of the offensive comments over
          Vero Volley, and some of the main players. The data is shown in
          percentage and in number of comments.
        </p>
        <p style={{ textAlign: "justify", fontSize: "1.5em" }}>
          The pie chart shows the four levels of offensive classification by
          subject.
        </p>
      </div>
      {["2023/2024", "2022/2023", "2021/2022"].map((season) => (
        <div style={{ width: "60%", marginBottom: "50px" }}>
          <h1>Season {season}</h1>
          <div style={{ display: "flex", justifyContent: "space-between" }}>
            <div>
              <h1>Offensive Messages Per Subject</h1>
              {/* <InvertedBarChartComponent
                data={getOffensiveData(
                  season,
                  AVAILABLE_PLATFORMS.map((p) => p.key),
                  true
                )}
                height={300}
                width={1000}
              /> */}
              <Downloader
                data={getOffensiveData(
                  season,
                  AVAILABLE_PLATFORMS.map((p) => p.key),
                  true
                )}
                name={`Offensive_BarChart_Percentual_${season}`}
                xAxisLabel={"subject"}
                ChartComponent={InvertedBarChartComponent}
                defaultWidth={1000}
                defaultHeight={300}
                justCsvDownload={true}
              />

              <Downloader
                data={getOffensiveData(
                  season,
                  AVAILABLE_PLATFORMS.map((p) => p.key),
                  false
                )}
                name={`Offensive_BarChart_Quantity_${season}`}
                xAxisLabel={"subject"}
                ChartComponent={InvertedBarChartComponent}
                defaultWidth={1000}
                defaultHeight={300}
                justCsvDownload={true}
              />
            </div>
            <div style={{ display: "flex", flexDirection: "column" }}>
              <Downloader
                data={getOffensiveDistributionData(
                  season,
                  AVAILABLE_PLATFORMS.map((p) => p.key)
                )}
                name={`Offensive_PieChart_${season}`}
                xAxisLabel={"subject"}
                props={{
                  title: "Toxicity Levels Per Subject: [ONE PER SUBJECT]",
                }}
                ChartComponent={PieChartComponent}
                defaultWidth={400}
                defaultHeight={272}
                justCsvDownload={true}
              />
              <h2>Sentiment Distribution Per Athlete</h2>
              <Downloader
                data={getRadarDataSentimentAsCorners(
                  [season],
                  AVAILABLE_PLATFORMS.map((p) => p.key),
                  false
                )}
                name={`Offensive_Radar_${season}`}
                xAxisLabel="subject"
                ChartComponent={RadarChartComponent}
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

export default Offensive;
