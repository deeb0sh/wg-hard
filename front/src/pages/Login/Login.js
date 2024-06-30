import React, { useState, useRef } from "react";
import {
  CButton,
  CCard,
  CCardBody,
  CCardGroup,
  CCol,
  CContainer,
  CForm,
  CFormInput,
  CInputGroup,
  CInputGroupText,
  CRow,
  CModal,
  CModalTitle,
  CModalHeader,
  CModalBody,
  CImage,
  CSpinner,
  CToast,
  CToastBody,
  CToastHeader,
  CToaster,
} from "@coreui/react";
import CIcon from "@coreui/icons-react";
import { cilLockLocked, cilUser } from "@coreui/icons";
import ForgottenImage from "../../assets/pacany.jpg";

const Login = () => {
  const [isShowModal, setShowModal] = useState(false);
  const [validated, setValidated] = useState(false);
  const [preccesing, setPreccesing] = useState(false);
  const [toast, addToast] = useState(0);
  const toaster = useRef();
  const [username, changeUsername] = useState("");
  const [password, changePassword] = useState("");

  const sleep = (ms = 0) => new Promise((resolve) => setTimeout(resolve, ms));

  const handleSubmit = async (event) => {
    event.preventDefault();
    setValidated(true);

    const form = event.currentTarget;
    if (form.checkValidity() === false) {
      event.stopPropagation();
      return;
    }

    setPreccesing(true);
    await sleep(5000);
    setPreccesing(false);
    addToast(failedLogginToast);

    setValidated(true);
  };

  const failedLogginToast = (
    <CToast color="danger" delay={5000} animation={true}>
      <CToastHeader closeButton>
        <div className="fw-bold me-auto">Ошибка</div>
      </CToastHeader>
      <CToastBody>Неверный логин или пароль</CToastBody>
    </CToast>
  );

  return (
    <div className="bg-body-tertiary min-vh-100 d-flex flex-row align-items-center">
      <CContainer>
        <CRow className="justify-content-center">
          <CCol md={5}>
            <CCardGroup>
              <CCard className="p-4">
                <CCardBody>
                  <CForm
                    className="needs-validation"
                    validated={validated}
                    onSubmit={handleSubmit}
                    noValidate
                  >
                    <h1>Авторизация</h1>
                    <p className="text-body-secondary">
                      Войдите в свой аккаунт
                    </p>
                    <CInputGroup className="mb-3">
                      <CInputGroupText>
                        <CIcon icon={cilUser} />
                      </CInputGroupText>
                      <CFormInput
                        placeholder="Логин"
                        autoComplete="username"
                        value={username}
                        onChange={(e) => changeUsername(e.target.value)}
                        disabled={preccesing}
                        required
                      />
                    </CInputGroup>
                    <CInputGroup className="mb-4">
                      <CInputGroupText>
                        <CIcon icon={cilLockLocked} />
                      </CInputGroupText>
                      <CFormInput
                        type="password"
                        placeholder="Пароль"
                        autoComplete="current-password"
                        value={password}
                        onChange={(e) => changePassword(e.target.value)}
                        disabled={preccesing}
                        required
                      />
                    </CInputGroup>
                    <CRow>
                      <CCol xs={6}>
                        <CButton
                          color="primary"
                          className="px-4"
                          type="submit"
                          disabled={preccesing}
                        >
                          {preccesing && (
                            <CSpinner as="span" size="sm" aria-hidden="true" />
                          )}
                          {!preccesing && "Войти"}
                        </CButton>
                      </CCol>
                      <CCol xs={6} className="text-right">
                        <CButton
                          color="link"
                          className="px-0"
                          onClick={() => setShowModal(!isShowModal)}
                        >
                          Забыли пароль?
                        </CButton>
                      </CCol>
                    </CRow>
                  </CForm>
                </CCardBody>
              </CCard>
            </CCardGroup>
          </CCol>
        </CRow>
        <CModal
          size="xl"
          visible={isShowModal}
          onClose={() => setShowModal(false)}
          aria-labelledby="forgottemModal"
        >
          <CModalHeader>
            <CModalTitle id="forgottemModal">Какая досада</CModalTitle>
          </CModalHeader>
          <CModalBody>
            <CRow className="justify-content-center">
              <CImage rounded src={ForgottenImage} />
            </CRow>
          </CModalBody>
        </CModal>
        <CToaster
          className="p-3"
          placement="top-end"
          push={toast}
          ref={toaster}
        />
      </CContainer>
    </div>
  );
};

export default Login;
