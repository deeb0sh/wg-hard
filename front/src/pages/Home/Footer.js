import * as React from "react";
import { CFooter } from "@coreui/react";

const Footer = () => {
  return (
    <CFooter position='fixed'>
      <div>
        <span className="ml-1">&copy; {new Date().getFullYear()}</span>
      </div>
    </CFooter>
  );
};

export default Footer;
