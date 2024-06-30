import React from "react";
import {
  CDropdown,
  CDropdownDivider,
  CDropdownHeader,
  CDropdownItem,
  CDropdownMenu,
  CDropdownToggle,
  CAvatar
} from "@coreui/react";
import { cilLockUnlocked, cilUser } from "@coreui/icons";
import CIcon from "@coreui/icons-react";

import avatar from '../../assets/avatar.jpg'

const HeaderAccount = () => {
  return (
    <CDropdown variant="nav-item">
      <CDropdownToggle
        placement="bottom-end"
        className="py-0 pe-0 pl-4"
        caret={false}
      >
        <CAvatar src={avatar} size="md" />
      </CDropdownToggle>
      <CDropdownMenu className="pt-0" placement="bottom-end">
        <CDropdownHeader className="bg-body-secondary fw-semibold my-2">
          Учетная запись
        </CDropdownHeader>
        <CDropdownItem href="#">
          <CIcon icon={cilUser} className="me-2" />
          Профиль
        </CDropdownItem>
        <CDropdownDivider />
        <CDropdownItem href="#">
          <CIcon icon={cilLockUnlocked} className="me-2" />
          Выход
        </CDropdownItem>
      </CDropdownMenu>
    </CDropdown>
  );
};

export default HeaderAccount;
