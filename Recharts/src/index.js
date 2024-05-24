import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { createBrowserRouter, RouterProvider } from "react-router-dom";

import App from "./App";
import VeroVolley from "./views/VeroVolley";
import Athletes from "./views/Athletes";
import Offensive from "./views/Offensive";

const rootElement = document.getElementById("root");
const root = createRoot(rootElement);

const router = createBrowserRouter([
  {
    path: "/",
    element: <App />,
  },
  {
    path: "/vero-volley",
    element: <VeroVolley />,
  },
  {
    path: "/athletes",
    element: <Athletes />,
  },
  {
    path: "/offensive",
    element: <Offensive />,
  },
]);

root.render(
  <StrictMode>
    <nav
      style={{
        display: "flex",
        justifyContent: "center",
        gap: 20,
        backgroundColor: "lightgray",
        padding: 10,
      }}
    >
      <ul
        style={{
          display: "flex",
          justifyContent: "center",
          gap: 20,
          listStyleType: "none",
          fontSize: "1.5em",
        }}
      >
        <li>
          <a href="/">Sandbox</a>
        </li>
        <li>|</li>
        <li>Layouts for Group 5:</li>
        <li>
          <a href="/vero-volley">Vero Volley</a>
        </li>
        <li>
          <a href="/athletes">Athletes</a>
        </li>
        <li>
          <a href="/offensive">Offensive</a>
        </li>
      </ul>
    </nav>
    <RouterProvider router={router} />
  </StrictMode>
);
