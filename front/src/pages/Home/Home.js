import * as React from "react";
import Footer from "./Footer";
import Header from "./Header";
import Content from "./Content";

const Home = () => {
  return (
    <div className="c-app c-default-layout">
      <div className="c-wrapper">
        <Header />
        <div className="c-body">
          <Content />
        </div>
        <Footer />
      </div>
    </div>
  );
};

export default Home;
