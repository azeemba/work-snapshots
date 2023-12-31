import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.tsx'
import './index.css'

import WorkSession, { loader as sessionLoader } from "./pages/worksession.tsx"
import WorkSessionsSummaries from "./pages/worksessionsummaries.tsx"
import { createBrowserRouter, RouterProvider } from "react-router-dom";

const router = createBrowserRouter([
  {
    path: "/",
    element: <App />,
    children: [
      { path: "/", element: <WorkSessionsSummaries /> },
      {
        path: "/session/:sessionId",
        element: <WorkSession />,
        loader: sessionLoader,
      },
    ],
  },
]);

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <RouterProvider router={router} />
  </React.StrictMode>,
);