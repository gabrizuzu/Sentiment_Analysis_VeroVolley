import React, { useCallback, useState } from "react";
import { useCurrentPng } from "recharts-to-png";
import FileSaver from "file-saver";

export default function Downloader({ data, props, ChartComponent }) {
  // useCurrentPng usage (isLoading is optional)
  const [getPng, { ref, isLoading }] = useCurrentPng();

  const [width, setWidth] = useState(1000);
  const [newWidth, setNewWidth] = useState("1000");
  const [height, setHeight] = useState(400);
  const [newHeight, setNewHeight] = useState("400");

  // Can also pass in options for html2canvas
  // const [getPng, { ref }] = useCurrentPng({ backgroundColor: '#000' });

  const handleDownload = useCallback(async () => {
    console.log("Downloading...");
    const png = await getPng();

    // Verify that png is not undefined
    if (png) {
      // Download with FileSaver
      FileSaver.saveAs(png, "myChart.png");
    } else {
      console.log("No png found.");
    }
  }, [getPng]);

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
      </div>
    </div>
  );
}
