import React from "react";
import { CHeader, CHeaderNav } from "@coreui/react";
import HeaderAccount from "./HeaderAccount";
import Breadcrumb from "./Breadcrumb";

const Header = () => {
  return (
    <CHeader className="justify-content-between px-4">
      <Breadcrumb />
      <CHeaderNav>
        <HeaderAccount />
      </CHeaderNav>
    </CHeader>
  );
};

export default Header;
