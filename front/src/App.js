import React, { Suspense } from "react";
import { HashRouter, Route, Routes } from "react-router-dom";
import { CSpinner,  } from '@coreui/react'
import "./scss/style.scss";
import Login from "./pages/Login/Login";
import Home from "./pages/Home/Home";

const App = () => {
  return (
    <HashRouter>
      <Suspense
        fallback={
          <div className="pt-3 text-center">
            <CSpinner color="primary" variant="grow" />
          </div>
        }
      >
        <Routes>
          <Route exact path="/login" element={<Login />} />
          <Route path="*" element={<Home />} />
        </Routes>
      </Suspense>
    </HashRouter>
  );
};

export default App;
