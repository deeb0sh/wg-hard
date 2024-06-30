import { useState } from "react";
import {
  CAccordion,
  CAccordionItem,
  CAccordionHeader,
  CAccordionBody,
  CCard,
  CCardBody,
  CCardHeader,
  CTable,
  CButton,
  CTooltip,
  CTableHead,
  CTableHeaderCell,
  CTableBody,
  CTableRow,
  CTableDataCell,
} from "@coreui/react";

import { cilUserPlus, cilCloudDownload, cilTrash } from "@coreui/icons";
import CIcon from "@coreui/icons-react";

import mock from "./mock.json";

const Configs = () => {
  const [configs, setConfigs] = useState(mock);

  const columns = [{ label: "Имя" }, { label: "IP-адрес" }];

  return (
    <CCard>
      <CCardHeader>
        <h4>DarkSurf.ru</h4>
      </CCardHeader>
      <CCardBody>
        <CAccordion alwaysOpen>
          {configs.map((config) => (
            <CAccordionItem>
              <CAccordionHeader>{config.w_host}</CAccordionHeader>
              <CAccordionBody>
                <CButton color="success" variant="outline">
                  <CIcon icon={cilUserPlus} /> Добавить
                </CButton>
                <CTable striped>
                  <CTableHead>
                    <CTableRow>
                      <CTableHeaderCell scope="col">#</CTableHeaderCell>
                      {columns.map((column) => (
                        <CTableHeaderCell scope="col">
                          {column.label}
                        </CTableHeaderCell>
                      ))}
                    </CTableRow>
                  </CTableHead>
                  <CTableBody>
                    {config.clients.map((client, idx) => (
                      <CTableRow>
                        <CTableHeaderCell scope="row">
                          {idx + 1}
                        </CTableHeaderCell>
                        <CTableDataCell>{client.name}</CTableDataCell>
                        <CTableDataCell>{client.ip}</CTableDataCell>
                        <CTableDataCell style={{width: "1%", cursor: "pointer"}}>
                          <CTooltip content="Скачать" placement="bottom-start">
                              <CIcon icon={cilCloudDownload} />
                          </CTooltip>
                        </CTableDataCell>
                        <CTableDataCell style={{width: "1%", cursor: "pointer"}}>
                          <CTooltip content="Удалить" placement="bottom-start">
                              <CIcon icon={cilTrash} />
                          </CTooltip>
                        </CTableDataCell>
                      </CTableRow>
                    ))}
                  </CTableBody>
                </CTable>
              </CAccordionBody>
            </CAccordionItem>
          ))}
        </CAccordion>
      </CCardBody>
    </CCard>
  );
};

export default Configs;
