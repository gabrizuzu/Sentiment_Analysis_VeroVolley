import React, { useCallback, useState } from "react";
import { useCurrentPng } from "recharts-to-png";
import FileSaver from "file-saver";
import uuid from "uuid";
import { dataToCSV } from "../helpers/formatData";

export default function Downloader({
  name,
  xAxisLabel,
  data,
  props,
  ChartComponent,
  getCustomCSVData = () => null,
  justCsvDownload = false,
  defaultWidth = 1000,
  defaultHeight = 400,
}) {
  // useCurrentPng usage (isLoading is optional)
  const [getPng, { ref, isLoading }] = useCurrentPng();

  const [width, setWidth] = useState(defaultWidth);
  const [newWidth, setNewWidth] = useState("1000");
  const [height, setHeight] = useState(defaultHeight);
  const [newHeight, setNewHeight] = useState("400");

  // Can also pass in options for html2canvas
  // const [getPng, { ref }] = useCurrentPng({ backgroundColor: '#000' });

  const handleDownload = useCallback(async () => {
    console.log("Downloading...");
    const png = await getPng();

    // Verify that png is not undefined
    if (png) {
      // Download with FileSaver
      FileSaver.saveAs(png, `${name}.png`);
    } else {
      console.log("No png found.");
    }
  }, [getPng, name]);

  const handleCSVDownload = useCallback(async () => {
    console.log("Downloading...");
    let csv = getCustomCSVData();
    if (!csv) {
      csv = dataToCSV(data, xAxisLabel);
    }
    const csvData = new Blob([csv], {
      type: "text/csv",
    });
    FileSaver.saveAs(csvData, `${name}.csv`);
  }, [data, xAxisLabel, name, getCustomCSVData]);

  return (
    <div style={{ marginTop: 20, marginBottom: 20 }}>
      <div
        style={{
          width: "100%",
          display: "flex",
          flexDirection: "column",
          justifyContent: "center",
          alignItems: "center",
          gap: 10,
        }}
      >
        <ChartComponent
          {...props}
          graphRef={ref}
          data={data}
          height={height}
          width={width}
        />
      </div>
      <br />
      <div
        style={{
          display: "flex",
          width: "100%",
          justifyContent: "center",
          gap: 10,
        }}
      >
        {!justCsvDownload && (
          <>
            <label>
              Width:
              <input
                type="text"
                value={newWidth}
                onChange={(e) => setNewWidth(e.target.value)}
              />
            </label>
            <label>
              Height:
              <input
                type="text"
                value={newHeight}
                onChange={(e) => setNewHeight(e.target.value)}
              />
            </label>
            <button
              onClick={() => {
                const fixedWidth = newWidth?.includes("%")
                  ? newWidth
                  : parseInt(newWidth);
                const fixedHeight = newHeight?.includes("%")
                  ? newHeight
                  : parseInt(newHeight);
                setWidth(fixedWidth || 1);
                setHeight(fixedHeight || 1);
              }}
            >
              Resize Chart
            </button>
            <button onClick={handleDownload}>
              {isLoading ? "Downloading..." : "Download Chart"}
            </button>
          </>
        )}
        <button onClick={handleCSVDownload}>Download CSV data</button>
      </div>
    </div>
  );
}
