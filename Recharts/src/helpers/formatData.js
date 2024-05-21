import posts from "../data/sentiment_output";

export const AVAILABLE_KEYWORDS = {
  VeroVolley: ["monza", "verovolley", "vero volley", "allianz milano"],
  egonu: null,
  orro: null,
  danesi: null,
  larson: null,
  sylla: null,
  cazaute: null,
  malual: null,
  heyrman: null,
  folie: null,
  prandi: null,
  pusic: null,
  rettke: null,
  bajema: null,
  daalderop: null,
  candi: null,
  castillo: null,
};

export const AVAILABLE_PLATFORMS = [
  { name: "Facebook", key: "FB" },
  { name: "Instagram", key: "IG" },
  { name: "Web", key: "Web" },
];

export const AVAILABLE_SOURCES = posts
  .map((post) => post.source)
  .filter((v, i, a) => a.indexOf(v) === i)
  .sort();

export default function getProcessedPosts() {
  return posts;
}

export function dataToCSV(data, xAxisLabel) {
  if (!data.length) {
    return "";
  }

  let csv = "";
  const separator = ";";

  // Set header
  const header = Object.keys(data[0]);
  header.splice(header.indexOf(xAxisLabel), 1);
  header.unshift(xAxisLabel);

  for (const key of header) {
    csv += key.charAt(0).toUpperCase() + key.slice(1) + separator;
  }
  csv = csv.slice(0, csv.length - 1) + "\n";

  // Set data
  for (const row of data) {
    for (const key of header) {
      csv += row[key] + separator;
    }
    csv = csv.slice(0, csv.length - 1) + "\n";
  }
  return csv;
}

export function countPosts(season, keywords) {
  let count = 0;
  for (const post of posts) {
    if (
      post.season === season &&
      keywords.some((k) => post.keywords.includes(k))
    ) {
      count += 1;
    }
  }
  return count;
}

export function countComments(season, keywords) {
  let count = 0;
  for (const post of posts) {
    if (
      post.season === season &&
      keywords.some((k) => post.keywords.includes(k))
    ) {
      count += post.comments.length;
    }
  }
  return count;
}
