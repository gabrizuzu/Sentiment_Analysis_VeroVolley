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
        const season = comment.season;
        const mese = comment.mese - 1;
        const sentiment = comment.sentiment_comment;

        if (count[season]) {
          if (sentiment === "positive")
            count[season].positive[(mese + 12 - seasonStart) % 12] += 1;
          else if (sentiment === "negative")
            count[season].negative[(mese + 12 - seasonStart) % 12] += 1;
          else if (sentiment === "neutral")
            count[season].neutral[(mese + 12 - seasonStart) % 12] += 1;
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
    const season = post.season;
    const mese = post.mese - 1;
    const sentiment = post.sentiment_post;

    if (count[season]) {
      if (sentiment === "positive")
        count[season].positive[(mese + 12 - seasonStart) % 12] += 1;
      else if (sentiment === "negative")
        count[season].negative[(mese + 12 - seasonStart) % 12] += 1;
      else if (sentiment === "neutral")
        count[season].neutral[(mese + 12 - seasonStart) % 12] += 1;
    }
  }

  return count;
}

export function getTimelineData(season, platforms, usePosts = true) {
  let count;
  if (usePosts) {
    count = countSentimentComments(platforms);
  } else {
    count = countSentimentPosts(platforms);
  }

  const data = [];

  for (const index of [...Array(12).keys()]) {
    data.push({
      month: monthLabels[(index + seasonStart) % 12],
      positive: count[season].positive[index],
      negative: count[season].negative[index],
      neutral: count[season].neutral[index],
    });
  }

  return data;
}
