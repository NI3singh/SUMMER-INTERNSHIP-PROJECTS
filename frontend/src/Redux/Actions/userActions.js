import * as userConstants from "../Constants/userConstants";
import * as userApi from "../APIs/userServices";
import toast from "react-hot-toast";
import { ErrorsAction } from "../Protection";

// login action
const loginAction = (datas) => async (dispatch) => {
  try {
    dispatch({ type: userConstants.USER_LOGIN_REQUEST });
    const response = await userApi.loginService(datas);
    dispatch({ type: userConstants.USER_LOGIN_SUCCESS, payload: response });
  } catch (error) {
    ErrorsAction(error, dispatch, userConstants.USER_LOGIN_FAIL)
  }
};

// register action
const registerAction = (datas) => async (dispatch) => {
    try {
      dispatch({ type: userConstants.USER_REGISTER_REQUEST });
      const response = await userApi.registerService(datas);
      dispatch({ type: userConstants.USER_REGISTER_SUCCESS, payload: response });
      dispatch({ type: userConstants.USER_LOGIN_SUCCESS, payload: response });
    } catch (error) {
      ErrorsAction(error, dispatch, userConstants.USER_REGISTER_FAIL);
    }
  };
  // logout action
  const logoutAction = () => (dispatch) => {
    userApi.logoutService();
    dispatch({ type: userConstants.USER_LOGOUT });
    dispatch({ type: userConstants.USER_LOGIN_RESET });
    dispatch({ type: userConstants.USER_REGISTER_RESET });
  };
  
export{ loginAction, registerAction, logoutAction};