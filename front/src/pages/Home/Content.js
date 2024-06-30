import React, { Suspense } from "react";
import { Navigate, Route, Routes } from "react-router-dom";
import { CContainer } from "@coreui/react";
import routes from "../../routes";

const loading = (
  <div className="d-flex justify-content-center align-items-center h-100">
    <div
      className="spinner-border text-info"
      style={{ width: "5rem", height: "5rem" }}
      role="status"
    >
      <span className="sr-only">Loading...</span>
    </div>
  </div>
);

const Content = () => {
  return (
    <main className="c-main">
      <CContainer className="h-100 pt-4">
        <Suspense fallback={loading}>
          <Routes>
            {routes.map((route, idx) => {
              return (
                route.component && (
                  <Route
                    key={idx}
                    path={route.path}
                    exact={route.exact}
                    name={route.name}
                    element={<route.component />}
                  />
                )
              );
            })}
            <Route path="/" element={<Navigate to="configs" replace />} />
          </Routes>
        </Suspense>
      </CContainer>
    </main>
  );
};

export default React.memo(Content)
;
