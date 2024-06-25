import React, { Suspense } from 'react'
import { HashRouter, Route, Routes } from 'react-router-dom'

import { CSpinner } from '@coreui/react'

import './scss/style.scss'

const Login = React.lazy(() => import('./pages/Login'))

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
          <Route exact path="/login" name="Login Page" element={<Login />} />
          <Route path="*" name="Home" element={<Login />} />
        </Routes>
      </Suspense>
    </HashRouter>
  );
}

export default App;
