import getProcessedPosts from "./formatData";

const monthLabels = [
  "Jan",
  "Feb",
  "Mar",
  "Apr",
  "May",
  "Jun",
  "Jul",
  "Aug",
  "Sep",
  "Oct",
  "Nov",
  "Dec",
];

const seasonStart = 8;

// - Comments
export function countSentimentComments(platforms) {
  const posts = getProcessedPosts();
  const count = {
    "2020/2021": {
      positive: new Array(12).fill(0),
      negative: new Array(12).fill(0),
      neutral: new Array(12).fill(0),
    },
    "2021/2022": {
      positive: new Array(12).fill(0),
      negative: new Array(12).fill(0),
      neutral: new Array(12).fill(0),
    },
    "2022/2023": {
      positive: new Array(12).fill(0),
      negative: new Array(12).fill(0),
      neutral: new Array(12).fill(0),
    },
    "2023/2024": {
      positive: new Array(12).fill(0),
      negative: new Array(12).fill(0),
      neutral: new Array(12).fill(0),
    },
  };

  for (const post of posts) {
    if (!platforms.includes(post.platform)) {
      continue;
    }
    const comments = post.comments || [];

    for (const comment of comments) {
      if (!comment.author.includes("verovolley")) {
        const anno = comment.anno;
        const mese = comment.mese;
        const sentiment = comment.sentiment_comment;

        let season = `${anno - 1}/${anno}`;
        if (mese - 1 >= seasonStart) {
          season = `${anno}/${anno + 1}`;
        }

        if (count[season]) {
          if (sentiment === "positive") count[season].positive[mese - 1] += 1;
          else if (sentiment === "negative")
            count[season].negative[mese - 1] += 1;
          else if (sentiment === "neutral")
            count[season].neutral[mese - 1] += 1;
        }
      }
    }
  }

  return count;
}

// - Posts
export function countSentimentPosts(platforms) {
  const posts = getProcessedPosts();
  const count = {
    "2020/2021": {
      positive: new Array(12).fill(0),
      negative: new Array(12).fill(0),
      neutral: new Array(12).fill(0),
    },
    "2021/2022": {
      positive: new Array(12).fill(0),
      negative: new Array(12).fill(0),
      neutral: new Array(12).fill(0),
    },
    "2022/2023": {
      positive: new Array(12).fill(0),
      negative: new Array(12).fill(0),
      neutral: new Array(12).fill(0),
    },
    "2023/2024": {
      positive: new Array(12).fill(0),
      negative: new Array(12).fill(0),
      neutral: new Array(12).fill(0),
    },
  };

  for (const post of posts) {
    if (!platforms.includes(post.platform)) {
      continue;
    }
    const anno = post.anno;
    const mese = post.mese;
    const sentiment = post.sentiment_post;

    let season = `${anno - 1}/${anno}`;
    if (mese - 1 >= seasonStart) {
      season = `${anno}/${anno + 1}`;
    }

    if (count[season]) {
      if (sentiment === "positive") count[season].positive[mese - 1] += 1;
      else if (sentiment === "negative") count[season].negative[mese - 1] += 1;
      else if (sentiment === "neutral") count[season].neutral[mese - 1] += 1;
    }
  }

  return count;
}

export function getTimelineData(season, platforms, isComments = false) {
  let count;
  if (isComments) {
    count = countSentimentComments(platforms);
  } else {
    count = countSentimentPosts(platforms);
  }

  const data = [];

  for (const index of [...Array(12).keys()]) {
    const month = (index + seasonStart) % 12;
    data.push({
      month: monthLabels[month],
      positive: count[season].positive[month],
      negative: count[season].negative[month],
      neutral: count[season].neutral[month],
    });
  }

  return data;
}
