import React from "react";
import ReactDOM from "react-dom/client";
import App from "./App.tsx";
import "./index.css";

import WorkSession, { loader as sessionLoader } from "./pages/worksession.tsx";
import WorkSessionsSummaries from "./pages/worksessionsummaries.tsx";
import { createBrowserRouter, RouterProvider } from "react-router-dom";
import TagsPage from "./pages/tags.tsx";

const router = createBrowserRouter([
  {
    path: "/",
    element: <App />,
    children: [
      { 
        path: "/",
        element: <WorkSessionsSummaries />
      },
      {
        path: "/session/:sessionId",
        element: <WorkSession />,
        loader: sessionLoader,
      },
      {
        path: "/stats",
        element: <TagsPage/>
      }
    ],
  },
]);

ReactDOM.createRoot(document.getElementById("root")!).render(
  <React.StrictMode>
    <RouterProvider router={router} />
  </React.StrictMode>,
);
