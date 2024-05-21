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
    <RouterProvider router={router} />
  </StrictMode>
);
